from flask import jsonify, request
from marshmallow import ValidationError
from app.api.v1 import api_v1_bp
from app.core.extensions import db
from app.services.campaign_service import CampaignService
from app.schemas.campaign_schema import campaign_schema, campaigns_schema


@api_v1_bp.route('/campaigns', methods=['POST'])
def create_campaign():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        campaign = CampaignService.create_campaign(data)
        
        return jsonify({
            'message': 'Campaign created successfully',
            'campaign': campaign_schema.dump(campaign)
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_v1_bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    try:
        status = request.args.get('status')
        campaigns = CampaignService.get_all_campaigns(status)
        
        return jsonify({
            'campaigns': campaigns_schema.dump(campaigns),
            'count': len(campaigns)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_v1_bp.route('/campaigns/<uuid:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    try:
        campaign = CampaignService.get_campaign_by_id(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404
        
        return jsonify(campaign_schema.dump(campaign)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
