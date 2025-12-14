from flask import jsonify
from app.api.v1 import api_v1_bp
from app.core import db


@api_v1_bp.route('/health')
def health_check():
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'ok',
        'database': db_status
    })


@api_v1_bp.route('/')
def api_info():
    return jsonify({
        'name': 'Pathik AI API',
        'version': '1.0.0',
        'endpoints': {
            'campaigns': '/api/v1/campaigns',
            'health': '/api/v1/health'
        }
    })
