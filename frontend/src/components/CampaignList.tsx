import { useEffect, useState, useMemo } from 'react';
import type { Campaign } from '../types/campaign';
import { campaignService } from '../services/campaignService';
import { CAMPAIGN_STATUS } from '../lib/constants';

interface CampaignListProps {
  refresh: number;
  onError: (message: string) => void;
}

export default function CampaignList({ refresh, onError }: CampaignListProps) {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

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

  const filteredCampaigns = useMemo(() => 
    filter ? campaigns.filter(c => c.status === filter) : campaigns,
    [campaigns, filter]
  );

  const statusCounts = useMemo(() => ({
    draft: campaigns.filter(c => c.status === CAMPAIGN_STATUS.DRAFT).length,
    published: campaigns.filter(c => c.status === CAMPAIGN_STATUS.PUBLISHED).length,
    paused: campaigns.filter(c => c.status === CAMPAIGN_STATUS.PAUSED).length
  }), [campaigns]);

  const getStatusBadge = (status: string) => {
    const colors = {
      DRAFT: '#6b7280',
      PUBLISHED: '#10b981',
      PAUSED: '#f59e0b'
    };
    return (
      <span 
        className="status-badge" 
        style={{ backgroundColor: colors[status as keyof typeof colors] }}
      >
        {status}
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
            <option value={CAMPAIGN_STATUS.PAUSED}>Paused ({statusCounts.paused})</option>
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
                <th>Type</th>
                <th>Objective</th>
                <th>Budget</th>
                <th>Start Date</th>
                <th>Status</th>
                <th>Google ID</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredCampaigns.map((campaign) => (
                <tr key={campaign.id}>
                  <td>
                    <strong>{campaign.name}</strong>
                    <br />
                    <small>{campaign.ad_headline}</small>
                  </td>
                  <td>{campaign.campaign_type}</td>
                  <td>{campaign.objective}</td>
                  <td>${(campaign.daily_budget / 1000000).toFixed(2)}/day</td>
                  <td>{new Date(campaign.start_date).toLocaleDateString()}</td>
                  <td>{getStatusBadge(campaign.status)}</td>
                  <td>
                    {campaign.google_campaign_id || (
                      <span className="text-muted">-</span>
                    )}
                  </td>
                  <td>
                    {campaign.status === 'DRAFT' && (
                      <button className="btn-small btn-success" disabled>
                        Publish
                      </button>
                    )}
                    {campaign.status === 'PUBLISHED' && (
                      <button className="btn-small btn-warning" disabled>
                        Pause
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
