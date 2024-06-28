from flask import Flask
from .routes import main

import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.secret_key = os.urandom(8)
    
    app.register_blueprint(main)

    return app
