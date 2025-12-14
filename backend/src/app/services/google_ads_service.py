import uuid
from google.ads.googleads.errors import GoogleAdsException
from app.utils.google_ads_client import google_ads_client
from app.models.campaign import Campaign


class PublishResult:
    """Result of publishing a campaign to Google Ads"""
    def __init__(self, campaign_id: str):
        self.campaign_id = campaign_id
        self.warnings: list[str] = []
    
    def add_warning(self, warning: str):
        self.warnings.append(warning)


class GoogleAdsService:
    @staticmethod
    def publish_campaign(campaign: Campaign, customer_id: str) -> PublishResult:
        """
        Publish campaign to Google Ads. Creates:
        1. Campaign Budget
        2. Campaign
        3. Ad Group
        4. Responsive Search Ad
        
        Returns PublishResult with campaign_id and any warnings.
        """
        try:
            client = google_ads_client.client
            campaign_service = client.get_service("CampaignService")
            campaign_budget_service = client.get_service("CampaignBudgetService")
            ad_group_service = client.get_service("AdGroupService")
            ad_group_ad_service = client.get_service("AdGroupAdService")
            
            # ========== Step 1: Create Campaign Budget ==========
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
            
            # ========== Step 2: Create Campaign ==========
            campaign_operation = client.get_type("CampaignOperation")
            google_campaign = campaign_operation.create
            google_campaign.name = campaign.name
            google_campaign.campaign_budget = budget_resource_name
            
            # Create as PAUSED to avoid charges (per assignment requirement)
            google_campaign.status = client.enums.CampaignStatusEnum.PAUSED
            
            # Campaign type - SEARCH
            google_campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
            
            # Bidding strategy - Manual CPC
            google_campaign.manual_cpc = client.get_type("ManualCpc")
            
            # Network settings
            google_campaign.network_settings.target_google_search = True
            google_campaign.network_settings.target_search_network = True
            google_campaign.network_settings.target_partner_search_network = False
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
            
            # Campaign created successfully - extract ID now to ensure we can return it
            campaign_id = campaign_resource_name.split('/')[-1]
            result = PublishResult(campaign_id)
            
            # ========== Step 3: Create Ad Group (optional) ==========
            ad_group_resource_name = None
            try:
                ad_group_operation = client.get_type("AdGroupOperation")
                ad_group = ad_group_operation.create
                ad_group.name = campaign.ad_group_name or f"Ad Group - {campaign.name}"
                ad_group.campaign = campaign_resource_name
                ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
                ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
                ad_group.cpc_bid_micros = 1000000
                
                ad_group_response = ad_group_service.mutate_ad_groups(
                    customer_id=customer_id,
                    operations=[ad_group_operation]
                )
                ad_group_resource_name = ad_group_response.results[0].resource_name
            except Exception as ag_error:
                result.add_warning(f"Ad Group creation failed: {str(ag_error)}")
                # Continue - campaign is still created
            
            # ========== Step 4: Create Responsive Search Ad (optional) ==========
            # Only attempt if ad group was created successfully
            if ad_group_resource_name:
                try:
                    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
                    ad_group_ad = ad_group_ad_operation.create
                    ad_group_ad.ad_group = ad_group_resource_name
                    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
                    
                    # Set up Responsive Search Ad
                    ad = ad_group_ad.ad
                    ad.final_urls.append(campaign.final_url)
                    
                    # Add headlines (minimum 3 required for RSA, max 30 chars each)
                    headlines_text = [
                        (campaign.ad_headline[:30] if campaign.ad_headline else campaign.name[:30]),
                        f"{campaign.name[:20]} - Learn More",
                        f"Discover {campaign.name[:20]}"
                    ]
                    for text in headlines_text:
                        headline = client.get_type("AdTextAsset")
                        headline.text = text[:30]
                        ad.responsive_search_ad.headlines.append(headline)
                    
                    # Add descriptions (minimum 2 required for RSA, max 90 chars each)
                    descriptions_text = [
                        (campaign.ad_description[:90] if campaign.ad_description else f"Learn more about {campaign.name}."),
                        f"Visit our website to learn more about {campaign.name}."[:90]
                    ]
                    for text in descriptions_text:
                        description = client.get_type("AdTextAsset")
                        description.text = text[:90]
                        ad.responsive_search_ad.descriptions.append(description)
                    
                    ad_group_ad_service.mutate_ad_group_ads(
                        customer_id=customer_id,
                        operations=[ad_group_ad_operation]
                    )
                except Exception as ad_error:
                    # Log warning but don't fail - campaign and ad group are created
                    result.add_warning(f"Ad creation failed: {str(ad_error)}")
            
            # Return the result - campaign was created successfully
            return result
            
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
