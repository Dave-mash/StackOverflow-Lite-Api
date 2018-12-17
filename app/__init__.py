import os
from flask import Flask, Blueprint
from instance.config import app_config
from app.API.v1 import version1 as v1

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(v1)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app
