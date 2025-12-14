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

### Using Supabase (Recommended)

1. Create a project at [supabase.com](https://supabase.com)
2. Get your connection string from Settings > Database > Connection pooling
3. Update `.env` with your Supabase connection string:
   ```
   DATABASE_URL=postgresql://postgres.xxxxx:[PASSWORD]@aws-0-region.pooler.supabase.com:6543/postgres
   ```
4. Create tables using Flask-Migrate:
   ```bash
   flask db init
   flask db migrate -m "Initial schema"
   flask db upgrade
   ```

### Using Local PostgreSQL

```bash
# Create database
psql -U postgres -c "CREATE DATABASE pathik_db;"

# Run migrations
flask db init
flask db migrate -m "Initial schema"
flask db upgrade
```

### Alternative: Direct table creation

```bash
# If you don't want to use migrations
python -m src.app.db_init
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

Flask-Migrate tracks database schema changes automatically.

```bash
# Step 1: Initialize migrations (only once)
flask db init

# Step 2: After adding/modifying models, create migration
flask db migrate -m "description of changes"

# Step 3: Apply migration to database
flask db upgrade
```

**Example: Adding a new column**

1. Edit `app/models/campaign.py` to add a new column
2. Run `flask db migrate -m "Add new column"`
3. Run `flask db upgrade`

**Rollback migration:** `flask db downgrade`

## Development

### Database Schema

Single table `campaigns` with all fields:

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR | Campaign name |
| objective | VARCHAR | Campaign objective |
| campaign_type | VARCHAR | Type of campaign |
| daily_budget | INTEGER | Budget in micros (1M = $1) |
| start_date | DATE | Start date |
| end_date | DATE | End date (optional) |
| status | VARCHAR | DRAFT/PUBLISHED/PAUSED |
| ad_group_name | VARCHAR | Ad group name |
| ad_headline | VARCHAR | Ad headline |
| ad_description | TEXT | Ad description |
| final_url | VARCHAR | Landing page URL |
| asset_url | VARCHAR | Image/video URL (optional) |
| google_campaign_id | VARCHAR | Google Ads ID |
| created_at | TIMESTAMP | Created timestamp |
| updated_at | TIMESTAMP | Updated timestamp |

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
