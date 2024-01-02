from rmbserver.servers.base import app
from flask import jsonify
from rmbserver.exceptions import (
    ChatNotFound,
    DataSourceNotFound,
    DataSourceExists,
    ParameterError,
    DataSourceConfigError,
    PromptTooLong,
)


# 定义一个错误处理器
@app.errorhandler(ChatNotFound)
def handle_chat_not_found_error(error):
    return jsonify({'message': error.message, 'code': error.code}), 404


@app.errorhandler(DataSourceNotFound)
def handle_datasource_not_found_error(error):
    return jsonify({'message': str(error)}), 404


@app.errorhandler(DataSourceExists)
def handle_datasource_exists_error(error):
    return jsonify({'message': str(error)}), 409


@app.errorhandler(ParameterError)
def handle_parameter_error(error):
    return jsonify({'message': str(error)}), 400


@app.errorhandler(DataSourceConfigError)
def handle_datasource_config_error(error):
    return jsonify({'message': error.message, 'code': error.code}), 400


@app.errorhandler(PromptTooLong)
def handle_parameter_error(error):
    return jsonify({'message': str(error)}), 400


