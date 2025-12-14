"""
Logging Configuration
"""
import logging
from pathlib import Path


def setup_logger(app):
    """Setup application logging"""
    
    # Create logs directory
    log_dir = Path(app.root_path).parent.parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log'),
            logging.StreamHandler()
        ]
    )
    
    app.logger.info('Application starting...')
