from flask import Blueprint, jsonify, request
import random
from datetime import datetime
from config.config import Config,logging
from api.errors import error_response

bp = Blueprint('fake_psu_values', __name__)

class FakeValues:
    #set fake values
    IDENTITY = "fake psu"
    OUTPUT = True
    SET_VOLTAGE_LIMIT = 30
    SET_CURRENT_LIMIT = 8
    SET_VOLTAGE = 19
    SET_CURRENT = 5
    VOLTAGE = (random.randint(SET_VOLTAGE-15,SET_VOLTAGE+15))/10
    CURRENT = (random.randint(SET_CURRENT-5,SET_CURRENT+5))/10




@bp.route('/api/get/fakevalues', methods=['GET'])
def get_fake_values_route():
    response = jsonify(get_fake_values())
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response

@bp.route('/api/set/fake', methods=['POST'])
def set_fake_values_route():
    content = request.json
    if Config.LOGGING:
        print(content)
    if not isinstance(content["fake"], bool):
        #config.py default values as class
        #example error message
        return error_response("Invalid value", 400, {"fake": "Value must be bool"})
    Config.FAKE_VALUES=content["fake"]
    response = jsonify({"status":"success"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response


def get_fake_values():
    try:
        identity = FakeValues.IDENTITY
        voltage = FakeValues.VOLTAGE
        current = FakeValues.CURRENT
        get_voltage = FakeValues.SET_VOLTAGE
        get_current = FakeValues.SET_CURRENT
        get_voltage_limit = FakeValues.SET_VOLTAGE_LIMIT
        get_current_limit = FakeValues.SET_CURRENT_LIMIT
        output_status = FakeValues.OUTPUT
        power = round((voltage * current),3)

        values = {
                "status": "success",
                "code": 200,
                "message": "Power supply data retrieved successfully",
                "time": datetime.now().strftime("%M:%S:%f"),
                "device": identity,
                "data": { 
                    "readingVoltage": voltage, 
                    "readingCurrent": current,
                    "voltage": get_voltage, 
                    "current": get_current,
                    "voltageLimit": get_voltage_limit, 
                    "currentLimit": get_current_limit,
                    "power": power,
                    "output_status" : output_status,
                    
                }
            }
        if Config.LOGGING:
            print(values)
        return values
    except Exception as e:
        logging.error(f"Error ({e}", exc_info=True)
        