from flask import Flask, send_file, Blueprint, jsonify

bp = Blueprint('swagger', __name__)


@bp.route("/swagger.yaml")
def swagger_yaml():
    return send_file("/usr/src/app/swagger.yaml", mimetype="text/yaml")