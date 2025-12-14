# Pathik AI - Campaign Manager

Full-stack application for managing Google Ads campaigns with React frontend and Flask backend.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or Supabase account)
- Google Ads API access

## Project Structure

```
pathik/
├── backend/           # Flask API
│   └── src/app/
│       ├── api/       # REST endpoints
│       ├── core/      # Config & extensions
│       ├── models/    # Database models
│       ├── schemas/   # Validation schemas
│       ├── services/  # Business logic
│       └── utils/     # Utilities
├── frontend/          # React app
│   └── src/
│       ├── components/
│       ├── services/
│       ├── types/
│       └── lib/
└── README.md
```

## Environment Variables

### Backend (`backend/.env`)

```env
# Flask
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (Supabase or local PostgreSQL)
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres

# Google Ads
GOOGLE_ADS_CUSTOMER_ID=1234567890
```

### Google Ads Configuration (`backend/google-ads.yaml`)

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID.apps.googleusercontent.com
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
login_customer_id: YOUR_MCC_CUSTOMER_ID
use_proto_plus: true
```

## Google Ads Setup

1. **Create a Google Ads Manager Account** at [ads.google.com](https://ads.google.com)

2. **Get API Access**
   - Go to [Google Ads API Center](https://developers.google.com/google-ads/api/docs/first-call/overview)
   - Apply for a developer token (test account for development)

3. **Create OAuth2 Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a project and enable Google Ads API
   - Create OAuth2 credentials (Desktop app)
   - Download client ID and client secret

4. **Generate Refresh Token**
   ```bash
   pip install google-ads
   google-ads-generate-refresh-token --client-id=YOUR_CLIENT_ID --client-secret=YOUR_SECRET
   ```

5. **Create `google-ads.yaml`** in the `backend/` directory with your credentials

## Backend Setup

```bash
cd backend

# Install dependencies
pip install poetry
poetry install

# Create .env file
cp .env.example .env
# Edit .env with your database URL

# Initialize database (first time only)
poetry run flask db init
poetry run flask db migrate -m "Initial migration"
poetry run flask db upgrade

# Run server
poetry run python run.py
```

**Other commands:**
```bash
poetry run flask db migrate -m "msg"  # Create migration
poetry run flask db upgrade           # Apply migrations
poetry run flask db downgrade         # Rollback migration
```

Backend runs at: http://localhost:8000

## Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Other commands:**
```bash
npm run build    # Production build
npm run preview  # Preview production build
```

Frontend runs at: http://localhost:5173

## API Documentation

Base URL: `http://localhost:8000/api/v1`

### Campaigns

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/campaigns` | List all campaigns |
| GET | `/campaigns?status=DRAFT` | Filter by status |
| GET | `/campaigns/{id}` | Get campaign details |
| POST | `/campaigns` | Create new campaign |
| POST | `/campaigns/{id}/publish` | Publish to Google Ads |
| PUT | `/campaigns/{id}/enable` | Enable campaign |
| PUT | `/campaigns/{id}/pause` | Pause campaign |

### Create Campaign Request

```json
{
  "name": "Summer Sale Campaign",
  "objective": "Sales",
  "campaign_type": "Demand Gen",
  "daily_budget": 5000000,
  "start_date": "2025-12-20",
  "end_date": "2025-12-31",
  "ad_group_name": "Main Ad Group",
  "ad_headline": "Get 50% Off",
  "ad_description": "Limited time offer",
  "final_url": "https://www.google.com/",
  "asset_url": "https://ssl.gstatic.com/webp/gallery/1.sm.jpg"
}
```

**Notes:**
- `daily_budget` is in micros (1,000,000 = $1)
- `end_date` and `asset_url` are optional
- `start_date` cannot be in the past

### Campaign Status Flow

```
DRAFT → PUBLISHED → ENABLED ↔ PAUSED
```

- **DRAFT**: Saved locally, not yet on Google Ads
- **PUBLISHED**: Created on Google Ads (paused state)
- **ENABLED**: Active on Google Ads (billing active)
- **PAUSED**: Paused on Google Ads

### Response Examples

**Success Response:**
```json
{
  "message": "Campaign created successfully",
  "campaign": {
    "id": "uuid",
    "name": "Summer Sale 2025",
    "status": "DRAFT",
    ...
  }
}
```

**Error Response:**
```json
{
  "error": "Validation error",
  "messages": {
    "daily_budget": ["Must be at least 1000000"]
  }
}
```

### Health Check

```
GET /api/v1/         # API info
GET /api/v1/health   # Health with database status
```

## Database Schema

```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    objective VARCHAR(100) NOT NULL,
    campaign_type VARCHAR(100) NOT NULL,
    daily_budget INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(50) DEFAULT 'DRAFT',
    ad_group_name VARCHAR(255) NOT NULL,
    ad_headline VARCHAR(255) NOT NULL,
    ad_description TEXT NOT NULL,
    final_url VARCHAR(2048) NOT NULL,
    asset_url VARCHAR(2048),
    google_campaign_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Troubleshooting

**Database connection issues:**
- Verify DATABASE_URL in .env
- Check PostgreSQL is running
- For Supabase, ensure IP is whitelisted

**Google Ads API errors:**
- Verify google-ads.yaml credentials
- Check developer token is approved
- Ensure customer ID is correct (no dashes)

**Campaign publish fails:**
- Check GOOGLE_ADS_CUSTOMER_ID is set
- Verify URLs are valid and accessible
- Review Google Ads policy requirements

## License

MIT
