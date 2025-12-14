import { useState, type FormEvent } from 'react';
import type { CreateCampaignRequest } from '../types/campaign';
import { CAMPAIGN_OBJECTIVES, CAMPAIGN_TYPES, MINIMUM_BUDGET } from '../lib/constants';
import { campaignService } from '../services/campaignService';

interface CampaignModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  onError: (message: string) => void;
}

const INITIAL_FORM_DATA: CreateCampaignRequest = {
  name: '',
  objective: 'Sales',
  campaign_type: 'Demand Gen',
  daily_budget: 5000000,
  start_date: '',
  end_date: '',
  ad_group_name: '',
  ad_headline: '',
  ad_description: '',
  final_url: '',
  asset_url: ''
};

export default function CampaignModal({ isOpen, onClose, onSuccess, onError }: CampaignModalProps) {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<CreateCampaignRequest>(INITIAL_FORM_DATA);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const submitData = { ...formData };
      if (!submitData.end_date) delete submitData.end_date;
      if (!submitData.asset_url) delete submitData.asset_url;

      await campaignService.createCampaign(submitData);
      
      setFormData(INITIAL_FORM_DATA);
      onSuccess();
      onClose();
    } catch (err) {
      onError(err instanceof Error ? err.message : 'Failed to create campaign');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create New Campaign</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        <div className="modal-body">
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Campaign Name *</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Summer Sale 2025"
                />
              </div>

              <div className="form-group">
                <label>Objective *</label>
                <select
                  required
                  value={formData.objective}
                  onChange={(e) => setFormData({ ...formData, objective: e.target.value })}
                >
                  {CAMPAIGN_OBJECTIVES.map(obj => (
                    <option key={obj} value={obj}>{obj}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Campaign Type *</label>
                <select
                  required
                  value={formData.campaign_type}
                  onChange={(e) => setFormData({ ...formData, campaign_type: e.target.value })}
                >
                  {CAMPAIGN_TYPES.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Daily Budget (micros) *</label>
                <input
                  type="number"
                  required
                  min={MINIMUM_BUDGET}
                  value={formData.daily_budget}
                  onChange={(e) => setFormData({ ...formData, daily_budget: parseInt(e.target.value) })}
                  placeholder="5000000"
                />
                <small>${(formData.daily_budget / 1000000).toFixed(2)}</small>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Start Date *</label>
                <input
                  type="date"
                  required
                  value={formData.start_date}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>End Date</label>
                <input
                  type="date"
                  value={formData.end_date}
                  onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Ad Group Name *</label>
              <input
                type="text"
                required
                value={formData.ad_group_name}
                onChange={(e) => setFormData({ ...formData, ad_group_name: e.target.value })}
                placeholder="Main Ad Group"
              />
            </div>

            <div className="form-group">
              <label>Ad Headline *</label>
              <input
                type="text"
                required
                maxLength={255}
                value={formData.ad_headline}
                onChange={(e) => setFormData({ ...formData, ad_headline: e.target.value })}
                placeholder="Get 50% Off Today!"
              />
            </div>

            <div className="form-group">
              <label>Ad Description *</label>
              <textarea
                required
                maxLength={500}
                value={formData.ad_description}
                onChange={(e) => setFormData({ ...formData, ad_description: e.target.value })}
                placeholder="Limited time offer on all products..."
                rows={3}
              />
            </div>

            <div className="form-group">
              <label>Landing Page URL *</label>
              <input
                type="url"
                required
                value={formData.final_url}
                onChange={(e) => setFormData({ ...formData, final_url: e.target.value })}
                placeholder="https://example.com/sale"
              />
            </div>

            <div className="form-group">
              <label>Asset URL (Image/Video)</label>
              <input
                type="url"
                value={formData.asset_url}
                onChange={(e) => setFormData({ ...formData, asset_url: e.target.value })}
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div className="modal-footer">
              <button type="button" onClick={onClose} className="btn-secondary">
                Cancel
              </button>
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? 'Creating...' : 'Create Campaign'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
