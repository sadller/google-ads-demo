# Pathik AI - Frontend

React + TypeScript + Vite application for managing Google Ads campaigns.

## Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend server running on `http://localhost:8000`

## Installation

```bash
cd frontend

# Install dependencies
npm install
```

## Running the Application

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The app will be available at: http://localhost:5173

## Project Structure

```
frontend/src/
├── components/          # React components
│   ├── CampaignModal.tsx   # Campaign creation modal
│   └── CampaignList.tsx    # Campaign listing table
│
├── services/           # API services
│   └── campaignService.ts  # Campaign API calls
│
├── types/              # TypeScript types
│   └── campaign.ts         # Campaign interfaces
│
├── lib/                # Utilities & constants
│   └── constants.ts        # App constants
│
├── App.tsx             # Main app component
├── App.css             # App styles
├── main.tsx            # Entry point
└── index.css           # Global styles
```

## Features

### Campaign Modal
- "+ Create Campaign" button to open modal
- Create new campaigns with all required fields
- Modal popup for clean UI
- Validation for required fields
- Budget conversion display (micros to dollars)
- Date pickers for start/end dates
- Campaign type and objective selection
- Cancel/Create actions

### Campaign List
- View all campaigns in a table
- Filter by status (DRAFT, PUBLISHED, PAUSED) - client-side
- Display campaign details with budget conversion
- Status badges with color coding
- **Publish button** for DRAFT campaigns - publishes to Google Ads
- **Pause button** for PUBLISHED campaigns - pauses in Google Ads
- Loading states during publish/pause actions
- Real-time status updates

## API Integration

The app connects to the backend API at `http://localhost:8000/api/v1`

### Endpoints Used:
- `GET /campaigns` - Fetch all campaigns
- `POST /campaigns` - Create new campaign
- `POST /campaigns/:id/publish` - Publish campaign to Google Ads
- `POST /campaigns/:id/pause` - Pause campaign in Google Ads

## Configuration

Update API base URL in `src/lib/constants.ts`:

```typescript
export const API_BASE_URL = 'http://localhost:8000/api/v1';
```

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Fetch API** - HTTP requests
- **CSS3** - Styling

## Development

### Code Organization
- **Components** - Reusable UI components
- **Services** - API interaction layer
- **Types** - TypeScript interfaces
- **Lib** - Constants and utilities

### Best Practices
- TypeScript for type safety
- Async/await for API calls
- Error handling in all requests
- Loading states for better UX
- Responsive design

## Building for Production

```bash
npm run build
```

Builds the app for production to the `dist` folder.

## Troubleshooting

### CORS Issues
If you see CORS errors, make sure the backend has CORS enabled for the frontend origin.

### API Connection
Ensure the backend is running on port 8000 before starting the frontend.

### Port Already in Use
If port 5173 is taken, Vite will automatically use the next available port.

## Features Implemented

- ✅ Create campaigns with modal form
- ✅ List all campaigns
- ✅ Client-side status filtering
- ✅ Publish to Google Ads
- ✅ Pause campaigns
- ✅ Snackbar notifications
- ✅ Real-time updates
- ✅ Loading states
- ✅ Error handling

## Future Enhancements

- [ ] Campaign edit functionality
- [ ] Campaign delete
- [ ] Pagination for large lists
- [ ] Campaign analytics
- [ ] Bulk operations
