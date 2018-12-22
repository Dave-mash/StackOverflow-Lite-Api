import os
from flask import Flask, Blueprint
from instance.config import app_config
from .API.v1.views.user_views import version1 as v1

def create_app(config_name):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    # app.config.from_object(app_config[config_name])
    
    app.register_blueprint(v1)

    return app

