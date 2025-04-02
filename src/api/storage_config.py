from flask import Blueprint, jsonify, request
from config.config import Config,get_redis_db_connection
from api.utility import get_settings
import orjson as json


bp = Blueprint('storage_config', __name__)

r = get_redis_db_connection()


def get_last_values():
    data = r.lrange("measurements", 0, 1)

    return json.loads(data[0])


@bp.route('/api/storage/task', methods=['POST'])
def enable_storage_route():
    content = request.json
    if Config.LOGGING:
        print(content)
    Config.STORAGE_TASK=content["task"]
    response = jsonify(get_settings())
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response


@bp.route('/api/storage/interval', methods=['POST'])
def storage_interval_route():
    content = request.json
    if Config.LOGGING:
        print(content)
    Config.STORAGE_INTERVAL=content["interval"]
    response = jsonify(get_settings())
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response


@bp.route('/api/storage/limit', methods=['POST'])
def storage_limit_route():
    content = request.json
    if Config.LOGGING:
        print(content)
    Config.STORAGE_LIMIT=content["limit"]
    response = jsonify(get_settings())
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response


@bp.route('/api/storage/data', methods=['GET'])
def storage_data_route():
    # read `limit` parameter from request, default 10)
    limit = request.args.get('limit', default=10, type=int)

    data = r.lrange("measurements", 0, limit - 1)  # get last 'limit' values from redis

    parsed_data = [json.loads(entry) for entry in data]
    if Config.LOGGING:
        print(parsed_data)
    if limit == 1 and parsed_data:
        return jsonify(parsed_data[0])  # if only one
    else:
        return jsonify(parsed_data)