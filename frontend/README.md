# Medietat Frontend

Next.js frontend for Medietat job search engine.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── page.tsx           # Homepage
│   ├── job/[id]/          # Job detail page
│   └── layout.tsx         # Root layout
├── components/
│   ├── layout/            # Layout components
│   ├── jobs/              # Job-related components
│   ├── filters/           # Filter components
│   └── ui/                # Reusable UI components
├── lib/
│   └── api.ts             # API client
├── types/
│   └── index.ts           # TypeScript types
└── app/globals.css        # Design system variables
```

## Design System

All styling uses CSS variables defined in `app/globals.css`:
- Colors (primary, neutral, semantic, role-specific)
- Typography (sizes, weights, line heights)
- Spacing (8px base unit)
- Border radius, shadows, transitions

## Components

- **Layout**: Header, Footer, Layout wrapper
- **Jobs**: JobCard, JobList, RoleBadge, LocationTag
- **Filters**: FiltersPanel (role and location)
- **UI**: Button, LoadingState, EmptyState

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`:
- `GET /api/jobs/` - List all jobs
- `GET /api/jobs/?role=ROLE` - Filter by role
- `GET /api/jobs/{id}` - Get single job

## Features

- ✅ Job listing with filters
- ✅ Role filtering
- ✅ Location filtering (client-side)
- ✅ Job detail page
- ✅ External source links
- ✅ Responsive design
- ✅ Loading and empty states
