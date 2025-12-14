import type { Campaign, CreateCampaignRequest } from '../types/campaign';
import { API_BASE_URL } from '../lib/constants';
import { formatApiError } from '../lib/apiErrors';

async function handleResponse(response: Response) {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(formatApiError(errorData));
  }
  return response.json();
}

export const campaignService = {
  async getAllCampaigns(): Promise<Campaign[]> {
    const response = await fetch(`${API_BASE_URL}/campaigns`);
    const data = await handleResponse(response);
    return data.campaigns;
  },

  async getCampaignById(id: string): Promise<Campaign> {
    const response = await fetch(`${API_BASE_URL}/campaigns/${id}`);
    return handleResponse(response);
  },

  async createCampaign(data: CreateCampaignRequest): Promise<Campaign> {
    const response = await fetch(`${API_BASE_URL}/campaigns`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await handleResponse(response);
    return result.campaign;
  },

  async publishCampaign(id: string): Promise<Campaign> {
    const response = await fetch(`${API_BASE_URL}/campaigns/${id}/publish`, {
      method: 'POST'
    });
    const result = await handleResponse(response);
    return result.campaign;
  },

  async enableCampaign(id: string): Promise<Campaign> {
    const response = await fetch(`${API_BASE_URL}/campaigns/${id}/enable`, {
      method: 'PUT'
    });
    const result = await handleResponse(response);
    return result.campaign;
  },

  async pauseCampaign(id: string): Promise<Campaign> {
    const response = await fetch(`${API_BASE_URL}/campaigns/${id}/pause`, {
      method: 'PUT'
    });
    const result = await handleResponse(response);
    return result.campaign;
  }
};
