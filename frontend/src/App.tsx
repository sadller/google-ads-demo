import { useState } from 'react';
import CampaignModal from './components/CampaignModal';
import CampaignList from './components/CampaignList';
import Snackbar, { type SnackbarType } from './components/Snackbar';
import './App.css';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [snackbar, setSnackbar] = useState({ isOpen: false, message: '', type: 'info' as SnackbarType });

  const showSnackbar = (message: string, type: SnackbarType = 'info') => 
    setSnackbar({ isOpen: true, message, type });

  const handleCampaignCreated = () => {
    setRefreshKey(prev => prev + 1);
    showSnackbar('Campaign created successfully!', 'success');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📊 Pathik AI - Campaign Manager</h1>
        <p>Create and manage your Google Ads campaigns</p>
      </header>

      <main className="app-main">
        <div className="container">
          <div className="actions-bar">
            <button 
              className="btn-primary btn-add-campaign" 
              onClick={() => setIsModalOpen(true)}
            >
              + Create Campaign
            </button>
          </div>
          
          <CampaignList refresh={refreshKey} onError={(msg) => showSnackbar(msg, 'error')} />
        </div>
      </main>

      <CampaignModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleCampaignCreated}
        onError={(msg) => showSnackbar(msg, 'error')}
      />

      <Snackbar
        isOpen={snackbar.isOpen}
        message={snackbar.message}
        type={snackbar.type}
        onClose={() => setSnackbar(prev => ({ ...prev, isOpen: false }))}
      />

      <footer className="app-footer">
        <p>Pathik AI © 2025</p>
      </footer>
    </div>
  );
}

export default App;
