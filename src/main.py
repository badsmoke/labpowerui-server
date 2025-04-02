import orjson as json
from flask import Flask
import importlib
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from api import fake_psu_values, get_psu_values, set_psu_output,set_psu_values, storage_config,utility,swagger,errors
from config.config import Config

from tasks.background_tasks import start_background_task

app = Flask(__name__)
CORS(app)


#swagger
SWAGGER_URL = "/api/docs"
API_URL = "/swagger.yaml"  
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


app.config.from_object(Config)


app.register_blueprint(fake_psu_values.bp)
app.register_blueprint(get_psu_values.bp)
app.register_blueprint(set_psu_output.bp)
app.register_blueprint(set_psu_values.bp)
app.register_blueprint(storage_config.bp)
app.register_blueprint(utility.bp)
app.register_blueprint(swagger.bp)
app.register_blueprint(errors.bp)



if __name__ == '__main__':
    print(importlib.metadata.version("flask"))
    start_background_task()
    app.run(debug=False,host='0.0.0.0',port="1234")
    #,ssl_context='adhoc'
    


