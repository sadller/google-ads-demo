"""
Google Ads API Client Wrapper
"""
from google.ads.googleads.client import GoogleAdsClient
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class GoogleAdsClientWrapper:
    """Wrapper for Google Ads API client"""
    
    def __init__(self, config_path='google-ads.yaml'):
        self.config_path = config_path
        self._client = None
    
    @property
    def client(self):
        """Get Google Ads client (lazy load)"""
        if self._client is None:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Google Ads config not found: {self.config_path}")
            
            self._client = GoogleAdsClient.load_from_storage(str(config_file))
            logger.info("Google Ads client initialized")
        
        return self._client
    
    def get_service(self, service_name, version='v18'):
        """Get a Google Ads service"""
        return self.client.get_service(service_name, version=version)


# Global instance
google_ads_client = GoogleAdsClientWrapper()
