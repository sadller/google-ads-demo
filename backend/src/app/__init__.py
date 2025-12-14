from flask import Flask
from app.core import Config, init_app
from app.utils import register_error_handlers, setup_logger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    setup_logger(app)
    init_app(app)
    register_error_handlers(app)
    
    from app import models
    from app.api import api_v1_bp
    app.register_blueprint(api_v1_bp)
    
    return app
