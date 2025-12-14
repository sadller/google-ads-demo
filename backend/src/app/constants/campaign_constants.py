"""Campaign Constants"""

# Campaign Status
class CampaignStatus:
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    PAUSED = 'PAUSED'
    
    @classmethod
    def all(cls):
        return [cls.DRAFT, cls.PUBLISHED, cls.PAUSED]


# Campaign Objectives
class CampaignObjective:
    SALES = 'Sales'
    LEADS = 'Leads'
    WEBSITE_TRAFFIC = 'Website Traffic'
    BRAND_AWARENESS = 'Brand Awareness'


# Campaign Types
class CampaignType:
    DEMAND_GEN = 'Demand Gen'
    SEARCH = 'Search'
    DISPLAY = 'Display'
    VIDEO = 'Video'
    SHOPPING = 'Shopping'


# Budget Constants (in micros)
class BudgetConstants:
    MINIMUM_DAILY_BUDGET = 1_000_000  # $1 in micros
    MICRO_TO_DOLLAR = 1_000_000
