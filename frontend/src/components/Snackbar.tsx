import { useEffect } from 'react';

export type SnackbarType = 'success' | 'error' | 'warning' | 'info';

interface SnackbarProps {
  message: string;
  type?: SnackbarType;
  isOpen: boolean;
  onClose: () => void;
  duration?: number;
}

const SNACKBAR_STYLES = {
  success: { backgroundColor: '#10b981', icon: '✓' },
  error: { backgroundColor: '#ef4444', icon: '✕' },
  warning: { backgroundColor: '#f59e0b', icon: '⚠' },
  info: { backgroundColor: '#3b82f6', icon: 'ℹ' }
};

export default function Snackbar({ 
  message, 
  type = 'info', 
  isOpen, 
  onClose,
  duration = 5000 
}: SnackbarProps) {
  
  useEffect(() => {
    if (isOpen && duration > 0) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [isOpen, duration, onClose]);

  if (!isOpen) return null;

  const { backgroundColor, icon } = SNACKBAR_STYLES[type];

  return (
    <div className="snackbar-container">
      <div 
        className="snackbar" 
        style={{ backgroundColor }}
      >
        <span className="snackbar-icon">{icon}</span>
        <span className="snackbar-message">{message}</span>
        <button 
          className="snackbar-close" 
          onClick={onClose}
          aria-label="Close"
        >
          ×
        </button>
      </div>
    </div>
  );
}
