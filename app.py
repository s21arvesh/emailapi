from flask import Flask, request, current_app as app, render_template, g
import logging
import os
import FlaskServiceImpl
from src.modules.database import MYSQLDatabaseCon
from src.modules.json_schema_validator import cls_json_schema_validator

logging.basicConfig(filename="log/flask_logs.log", format="%(asctime)s { %(filename)s [ %(funcName)s : %(lineno)d] } "
                                                          "%(levelname)s : %(message)s ")

app = Flask(__name__)

cors_config = {
    "origins": '*'
}

envType = os.environ.get('FLASK_ENV')
app.logger.info(f'Loaded Environment : {envType}')

if envType.islower() == "production":
    app.config.from_object('config.ProductionConfig')
    app.logger.setLevel('INFO')

if envType.islower() == "testing":
    app.config.from_object('config.TestingConfig')
    app.logger.setLevel('DEBUG')

else:
    app.config.from_object('config.DevelopmentConfig')
    app.logger.setLevel('DEBUG')

JSONschemavalidator = cls_json_schema_validator()


@app.route("/", methods=['GET'])
def home():
    return {'message': 'WELCOME TO FLASK, HOME PAGE STARTS HERE'}


@app.route("/send_email", methods=['GET'])
@JSONschemavalidator.validate_json(schema='send_email')
def send_email():
    resp = FlaskServiceImpl.fn_send_email(request.json)
    return resp


@app.route("/frontend_form", methods=['GET'])
def frontend_form():
    return render_template('index.html')


# @app.before_request
# def before_request_func():
#     MYSQLDatabaseCon.get_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
