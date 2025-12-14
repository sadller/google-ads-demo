import logging
from pathlib import Path

logger = logging.getLogger('pathik')


def setup_logger(app):
    log_dir = Path(app.root_path).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log'),
            logging.StreamHandler()
        ]
    )
    
    logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    app.logger.info('Application starting...')
