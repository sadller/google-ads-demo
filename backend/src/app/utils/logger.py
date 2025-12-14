import logging
from pathlib import Path

# Create application logger
logger = logging.getLogger('pathik')


def setup_logger(app):
    log_dir = Path(app.root_path).parent.parent / 'logs'
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
    
    # Set logger level
    logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    
    app.logger.info('Application starting...')
