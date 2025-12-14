export const API_BASE_URL = 'http://localhost:8000/api/v1';

export const CAMPAIGN_OBJECTIVES = [
  'Sales',
  'Leads',
  'Website Traffic',
  'Brand Awareness'
];

export const CAMPAIGN_TYPES = [
  'Demand Gen',
  'Search',
  'Display',
  'Video',
  'Shopping'
];

export const CAMPAIGN_STATUS = {
  DRAFT: 'DRAFT',
  PUBLISHED: 'PUBLISHED',  // Published to Google Ads but paused
  ENABLED: 'ENABLED',      // Active in Google Ads (billing active)
  PAUSED: 'PAUSED'         // Paused in Google Ads
} as const;

export type CampaignStatusType = typeof CAMPAIGN_STATUS[keyof typeof CAMPAIGN_STATUS];

export const MINIMUM_BUDGET = 1000000; // $1 in micros
