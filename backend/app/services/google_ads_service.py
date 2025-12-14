import uuid
import requests
from google.ads.googleads.errors import GoogleAdsException
from app.utils.google_ads_client import google_ads_client
from app.models import Campaign


class PublishResult:
    def __init__(self, campaign_id: str):
        self.campaign_id = campaign_id
        self.asset_resource_name: str = None
        self.warnings: list[str] = []
    
    def add_warning(self, warning: str):
        self.warnings.append(warning)


class GoogleAdsService:
    @staticmethod
    def create_image_asset(customer_id: str, asset_url: str, asset_name: str) -> str:
        client = google_ads_client.client
        asset_service = client.get_service("AssetService")
        
        response = requests.get(asset_url, timeout=30)
        response.raise_for_status()
        image_data = response.content
        
        content_type = response.headers.get('Content-Type', '').lower()
        
        asset_operation = client.get_type("AssetOperation")
        asset = asset_operation.create
        asset.name = asset_name[:255]
        asset.type_ = client.enums.AssetTypeEnum.IMAGE
        asset.image_asset.data = image_data
        asset.image_asset.file_size = len(image_data)
        
        if 'png' in content_type:
            asset.image_asset.mime_type = client.enums.MimeTypeEnum.IMAGE_PNG
        elif 'gif' in content_type:
            asset.image_asset.mime_type = client.enums.MimeTypeEnum.IMAGE_GIF
        else:
            asset.image_asset.mime_type = client.enums.MimeTypeEnum.IMAGE_JPEG
        
        asset_response = asset_service.mutate_assets(
            customer_id=customer_id,
            operations=[asset_operation]
        )
        
        return asset_response.results[0].resource_name
    
    @staticmethod
    def _create_budget(client, customer_id: str, campaign_name: str, daily_budget: int) -> str:
        budget_service = client.get_service("CampaignBudgetService")
        
        budget_operation = client.get_type("CampaignBudgetOperation")
        budget = budget_operation.create
        budget.name = f"Budget {campaign_name} {uuid.uuid4()}"
        budget.amount_micros = daily_budget
        budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
        
        response = budget_service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[budget_operation]
        )
        return response.results[0].resource_name
    
    @staticmethod
    def _create_google_campaign(client, customer_id: str, campaign: Campaign, budget_resource_name: str) -> str:
        campaign_service = client.get_service("CampaignService")
        
        campaign_operation = client.get_type("CampaignOperation")
        google_campaign = campaign_operation.create
        google_campaign.name = campaign.name
        google_campaign.campaign_budget = budget_resource_name
        google_campaign.status = client.enums.CampaignStatusEnum.PAUSED
        google_campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
        google_campaign.manual_cpc = client.get_type("ManualCpc")
        
        google_campaign.network_settings.target_google_search = True
        google_campaign.network_settings.target_search_network = True
        google_campaign.network_settings.target_partner_search_network = False
        google_campaign.network_settings.target_content_network = True
        
        google_campaign.contains_eu_political_advertising = (
            client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
        )
        
        google_campaign.start_date = campaign.start_date.strftime("%Y%m%d")
        if campaign.end_date:
            google_campaign.end_date = campaign.end_date.strftime("%Y%m%d")
        
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation]
        )
        return response.results[0].resource_name
    
    @staticmethod
    def _create_ad_group_with_ad(client, customer_id: str, campaign: Campaign, campaign_resource_name: str, result: PublishResult):
        ad_group_service = client.get_service("AdGroupService")
        ad_group_ad_service = client.get_service("AdGroupAdService")
        
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
        
        ad_group_ad_operation = client.get_type("AdGroupAdOperation")
        ad_group_ad = ad_group_ad_operation.create
        ad_group_ad.ad_group = ad_group_resource_name
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        ad = ad_group_ad.ad
        ad.final_urls.append(campaign.final_url)
        
        headlines_text = [
            (campaign.ad_headline[:30] if campaign.ad_headline else campaign.name[:30]),
            f"{campaign.name[:20]} - Learn More",
            f"Discover {campaign.name[:20]}"
        ]
        for text in headlines_text:
            headline = client.get_type("AdTextAsset")
            headline.text = text[:30]
            ad.responsive_search_ad.headlines.append(headline)
        
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
    
    @staticmethod
    def publish_campaign(campaign: Campaign, customer_id: str) -> PublishResult:
        try:
            client = google_ads_client.client
            
            asset_resource_name = None
            asset_warning = None
            if campaign.asset_url:
                try:
                    asset_name = f"Asset {campaign.name} {uuid.uuid4()}"
                    asset_resource_name = GoogleAdsService.create_image_asset(
                        customer_id, campaign.asset_url, asset_name
                    )
                except Exception as asset_error:
                    asset_warning = f"Asset creation failed: {str(asset_error)}"
            
            budget_resource_name = GoogleAdsService._create_budget(
                client, customer_id, campaign.name, campaign.daily_budget
            )
            
            campaign_resource_name = GoogleAdsService._create_google_campaign(
                client, customer_id, campaign, budget_resource_name
            )
            
            campaign_id = campaign_resource_name.split('/')[-1]
            result = PublishResult(campaign_id)
            
            if asset_resource_name:
                result.asset_resource_name = asset_resource_name
            elif asset_warning:
                result.add_warning(asset_warning)
            
            try:
                GoogleAdsService._create_ad_group_with_ad(
                    client, customer_id, campaign, campaign_resource_name, result
                )
            except Exception as ad_error:
                result.add_warning(f"Ad Group/Ad creation failed: {str(ad_error)}")
            
            return result
            
        except GoogleAdsException as ex:
            error_msg = f"Google Ads API error: {ex.error.code().name}"
            if ex.failure and ex.failure.errors:
                error_msg += f" - {ex.failure.errors[0].message}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Failed to publish campaign: {str(e)}")
    
    @staticmethod
    def _update_campaign_status(google_campaign_id: str, customer_id: str, status) -> None:
        client = google_ads_client.client
        campaign_service = client.get_service("CampaignService")
        
        resource_name = f"customers/{customer_id}/campaigns/{google_campaign_id}"
        
        campaign_operation = client.get_type("CampaignOperation")
        campaign = campaign_operation.update
        campaign.resource_name = resource_name
        campaign.status = status
        campaign_operation.update_mask.paths.append("status")
        
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation]
        )
        
        if not response.results:
            raise Exception("No results returned from Google Ads API")
    
    @staticmethod
    def enable_campaign(google_campaign_id: str, customer_id: str) -> None:
        try:
            client = google_ads_client.client
            GoogleAdsService._update_campaign_status(
                google_campaign_id, 
                customer_id, 
                client.enums.CampaignStatusEnum.ENABLED
            )
        except GoogleAdsException as ex:
            error_msg = f"Google Ads API error: {ex.error.code().name}"
            if ex.failure and ex.failure.errors:
                error_msg += f" - {ex.failure.errors[0].message}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Failed to enable campaign: {str(e)}")
    
    @staticmethod
    def pause_campaign(google_campaign_id: str, customer_id: str) -> None:
        try:
            client = google_ads_client.client
            GoogleAdsService._update_campaign_status(
                google_campaign_id, 
                customer_id, 
                client.enums.CampaignStatusEnum.PAUSED
            )
        except GoogleAdsException as ex:
            error_msg = f"Google Ads API error: {ex.error.code().name}"
            if ex.failure and ex.failure.errors:
                error_msg += f" - {ex.failure.errors[0].message}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Failed to pause campaign: {str(e)}")
