import os
from os.path import join, dirname
from dotenv import load_dotenv
from app import create_app

# load dotenv in the base root
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

config_name = os.getenv('APP_SETTINGS')
secret = os.getenv('SECRET')
app = create_app(config_name)

if __name__ == "__main__":
    app.run()
