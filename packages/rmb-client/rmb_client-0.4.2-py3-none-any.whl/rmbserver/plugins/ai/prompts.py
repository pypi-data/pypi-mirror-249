PROMPT_ANALYSE_SHEET_DATA = """
任务描述：
需要从Excel表格中识别和提取二维表数据，然后将其转换为SQLite数据库格式。目标是识别表格的列名、表头和数据的起始行。

要求：
识别最左侧的第一个二维表格。这个表格由紧邻的列组成，没有中间空列。

提取的信息需要包括：
- 表格是否存在（exists_table），若不存在，其他字段无意义，可不填
- 数据的起始行（data_begin_row），取自左侧第一列Index序号值
- 列名（columns），结合多行表头生成


示例数据：
Sheet名称：2月
前两行作为表头。

输入示例
```yaml
sheet name: 2月
sheet top rows:
  Unnamed: 0 一单元 Unnamed: 2 二单元 Unnamed: 4
0         姓名  数学         语文  数学         语文
1         张三   1          2   3          4
2         李四   1          2   3          4
...（后续行数据）
```

输出格式：

```json
{
  "sheet_name": {
      "exists_table": true|false,    
      "data_begin_row": [整数],
      "columns": [
          "col1", 
          "col2",
          ...
      ]
  }
}
```

--- 待分析数据 begin---
{{ sheets_top_n_rows }}
--- 待分析数据 end---

备注：请根据上述待分析数据，识别并提取表格信息。
"""
