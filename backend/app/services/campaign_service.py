from typing import List, Optional, Tuple
from app.core.extensions import db
from app.models import Campaign
from app.schemas import campaign_schema
from app.constants import CampaignStatus
from app.services.google_ads_service import GoogleAdsService


class CampaignService:
    @staticmethod
    def create_campaign(data: dict) -> Campaign:
        validated_data = campaign_schema.load(data)
        campaign = Campaign(**validated_data, status=CampaignStatus.DRAFT)
        
        db.session.add(campaign)
        db.session.commit()
        
        return campaign
    
    @staticmethod
    def get_all_campaigns(status: Optional[str] = None) -> List[Campaign]:
        query = Campaign.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Campaign.created_at.desc()).all()
    
    @staticmethod
    def get_campaign_by_id(campaign_id: str) -> Optional[Campaign]:
        return Campaign.query.get(campaign_id)
    
    @staticmethod
    def publish_campaign(campaign_id: str, customer_id: str) -> Tuple[Campaign, List[str]]:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            raise ValueError('Campaign not found')
        
        if campaign.status == CampaignStatus.PUBLISHED:
            raise ValueError('Campaign already published')
        
        result = GoogleAdsService.publish_campaign(campaign, customer_id)
        
        campaign.google_campaign_id = result.campaign_id
        campaign.status = CampaignStatus.PUBLISHED
        db.session.commit()
        
        return campaign, result.warnings
    
    @staticmethod
    def enable_campaign(campaign_id: str, customer_id: str) -> Campaign:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            raise ValueError('Campaign not found')
        
        if not campaign.google_campaign_id:
            raise ValueError('Campaign not published to Google Ads')
        
        if campaign.status == CampaignStatus.ENABLED:
            raise ValueError('Campaign already enabled')
        
        GoogleAdsService.enable_campaign(campaign.google_campaign_id, customer_id)
        
        campaign.status = CampaignStatus.ENABLED
        db.session.commit()
        
        return campaign
    
    @staticmethod
    def pause_campaign(campaign_id: str, customer_id: str) -> Campaign:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            raise ValueError('Campaign not found')
        
        if not campaign.google_campaign_id:
            raise ValueError('Campaign not published to Google Ads')
        
        if campaign.status == CampaignStatus.PAUSED:
            raise ValueError('Campaign already paused')
        
        GoogleAdsService.pause_campaign(campaign.google_campaign_id, customer_id)
        
        campaign.status = CampaignStatus.PAUSED
        db.session.commit()
        
        return campaign
