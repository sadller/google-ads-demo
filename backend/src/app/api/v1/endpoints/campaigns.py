from flask import jsonify, request
from marshmallow import ValidationError
from app.api.v1 import api_v1_bp
from app.core.extensions import db
from app.core.config import Config
from app.services.campaign_service import CampaignService
from app.schemas.campaign_schema import campaign_schema, campaigns_schema
import os


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


@api_v1_bp.route('/campaigns/<uuid:campaign_id>/publish', methods=['POST'])
def publish_campaign(campaign_id):
    try:
        customer_id = os.getenv('GOOGLE_ADS_CUSTOMER_ID')
        if not customer_id:
            return jsonify({'error': 'Google Ads customer ID not configured'}), 500
        
        campaign = CampaignService.publish_campaign(str(campaign_id), customer_id)
        
        return jsonify({
            'message': 'Campaign published successfully',
            'campaign': campaign_schema.dump(campaign)
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_v1_bp.route('/campaigns/<uuid:campaign_id>/enable', methods=['PUT'])
def enable_campaign(campaign_id):
    try:
        customer_id = os.getenv('GOOGLE_ADS_CUSTOMER_ID')
        if not customer_id:
            return jsonify({'error': 'Google Ads customer ID not configured'}), 500
        
        campaign = CampaignService.enable_campaign(str(campaign_id), customer_id)
        
        return jsonify({
            'message': 'Campaign enabled successfully',
            'campaign': campaign_schema.dump(campaign)
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_v1_bp.route('/campaigns/<uuid:campaign_id>/pause', methods=['PUT'])
def pause_campaign(campaign_id):
    try:
        customer_id = os.getenv('GOOGLE_ADS_CUSTOMER_ID')
        if not customer_id:
            return jsonify({'error': 'Google Ads customer ID not configured'}), 500
        
        campaign = CampaignService.pause_campaign(str(campaign_id), customer_id)
        
        return jsonify({
            'message': 'Campaign paused successfully',
            'campaign': campaign_schema.dump(campaign)
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
