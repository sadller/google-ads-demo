"""
Flask Application Factory
"""
from flask import Flask, jsonify
from app.core import Config, init_app
from app.utils import register_error_handlers, setup_logger


def create_app():
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup
    setup_logger(app)
    init_app(app)
    register_error_handlers(app)
    
    # Import models for Flask-Migrate
    from app import models
    
    # Register blueprints
    from app.api import api_v1_bp
    app.register_blueprint(api_v1_bp)
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Pathik AI Campaign Manager API',
            'version': '1.0.0',
            'health': '/health',
            'api': '/api/v1/'
        })
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})
    
    return app
