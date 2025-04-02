from flask import Blueprint, jsonify, request
from config.config import Config,logging
from api.storage_config import get_last_values
from api.fake_psu_values import FakeValues

bp = Blueprint('set_psu_values', __name__)


opsu=Config.USB_DEVICE_OBJECT


def set_values(content):

    print(content)
    set_voltage = content["setValue"]["setVoltage"]
    set_current = content["setValue"]["setCurrent"]

    set_voltage_limit = content["setValue"]["setVoltageLimit"]
    set_current_limit = content["setValue"]["setCurrentLimit"]


    try:

        #stop task
        Config.STORAGE_TASK=False
        if Config.FAKE_VALUES:
            FakeValues.SET_VOLTAGE_LIMIT = set_voltage_limit
            FakeValues.SET_CURRENT_LIMIT = set_current_limit
            FakeValues.SET_VOLTAGE = set_voltage
            FakeValues.SET_CURRENT = set_current

        else:          
            opsu.set_voltage_limit(set_voltage_limit)
            opsu.set_current_limit(set_current_limit)
            opsu.set_voltage(set_voltage)
            opsu.set_current(set_current)


        #reenable task
        Config.STORAGE_TASK=True

        return get_last_values()

    except Exception as e:
        logging.error(f"Error ({e}", exc_info=True)
        
        #opsu.close()


@bp.route('/api/set/values', methods=['POST'])
def set_values_route():
    content = request.json
    if Config.LOGGING:
        print(content)
    response = jsonify(set_values(content))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response