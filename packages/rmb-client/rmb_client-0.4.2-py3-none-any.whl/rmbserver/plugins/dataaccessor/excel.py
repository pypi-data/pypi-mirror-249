import pandas as pd
import os
import sqlite3
import pandas.errors
from pandas import DataFrame
import requests
from io import BytesIO
import tempfile
import time
import hashlib
from apscheduler.schedulers.background import BackgroundScheduler

from rmbserver.plugins.dataaccessor.da_base import BaseDataAccessor
from rmbserver.plugins.dataaccessor.da_register import register_data_accessor
from rmbserver.log import log
from rmbcommon.models import MetaData, DataSchema, DataTable, DataField, StrucQuery
from rmbserver.plugins.model.excel import ExcelQuery, ExcelQueryResult
from rmbserver import config
from rmbserver.exceptions import DataSourceConfigError, InvalidStrucQuery
from rmbserver.ai.generations import ai_generate
from rmbserver.plugins.ai.prompts import PROMPT_ANALYSE_SHEET_DATA


@register_data_accessor
class ExcelDataAccessor(BaseDataAccessor):
    __source_type__ = "Excel"

    # location_type: local, http
    # location_url: local file path or http(s) url
    __access_config_keys_must__ = ['location_type', 'location_url']

    PROMPT_GEN_STRUC_QUERY = """这是一个Excel文件，已经被导入到一个SQLite数据库中，每个sheet对应一个表。
注意：
1. 在SQLite中没有MySQL中的DB（Schema）的概念，因此在生成的SQL中请直接使用table，而不要使用db.table。
2. 表名需要像这样`table_name`引起来。"""

    # 创建临时目录
    TEMP_DIR = tempfile.mkdtemp()
    # 设置过期时间（例如5分钟）
    EXPIRATION_TIME = 300  # 300秒

    # 缓存sqlite连接
    _cached_sqlite_conns = {}

    def _get_file_name(self):
        location_type = self.ds_access_config.get('location_type')
        location_url = self.ds_access_config.get('location_url')

        if location_type == 'local':
            file_name, file_ext = os.path.basename(location_url).split('.')
        elif location_type == 'http':
            file_name, file_ext = location_url.split('/')[-1].split('.')
        else:
            raise ValueError('location_type must be local or http')

        # 对URL应用哈希函数，创建一个唯一的文件名
        url_hash_object = hashlib.sha256(location_url.encode())
        unique_filename = url_hash_object.hexdigest()

        return file_name, file_ext, unique_filename

    def _read_excel(self, sheet_name=None, skip_rows=0):
        location_type = self.ds_access_config.get('location_type')
        location_url = self.ds_access_config.get('location_url')
        max_file_size = config.rmb_max_exec_file_size

        if location_type == 'local':
            # 检查文件大小
            file_size = os.path.getsize(location_url)
            if file_size > max_file_size:
                raise DataSourceConfigError(f"The file size exceeds the limit of {max_file_size} bytes.")
            excel_data = pd.read_excel(location_url, sheet_name=sheet_name, skiprows=skip_rows)

        elif location_type == 'http':
            # 先发送HEAD请求以获取文件大小
            response = requests.head(location_url)
            content_length = int(response.headers.get('content-length', 0))
            if content_length > max_file_size:
                raise DataSourceConfigError(f"The file size exceeds the limit of {max_file_size} bytes.")

            # 然后发送GET请求以获取数据
            response = requests.get(location_url)
            response.raise_for_status()  # 确保请求成功
            excel_data = pd.read_excel(BytesIO(response.content), sheet_name=sheet_name, skiprows=skip_rows)

        else:
            raise ValueError('location_type must be local or http')

        return excel_data

    def _analyse_data(self, excel_data) -> dict:
        sheets_top_n_rows = ''
        for sheet_name, sheet_data in excel_data.items():
            sheets_top_n_rows += f"sheet name: {sheet_name}\n"
            sheets_top_n_rows += f"sheet top 8 rows:\n"
            sheets_top_n_rows += sheet_data.head(8).to_string(index=True)
            sheets_top_n_rows += '\n'
        result = ai_generate(
            "ANALYSE_SHEET_DATA",
            PROMPT_ANALYSE_SHEET_DATA,
            sheets_top_n_rows=sheets_top_n_rows,
        )
        return result

    def _read_sheet(self, sheet_name: str, sheet_analyse_rst: dict) -> DataFrame:
        # 根据分析出来的sheet特征，比如首行、表头等，读取数据
        sheet_data = self._read_excel(
            sheet_name=sheet_name,
            skip_rows=sheet_analyse_rst['data_begin_row']
        )
        # 只保留需要的列数
        data_end_col = len(sheet_analyse_rst['columns'])
        sheet_data = sheet_data.iloc[:, :data_end_col]
        # 重命名列为自定义的字段名
        sheet_data.columns = sheet_analyse_rst['columns']
        # log.debug(f"Sheet '{sheet_name}' 的前3行数据: {sheet_data.head(3)}")
        return sheet_data

    def _read_excel_head_n(self, analyse_rst, n=5) -> dict:
        # 利用分析后的结果，来获取Excel前N行数据（跳过表头）
        excel_head_n_dict = {}
        for sheet_name, sheet_aly_rst in analyse_rst.items():
            sheet_data = self._read_sheet(sheet_name, sheet_aly_rst)
            # 获取每列的前五行
            top_five_rows = sheet_data.head(n)

            # 初始化一个空字典来存储结果
            excel_head_n_dict[sheet_name] = {}

            # 遍历所有列
            for column in top_five_rows.columns:
                # 将每列的前五行数据转换为字符串列表
                # 使用 .astype(str) 确保所有数据都转换为字符串类型
                # 然后使用 .tolist() 转换为列表
                column_data_as_str = top_five_rows[column].astype(str).tolist()

                # 将列表转换为单个字符串，各个元素之间以逗号分隔
                # 截取前20字符，避免太长
                column_data_str = ', '.join([i[:20] for i in column_data_as_str])

                # 将结果存储在字典中
                excel_head_n_dict[sheet_name][column] = column_data_str
        return excel_head_n_dict

    def retrieve_meta_data(self) -> MetaData:
        excel_data = self._read_excel()
        file_name, _, _ = self._get_file_name()
        # Create MetaData object
        metadata_object = MetaData(name=f"Excel_{file_name}")

        # Create 1 DataSchema for whole excel file
        data_schema = DataSchema(
            name=file_name,
            metadata=metadata_object,
            origin_desc=""
        )

        # 分析数据
        analyse_rst = self._analyse_data(excel_data)

        # 获取前N行数据
        excel_head_n_dict = self._read_excel_head_n(analyse_rst, n=6)

        # for sheet_name, sheet_data in excel_data.items():
        for sheet_name, sheet_aly_rst in analyse_rst.items():
            if not sheet_aly_rst['exists_table']:
                log.warning(f"表格{sheet_name}不是结构化表格，不导入到数据库中。")
                continue

            # Create DataTable for each sheet
            data_table = DataTable(
                name=sheet_name,
                origin_desc="",
                schema=data_schema,
            )

            # Create DataField for each column in the sheet
            # 使用分析结果中的列名
            # 将 head N 写入Meta，待推理的时候使用
            for column_name in sheet_aly_rst['columns']:
                data_field = DataField(
                    name=column_name,
                    origin_desc="",
                    table=data_table,
                    sample_data=excel_head_n_dict[sheet_name][column_name],
                )

                data_table.add_field(data_field)

            # Add DataTable to DataSchema
            data_schema.add_table(data_table)

        if not data_schema.tables:
            raise DataSourceConfigError("Excel文件中没有可解析的二维表格。")

        # 将分析后的结果写入Meta，待查询的时候使用
        data_schema.set_custom_config(
            "analyse_rst", analyse_rst
        )

        # Add DataSchema to MetaData
        metadata_object.add_schema(data_schema)

        log.debug(f"从Excel中获取的Meta：{metadata_object.to_dict()}")

        return metadata_object

    def query(self, struc_query: StrucQuery, meta_data: MetaData) -> ExcelQueryResult:
        if not meta_data:
            raise ValueError("meta_data is required in an excel data query.")
        file_name, _, unique_filename = self._get_file_name()
        temp_sqlite_db_file = os.path.join(self.TEMP_DIR, unique_filename+'.sqlite')

        conn = self._cached_sqlite_conns.get(unique_filename)

        if os.path.exists(temp_sqlite_db_file) and conn:
            log.info(f"使用缓存的sqlite连接：{temp_sqlite_db_file}")
        else:
            log.info(f"创建sqlite连接：{temp_sqlite_db_file}")
            conn = sqlite3.connect(temp_sqlite_db_file)

            # excel_data = self._read_excel()

            meta_schema = meta_data.schemas[0]
            analyse_rst = meta_schema.get_custom_config('analyse_rst')

            # for sheet_name, sheet_data in excel_data.items():
            for sheet_name, configs in analyse_rst.items():
                if not configs['exists_table']:
                    log.warning(f"表格{sheet_name}不是结构化表格，不导入到数据库中。")
                    continue

                # 根据分析出来的sheet特征，比如首行、表头等，读取数据
                sheet_data = self._read_sheet(sheet_name, configs)

                sheet_data.to_sql(
                    sheet_name, con=conn, if_exists='replace', index=False
                )
            self._cached_sqlite_conns[unique_filename] = conn

        try:
            result = pd.read_sql_query(
                struc_query.content, conn,
                params=struc_query.params_for_query
            )
        except pandas.errors.DatabaseError as e:
            raise InvalidStrucQuery(f"执行SQL语句出错：{e} {struc_query}")
        return ExcelQueryResult(query=struc_query, result=result)


    @classmethod
    def cleanup_temp_dir(cls):
        for file in os.listdir(cls.TEMP_DIR):
            file_path = os.path.join(cls.TEMP_DIR, file)
            # 检查文件最后访问时间
            if os.path.getatime(file_path) + cls.EXPIRATION_TIME < time.time():
                log.info(f"删除临时文件：{file_path}")
                os.remove(file_path)

                cls._cached_sqlite_conns.pop(file, None)


log.info(f"registering data accessor: {ExcelDataAccessor.__source_type__}")


# 创建一个后台调度器
scheduler = BackgroundScheduler()
scheduler.add_job(ExcelDataAccessor.cleanup_temp_dir, 'interval', minutes=5)
log.info(f"启动后台任务：删除ExcelDataAccessor的临时文件...")
scheduler.start()

