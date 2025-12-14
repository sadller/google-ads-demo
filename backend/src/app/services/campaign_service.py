from typing import List, Optional
from app.core.extensions import db
from app.models.campaign import Campaign
from app.schemas.campaign_schema import campaign_schema
from app.constants import CampaignStatus


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
    def delete_campaign(campaign_id: str) -> bool:
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return False
        
        db.session.delete(campaign)
        db.session.commit()
        return True
