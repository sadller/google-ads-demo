import { useEffect, useState, useMemo } from 'react';
import type { Campaign } from '../types/campaign';
import { campaignService } from '../services/campaignService';
import { CAMPAIGN_STATUS } from '../lib/constants';

interface CampaignListProps {
  refresh: number;
  onError: (message: string) => void;
  onSuccess: (message: string) => void;
}

export default function CampaignList({ refresh, onError, onSuccess }: CampaignListProps) {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  useEffect(() => {
    loadCampaigns();
  }, [refresh]);

  const loadCampaigns = async () => {
    try {
      setLoading(true);
      const data = await campaignService.getAllCampaigns();
      setCampaigns(data);
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Failed to load campaigns');
    } finally {
      setLoading(false);
    }
  };

  const handlePublish = async (campaignId: string) => {
    try {
      setActionLoading(campaignId);
      const updatedCampaign = await campaignService.publishCampaign(campaignId);
      setCampaigns(prev => prev.map(c => c.id === campaignId ? updatedCampaign : c));
      onSuccess('Campaign published to Google Ads successfully!');
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Failed to publish campaign');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDisable = async (campaignId: string) => {
    try {
      setActionLoading(campaignId);
      const updatedCampaign = await campaignService.pauseCampaign(campaignId);
      setCampaigns(prev => prev.map(c => c.id === campaignId ? updatedCampaign : c));
      onSuccess('Campaign disabled successfully!');
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Failed to disable campaign');
    } finally {
      setActionLoading(null);
    }
  };

  const filteredCampaigns = useMemo(() => 
    filter ? campaigns.filter(c => c.status === filter) : campaigns,
    [campaigns, filter]
  );

  const statusCounts = useMemo(() => ({
    draft: campaigns.filter(c => c.status === CAMPAIGN_STATUS.DRAFT).length,
    published: campaigns.filter(c => c.status === CAMPAIGN_STATUS.PUBLISHED).length,
    enabled: campaigns.filter(c => c.status === CAMPAIGN_STATUS.ENABLED).length,
    disabled: campaigns.filter(c => c.status === CAMPAIGN_STATUS.PAUSED).length
  }), [campaigns]);

  const handleEnable = async (campaignId: string) => {
    try {
      setActionLoading(campaignId);
      const updatedCampaign = await campaignService.enableCampaign(campaignId);
      setCampaigns(prev => prev.map(c => c.id === campaignId ? updatedCampaign : c));
      onSuccess('Campaign enabled successfully! Billing is now active.');
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Failed to enable campaign');
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusText = (status: string) => {
    const colors: Record<string, string> = {
      DRAFT: '#6b7280',
      PUBLISHED: '#3b82f6',
      ENABLED: '#10b981',
      PAUSED: '#dc2626'
    };
    const labels: Record<string, string> = {
      DRAFT: 'Draft',
      PUBLISHED: 'Published',
      ENABLED: 'Enabled',
      PAUSED: 'Disabled'
    };
    return (
      <span style={{ color: colors[status], fontWeight: 600 }}>
        {labels[status] || status}
      </span>
    );
  };

  if (loading) return <div className="loading">Loading campaigns...</div>;

  return (
    <div className="campaign-list">
      <div className="list-header">
        <h2>Campaigns ({filteredCampaigns.length})</h2>
        <div className="filter-group">
          <label>Filter:</label>
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="">All ({campaigns.length})</option>
            <option value={CAMPAIGN_STATUS.DRAFT}>Draft ({statusCounts.draft})</option>
            <option value={CAMPAIGN_STATUS.PUBLISHED}>Published ({statusCounts.published})</option>
            <option value={CAMPAIGN_STATUS.ENABLED}>Enabled ({statusCounts.enabled})</option>
            <option value={CAMPAIGN_STATUS.PAUSED}>Disabled ({statusCounts.disabled})</option>
          </select>
        </div>
      </div>

      {filteredCampaigns.length === 0 ? (
        <div className="empty-state">
          <p>
            {campaigns.length === 0 
              ? 'No campaigns found. Click "Create Campaign" to get started!' 
              : `No ${filter.toLowerCase()} campaigns found.`}
          </p>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Status</th>
                <th>Google Campaign ID</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredCampaigns.map((campaign) => (
                <tr key={campaign.id}>
                  <td>{campaign.name}</td>
                  <td>{getStatusText(campaign.status)}</td>
                  <td>
                    {campaign.google_campaign_id || (
                      <span className="text-muted">-</span>
                    )}
                  </td>
                  <td>
                    {campaign.status === 'DRAFT' && (
                      <button 
                        className="btn-small btn-success" 
                        onClick={() => handlePublish(campaign.id)}
                        disabled={actionLoading === campaign.id}
                      >
                        {actionLoading === campaign.id ? 'Publishing...' : 'Publish'}
                      </button>
                    )}
                    {(campaign.status === 'PUBLISHED' || campaign.status === 'PAUSED') && (
                      <button 
                        className="btn-small btn-primary"
                        onClick={() => handleEnable(campaign.id)}
                        disabled={actionLoading === campaign.id}
                      >
                        {actionLoading === campaign.id ? 'Enabling...' : 'Enable'}
                      </button>
                    )}
                    {campaign.status === 'ENABLED' && (
                      <button 
                        className="btn-small btn-danger"
                        onClick={() => handleDisable(campaign.id)}
                        disabled={actionLoading === campaign.id}
                      >
                        {actionLoading === campaign.id ? 'Disabling...' : 'Disable'}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
