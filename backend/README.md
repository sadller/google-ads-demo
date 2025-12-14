# Pathik AI - Backend

Flask + PostgreSQL + Google Ads API integration for managing marketing campaigns.

## Prerequisites

- Python 3.9+
- PostgreSQL
- Poetry

## Installation

```bash
cd backend

# Install dependencies
poetry install

# Create environment file
copy env.template .env  # Windows
cp env.template .env    # macOS/Linux

# Edit .env with your database credentials
```

## Database Setup

```bash
# Create database
psql -U postgres -c "CREATE DATABASE pathik_db;"

# Create tables
poetry run flask shell
>>> from app.core import db
>>> db.create_all()
>>> exit()
```

## Running the Application

```bash
poetry run python run.py
```

The API will be available at: http://localhost:5000

## Environment Variables

Edit `.env` file:

```ini
DATABASE_URL=postgresql://postgres:password@localhost:5432/pathik_db
SECRET_KEY=your-secret-key
DEBUG=True
GOOGLE_ADS_YAML_PATH=google-ads.yaml
```

## Google Ads API Setup

1. Copy the configuration template:
   ```bash
   cp google-ads.yaml.example google-ads.yaml
   ```

2. Add your Google Ads API credentials to `google-ads.yaml`:
   - Developer token
   - Client ID
   - Client secret
   - Refresh token
   - Login customer ID

   Get credentials from: https://ads.google.com/aw/apicenter

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/v1/health` - Health check with database status

## Project Structure

```
backend/
├── run.py                      # Start server
├── src/app/
│   ├── __init__.py            # Application factory
│   ├── core/
│   │   ├── config.py          # Configuration
│   │   └── extensions.py      # Flask extensions (db, migrate, etc.)
│   ├── api/v1/endpoints/      # API endpoints
│   ├── models/                # Database models
│   ├── schemas/               # Validation schemas
│   ├── services/              # Business logic
│   └── utils/                 # Utilities
└── tests/                     # Tests
```

## Database Migrations

```bash
# Initialize migrations (first time)
poetry run flask db init

# Create migration after model changes
poetry run flask db migrate -m "description"

# Apply migrations
poetry run flask db upgrade
```

## Development

### Adding a Model

```python
# app/models/campaign.py
from app.core import db

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
```

### Adding an Endpoint

```python
# app/api/v1/endpoints/campaigns.py
from flask import jsonify
from app.api.v1 import api_v1_bp

@api_v1_bp.route('/campaigns')
def get_campaigns():
    return jsonify({'campaigns': []})
```

Then import in `app/api/v1/endpoints/__init__.py`:
```python
from . import health, campaigns
```

### Running Tests

```bash
poetry run pytest
```

## Tech Stack

- **Flask** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Marshmallow** - Validation
- **Flask-Migrate** - Database migrations
- **Google Ads API** - Campaign publishing

## API Design

The backend provides RESTful APIs for:
- **POST /api/campaigns** - Create campaign (stores in PostgreSQL with status=DRAFT)
- **GET /api/campaigns** - List all campaigns
- **POST /api/campaigns/:id/publish** - Publish campaign to Google Ads
- **POST /api/campaigns/:id/pause** - Pause Google Ads campaign

## Contact

Sumit Pandey - sumitpandey0304@gmail.com
