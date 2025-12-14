from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.extensions import db


class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    objective = db.Column(db.String(100), nullable=False)
    campaign_type = db.Column(db.String(100), nullable=False)
    daily_budget = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='DRAFT')
    ad_group_name = db.Column(db.String(255), nullable=False)
    ad_headline = db.Column(db.String(255), nullable=False)
    ad_description = db.Column(db.Text, nullable=False)
    final_url = db.Column(db.String(2048), nullable=False)
    asset_url = db.Column(db.String(2048), nullable=True)
    google_campaign_id = db.Column(db.String(255), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Campaign {self.name}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'objective': self.objective,
            'campaign_type': self.campaign_type,
            'daily_budget': self.daily_budget,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'ad_group_name': self.ad_group_name,
            'ad_headline': self.ad_headline,
            'ad_description': self.ad_description,
            'final_url': self.final_url,
            'asset_url': self.asset_url,
            'google_campaign_id': self.google_campaign_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
