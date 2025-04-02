from flask import Blueprint, jsonify, request
from config.config import Config,get_redis_db_connection
import orjson as json
from datetime import datetime


bp = Blueprint('utility', __name__)

r = get_redis_db_connection()


def get_settings():
    values = {
        "status": "success",
        "settings": { 
            "storageLimit": Config.STORAGE_LIMIT, 
            "storageInterval": Config.STORAGE_INTERVAL,
            "storageTask": Config.STORAGE_TASK, 
            "logging": Config.LOGGING,
            "fakeValues": Config.FAKE_VALUES, 
            "time": datetime.now().strftime("%M:%S:%f")
        }
    }
    return values



@bp.route('/api/logging', methods=['POST'])
def enable_logging_route():
    content = request.json
    print(content)
    Config.LOGGING=content["logging"]
    response = jsonify(get_settings())
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response



@bp.route('/api/get/settings', methods=['GET'])
def get_settings_route():

    response = jsonify(get_settings())
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response
