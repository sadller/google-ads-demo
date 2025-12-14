class CampaignStatus:
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    ENABLED = 'ENABLED'
    PAUSED = 'PAUSED'
    
    @classmethod
    def all(cls):
        return [cls.DRAFT, cls.PUBLISHED, cls.ENABLED, cls.PAUSED]
