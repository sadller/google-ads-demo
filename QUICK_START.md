# Quick Start Guide

Get the Pathik AI Campaign Manager running in 5 minutes!

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (or Supabase account)

## Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
poetry install

# Set up environment variables
# Create .env file with:
DATABASE_URL=postgresql://user:password@localhost:5432/pathik_db
SECRET_KEY=your-secret-key
DEBUG=True

# Run database migrations
poetry run flask db upgrade

# Start the backend server
poetry run python run.py
```

Backend will run on: **http://localhost:8000**

## Step 2: Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will run on: **http://localhost:3000**

## Step 3: Test the Application

1. Open your browser to http://localhost:3000
2. Fill out the campaign form
3. Click "Save Campaign Locally"
4. See your campaign appear in the list below

## API Endpoints

### ✅ Implemented
- `POST /api/v1/campaigns` - Create campaign
- `GET /api/v1/campaigns` - Get all campaigns
- `GET /api/v1/campaigns?status=DRAFT` - Filter by status
- `GET /api/v1/campaigns/:id` - Get single campaign

### 🚧 To Be Implemented
- `POST /api/v1/campaigns/:id/publish` - Publish to Google Ads
- `POST /api/v1/campaigns/:id/pause` - Pause campaign

## Project Structure

```
pathik/
├── backend/               # Flask API
│   ├── src/app/
│   │   ├── api/          # Controllers
│   │   ├── services/     # Business logic
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Validation
│   │   ├── constants/    # Constants
│   │   └── utils/        # Utilities
│   └── run.py            # Start server
│
└── frontend/             # React UI
    ├── src/
    │   ├── components/   # UI components
    │   ├── services/     # API calls
    │   ├── types/        # TypeScript types
    │   ├── lib/          # Constants
    │   └── App.tsx       # Main app
    └── package.json
```

## Common Issues

### Backend Port Already in Use
```bash
# Change port in backend/run.py or set environment variable
export PORT=8001
```

### Frontend Port Already in Use
Frontend will automatically use the next available port (3001, 3002, etc.)

### CORS Errors
CORS is already configured in the backend. If you see errors, check that backend is running.

### Database Connection Error
1. Check PostgreSQL is running
2. Verify DATABASE_URL in .env
3. Run migrations: `poetry run flask db upgrade`

## Testing the APIs

### Using curl

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Get all campaigns
curl http://localhost:8000/api/v1/campaigns

# Create campaign
curl -X POST http://localhost:8000/api/v1/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Campaign",
    "objective": "Sales",
    "campaign_type": "Demand Gen",
    "daily_budget": 5000000,
    "start_date": "2025-12-20",
    "ad_group_name": "Main Group",
    "ad_headline": "Get 50% Off",
    "ad_description": "Limited time offer",
    "final_url": "https://example.com"
  }'
```

## Architecture Overview

```
┌─────────────────┐
│  React Frontend │  ← User Interface
└────────┬────────┘
         │ HTTP
┌────────▼────────┐
│  API Layer      │  ← Controllers (endpoints)
├─────────────────┤
│  Service Layer  │  ← Business Logic
├─────────────────┤
│  Data Layer     │  ← Models & Database
└─────────────────┘
```

## Next Steps

1. ✅ Create campaigns via UI
2. ✅ View campaigns in list
3. ✅ Filter by status
4. 🚧 Implement Google Ads publishing
5. 🚧 Add campaign editing
6. 🚧 Add authentication

## Documentation

- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
- [Assignment Requirements](assignment.txt)

## Support

For issues or questions, check the README files in backend/ and frontend/ folders.
