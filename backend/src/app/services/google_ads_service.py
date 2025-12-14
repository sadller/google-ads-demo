import uuid
from google.ads.googleads.errors import GoogleAdsException
from app.utils.google_ads_client import google_ads_client
from app.models.campaign import Campaign


class GoogleAdsService:
    @staticmethod
    def publish_campaign(campaign: Campaign, customer_id: str) -> str:
        try:
            client = google_ads_client.client
            campaign_service = client.get_service("CampaignService")
            campaign_budget_service = client.get_service("CampaignBudgetService")
            
            # Step 1: Create budget first (with unique name)
            budget_operation = client.get_type("CampaignBudgetOperation")
            budget = budget_operation.create
            budget.name = f"Budget {campaign.name} {uuid.uuid4()}"
            budget.amount_micros = campaign.daily_budget
            budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
            
            budget_response = campaign_budget_service.mutate_campaign_budgets(
                customer_id=customer_id,
                operations=[budget_operation]
            )
            budget_resource_name = budget_response.results[0].resource_name
            
            # Step 2: Create campaign with all required fields
            campaign_operation = client.get_type("CampaignOperation")
            google_campaign = campaign_operation.create
            google_campaign.name = campaign.name
            google_campaign.campaign_budget = budget_resource_name
            
            # IMPORTANT: Create as PAUSED to avoid charges (per assignment requirement)
            google_campaign.status = client.enums.CampaignStatusEnum.PAUSED
            
            # Campaign type - SEARCH
            google_campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
            
            # Bidding strategy - Manual CPC (must be set before network settings)
            google_campaign.manual_cpc = client.get_type("ManualCpc")
            
            # Network settings for SEARCH campaigns
            google_campaign.network_settings.target_google_search = True
            google_campaign.network_settings.target_search_network = True
            google_campaign.network_settings.target_partner_search_network = False
            # Enable Display Expansion on Search campaigns
            google_campaign.network_settings.target_content_network = True
            
            # EU political advertising declaration (required field)
            google_campaign.contains_eu_political_advertising = (
                client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
            )
            
            # Dates
            google_campaign.start_date = campaign.start_date.strftime("%Y%m%d")
            if campaign.end_date:
                google_campaign.end_date = campaign.end_date.strftime("%Y%m%d")
            
            campaign_response = campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_operation]
            )
            
            campaign_resource_name = campaign_response.results[0].resource_name
            campaign_id = campaign_resource_name.split('/')[-1]
            
            return campaign_id
            
        except GoogleAdsException as ex:
            error_msg = f"Google Ads API error: {ex.error.code().name}"
            if ex.failure and ex.failure.errors:
                error_msg += f" - {ex.failure.errors[0].message}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Failed to publish campaign: {str(e)}")
    
    @staticmethod
    def enable_campaign(google_campaign_id: str, customer_id: str) -> None:
        """Enable a Google Ads campaign (set to ENABLED status - billing will be active!)"""
        try:
            client = google_ads_client.client
            campaign_service = client.get_service("CampaignService")
            
            # Build resource name
            resource_name = f"customers/{customer_id}/campaigns/{google_campaign_id}"
            
            campaign_operation = client.get_type("CampaignOperation")
            campaign = campaign_operation.update
            campaign.resource_name = resource_name
            campaign.status = client.enums.CampaignStatusEnum.ENABLED
            
            campaign_operation.update_mask.paths.append("status")
            
            response = campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_operation]
            )
            
            # Verify the update was applied
            if not response.results:
                raise Exception("No results returned from Google Ads API")
            
        except GoogleAdsException as ex:
            error_msg = f"Google Ads API error: {ex.error.code().name}"
            if ex.failure and ex.failure.errors:
                error_msg += f" - {ex.failure.errors[0].message}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Failed to enable campaign: {str(e)}")
    
    @staticmethod
    def pause_campaign(google_campaign_id: str, customer_id: str) -> None:
        """Pause a Google Ads campaign (set to PAUSED status)"""
        try:
            client = google_ads_client.client
            campaign_service = client.get_service("CampaignService")
            
            # Build resource name
            resource_name = f"customers/{customer_id}/campaigns/{google_campaign_id}"
            
            campaign_operation = client.get_type("CampaignOperation")
            campaign = campaign_operation.update
            campaign.resource_name = resource_name
            campaign.status = client.enums.CampaignStatusEnum.PAUSED
            
            campaign_operation.update_mask.paths.append("status")
            
            response = campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_operation]
            )
            
            # Verify the update was applied
            if not response.results:
                raise Exception("No results returned from Google Ads API")
            
        except GoogleAdsException as ex:
            error_msg = f"Google Ads API error: {ex.error.code().name}"
            if ex.failure and ex.failure.errors:
                error_msg += f" - {ex.failure.errors[0].message}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Failed to pause campaign: {str(e)}")
