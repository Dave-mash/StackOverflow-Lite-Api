import os
from flask import Flask
from instance.config import app_config
from .API.v1.views.user_views import version1 as user_v1    
from .API.v1.views.questions_views import version1 as questions_v1    

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    
    app.register_blueprint(user_v1)
    app.register_blueprint(questions_v1)

    return app

