from flask import Blueprint, jsonify
from datetime import datetime
from config.config import Config,logging


bp = Blueprint('errors', __name__)


def error_response(message, code=400, errors=None):
    """
    Returns a standardized error response.
    :param message: The error message to be returned.
    :param code: The HTTP status code.
    :param errors: Optional dictionary containing specific errors.
    :return: JSON response in error format.
    """
    response = {
        "status": "error",
        "code": code,
        "message": message,
        "timestamp": datetime.now().strftime("%M:%S:%f"),
        "errors": errors if errors else {}
    }
    logging.error(f"Error response: {response}") 
    return jsonify(response), code