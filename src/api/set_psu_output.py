from flask import Blueprint, jsonify, request
import time
from config.config import Config,logging
from api.storage_config import get_last_values
from api.fake_psu_values import FakeValues



bp = Blueprint('set_psu_output', __name__)
    
opsu=Config.USB_DEVICE_OBJECT




@bp.route('/api/set/output', methods=['POST'])
def set_output_route():
    content = request.json
    if Config.LOGGING:
        print(content)
    response = jsonify(set_output(content))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response



def set_output(content):

    try:
        Config.STORAGE_TASK=False
        print(content)
        if Config.FAKE_VALUES:
            FakeValues.OUTPUT=content
        else:
            opsu.set_output(content)   
        time.sleep(0.15)
        Config.STORAGE_TASK=True
        #opsu.close()
        return get_last_values()
    except Exception as e:
        logging.error(f"Error ({e}", exc_info=True)
        