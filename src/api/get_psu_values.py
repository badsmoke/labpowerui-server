from flask import Blueprint, jsonify, request
from datetime import datetime
from config.config import Config,logging


bp = Blueprint('get_psu_values', __name__)


@bp.route('/api/get/values', methods=['GET'])
def get_values_route():
    response = jsonify(get_values())
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response



def get_values():

    opsu=Config.USB_DEVICE_OBJECT

    try:
        
        if Config.LOGGING:
            print("opsu oject: ",opsu)
            print("opsu type: ",type(opsu))
        identity = opsu.read_identity()
        voltage = round(opsu.measure_voltage(),3)
        current = round(opsu.measure_current(),3)
        get_voltage = opsu.get_voltage()
        get_current = opsu.get_current()
        get_voltage_limit = opsu.get_voltage_limit()
        get_current_limit = opsu.get_current_limit()
        output_status = opsu.get_output()
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
                "time": datetime.now().strftime("%M:%S:%f")
            }
        }
        if Config.LOGGING:
            print(values)
        return values
    except Exception as e:
        logging.error(f"Error ({e}", exc_info=True)
        
        #opsu.close()