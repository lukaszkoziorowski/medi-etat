# Medietat UI Architecture

## Design System

### Color Palette

**Primary Colors:**
```css
--color-primary: #2563eb;        /* Professional blue - trust, healthcare */
--color-primary-dark: #1e40af;   /* Hover states, emphasis */
--color-primary-light: #3b82f6;  /* Active states */
```

**Neutral Colors:**
```css
--color-text-primary: #1f2937;   /* Main text - high contrast */
--color-text-secondary: #6b7280;  /* Secondary text, metadata */
--color-text-muted: #9ca3af;     /* Disabled, placeholders */

--color-bg-primary: #ffffff;      /* Main background */
--color-bg-secondary: #f9fafb;    /* Cards, sections */
--color-bg-tertiary: #f3f4f6;    /* Subtle backgrounds */

--color-border: #e5e7eb;          /* Default borders */
--color-border-light: #f3f4f6;   /* Subtle dividers */
```

**Semantic Colors:**
```css
--color-success: #10b981;         /* Success states */
--color-warning: #f59e0b;         /* Warnings */
--color-error: #ef4444;           /* Errors */
--color-info: #3b82f6;            /* Info messages */
```

**Role Badge Colors (Medical Roles):**
```css
--color-role-lekarz: #2563eb;           /* Doctor - primary blue */
--color-role-pielegniarka: #8b5cf6;     /* Nurse - purple */
--color-role-polozna: #ec4899;          /* Midwife - pink */
--color-role-ratownik: #f59e0b;         /* Paramedic - amber */
--color-role-inny: #6b7280;             /* Other - neutral gray */
```

### Typography Scale

**Font Family:**
```css
--font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
                    'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 
                    'Droid Sans', 'Helvetica Neue', sans-serif;
--font-family-heading: var(--font-family-base);
--font-family-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', monospace;
```

**Font Sizes (Modular Scale - 1.25 ratio):**
```css
--font-size-xs: 0.75rem;    /* 12px - labels, captions */
--font-size-sm: 0.875rem;   /* 14px - secondary text */
--font-size-base: 1rem;     /* 16px - body text */
--font-size-lg: 1.125rem;   /* 18px - emphasized text */
--font-size-xl: 1.25rem;   /* 20px - small headings */
--font-size-2xl: 1.5rem;   /* 24px - section headings */
--font-size-3xl: 1.875rem; /* 30px - page titles */
--font-size-4xl: 2.25rem;  /* 36px - hero text */
```

**Font Weights:**
```css
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

**Line Heights:**
```css
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
```

### Spacing Scale (8px base unit)

```css
--spacing-0: 0;
--spacing-1: 0.25rem;   /* 4px */
--spacing-2: 0.5rem;    /* 8px */
--spacing-3: 0.75rem;   /* 12px */
--spacing-4: 1rem;      /* 16px */
--spacing-5: 1.25rem;   /* 20px */
--spacing-6: 1.5rem;   /* 24px */
--spacing-8: 2rem;     /* 32px */
--spacing-10: 2.5rem;   /* 40px */
--spacing-12: 3rem;     /* 48px */
--spacing-16: 4rem;     /* 64px */
--spacing-20: 5rem;     /* 80px */
```

### Border Radius

```css
--radius-sm: 0.25rem;   /* 4px - small elements */
--radius-md: 0.375rem;  /* 6px - buttons, inputs */
--radius-lg: 0.5rem;    /* 8px - cards */
--radius-xl: 0.75rem;   /* 12px - large cards */
--radius-full: 9999px;   /* Pills, badges */
```

### Shadows

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

### Breakpoints

```css
--breakpoint-sm: 640px;   /* Mobile landscape */
--breakpoint-md: 768px;    /* Tablet */
--breakpoint-lg: 1024px;   /* Desktop */
--breakpoint-xl: 1280px;   /* Large desktop */
--breakpoint-2xl: 1536px;  /* Extra large */
```

### Transitions

```css
--transition-fast: 150ms ease-in-out;
--transition-base: 200ms ease-in-out;
--transition-slow: 300ms ease-in-out;
```

---

## Layout System

### Global Layout Structure

```
┌─────────────────────────────────────┐
│           Header                    │
│  (Logo + Navigation)                │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────┐  ┌─────────────────┐ │
│  │ Filters  │  │   Job List      │ │
│  │ Panel    │  │   (Main Content)│ │
│  │          │  │                 │ │
│  │          │  │   [JobCard]     │ │
│  │          │  │   [JobCard]     │ │
│  │          │  │   [JobCard]     │ │
│  └──────────┘  └─────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│           Footer                    │
└─────────────────────────────────────┘
```

### Max Content Width

```css
--container-max-width: 1280px;  /* Main content area */
--container-padding: var(--spacing-4);  /* Side padding */
```

**Layout Rules:**
- Content is centered with max-width
- Filters sidebar: 280px on desktop, full-width on mobile
- Main content area: flexible, fills remaining space
- Consistent padding on all sides

### Responsive Behavior

**Desktop (≥1024px):**
- Side-by-side layout: Filters (left) + Job List (right)
- Filters always visible
- 2-3 column grid for job cards (if needed)

**Tablet (768px - 1023px):**
- Stacked layout: Filters above Job List
- Filters can be collapsed/expanded
- 2 column grid for job cards

**Mobile (<768px):**
- Single column layout
- Filters in collapsible drawer/modal
- Full-width job cards
- Touch-friendly tap targets (min 44px)

---

## Component Architecture

### Core Components

#### 1. JobCard
**Purpose:** Display a single job offer preview

**Props:**
```typescript
interface JobCardProps {
  id: number;
  title: string;
  facilityName: string;
  city: string;
  role: MedicalRole;
  description?: string;
  sourceUrl: string;
  createdAt: string;
  onClick?: (id: number) => void;
}
```

**Structure:**
```
┌─────────────────────────────────────┐
│ [RoleBadge]                         │
│                                     │
│ Job Title (h3)                      │
│ Facility Name                       │
│ [LocationTag]                       │
│                                     │
│ Description preview (truncated)...  │
│                                     │
│ [View Details] →                    │
└─────────────────────────────────────┘
```

**Responsibilities:**
- Display job information clearly
- Handle click navigation
- Truncate long descriptions
- Show role badge and location
- Link to source URL

**Styling:**
- Card with subtle shadow
- Hover state: slight elevation
- Padding: `var(--spacing-6)`
- Border radius: `var(--radius-lg)`

---

#### 2. JobList
**Purpose:** Container for multiple JobCard components

**Props:**
```typescript
interface JobListProps {
  jobs: JobOffer[];
  loading?: boolean;
  emptyMessage?: string;
  onJobClick?: (id: number) => void;
}
```

**Structure:**
```
┌─────────────────────────────────────┐
│ Results: 45 jobs                    │
├─────────────────────────────────────┤
│ [JobCard]                           │
│ [JobCard]                           │
│ [JobCard]                           │
│ ...                                 │
└─────────────────────────────────────┘
```

**Responsibilities:**
- Render list of JobCard components
- Show loading state
- Show empty state when no jobs
- Display result count
- Handle pagination/infinite scroll (future)

**Styling:**
- Grid or flex layout
- Gap between cards: `var(--spacing-6)`
- Responsive columns

---

#### 3. FiltersPanel
**Purpose:** Filter job listings by role and location

**Props:**
```typescript
interface FiltersPanelProps {
  roles: MedicalRole[];
  selectedRole?: MedicalRole | null;
  cities: string[];
  selectedCity?: string | null;
  onRoleChange: (role: MedicalRole | null) => void;
  onCityChange: (city: string | null) => void;
  onClear: () => void;
  isMobile?: boolean;
}
```

**Structure:**
```
┌─────────────────────────────────────┐
│ Filters                             │
│                                     │
│ Role:                               │
│ ○ All                               │
│ ● Lekarz                            │
│ ○ Pielęgniarka                      │
│ ○ Położna                           │
│ ...                                 │
│                                     │
│ Location:                           │
│ [Select dropdown]                   │
│                                     │
│ [Clear Filters]                     │
└─────────────────────────────────────┘
```

**Responsibilities:**
- Display filter options dynamically
- Handle filter changes
- Show active filters
- Clear all filters
- Responsive behavior (drawer on mobile)

**Styling:**
- Background: `var(--color-bg-secondary)`
- Padding: `var(--spacing-6)`
- Border radius: `var(--radius-lg)`
- Sticky on desktop scroll

---

#### 4. RoleBadge
**Purpose:** Visual indicator for medical role

**Props:**
```typescript
interface RoleBadgeProps {
  role: MedicalRole;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'solid' | 'outline';
}
```

**Structure:**
```
[Lekarz]
```

**Responsibilities:**
- Display role name
- Apply role-specific color
- Support different sizes
- Support outline/solid variants

**Styling:**
- Background color from role color variable
- Text color: white or dark (contrast)
- Padding: `var(--spacing-2)` horizontal, `var(--spacing-1)` vertical
- Border radius: `var(--radius-full)`
- Font size: `var(--font-size-sm)`
- Font weight: `var(--font-weight-medium)`

---

#### 5. LocationTag
**Purpose:** Display job location

**Props:**
```typescript
interface LocationTagProps {
  city: string;
  size?: 'sm' | 'md';
}
```

**Structure:**
```
📍 Gdańsk
```

**Responsibilities:**
- Display city name
- Optional icon
- Consistent styling

**Styling:**
- Subtle background
- Icon + text
- Small, unobtrusive

---

#### 6. EmptyState
**Purpose:** Display when no jobs match filters

**Props:**
```typescript
interface EmptyStateProps {
  message?: string;
  actionLabel?: string;
  onAction?: () => void;
}
```

**Structure:**
```
┌─────────────────────────────────────┐
│         [Icon]                       │
│                                     │
│   No jobs found                     │
│                                     │
│   Try adjusting your filters        │
│                                     │
│   [Clear Filters]                   │
└─────────────────────────────────────┘
```

**Responsibilities:**
- Show helpful message
- Suggest actions
- Provide clear next steps

---

#### 7. LoadingState
**Purpose:** Show loading indicator

**Props:**
```typescript
interface LoadingStateProps {
  message?: string;
  fullScreen?: boolean;
}
```

**Structure:**
```
[Spinner] Loading jobs...
```

**Responsibilities:**
- Show loading indicator
- Optional message
- Skeleton screens for cards (future)

---

### Supporting Components

#### Button
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}
```

#### Input / Select
```typescript
interface SelectProps {
  options: { value: string; label: string }[];
  value?: string;
  onChange: (value: string) => void;
  placeholder?: string;
}
```

#### Link
```typescript
interface LinkProps {
  href: string;
  external?: boolean;
  children: ReactNode;
}
```

---

## Key Screens

### 1. Homepage (Job Listing)

**URL:** `/`

**Structure:**
```
<Layout>
  <Header />
  <MainContent>
    <FiltersPanel 
      roles={availableRoles}
      cities={availableCities}
      selectedRole={activeRole}
      selectedCity={activeCity}
      onRoleChange={handleRoleChange}
      onCityChange={handleCityChange}
    />
    <JobList 
      jobs={filteredJobs}
      loading={isLoading}
      onJobClick={handleJobClick}
    />
  </MainContent>
  <Footer />
</Layout>
```

**Information Hierarchy:**
1. Page title: "Oferty pracy dla personelu medycznego"
2. Active filters (if any)
3. Result count
4. Job cards (most important)
5. Pagination (future)

**Component Composition:**
- Layout (container)
- Header (logo, navigation)
- FiltersPanel (sidebar or top)
- JobList (main content)
- JobCard[] (individual jobs)
- Footer (minimal)

**Interaction Rules:**
- Click job card → navigate to detail page
- Change filter → update URL, refetch data
- Clear filters → reset to all jobs
- Mobile: Filters in drawer, toggleable

---

### 2. Job Detail Page

**URL:** `/job/[id]`

**Structure:**
```
<Layout>
  <Header />
  <MainContent>
    <Breadcrumb />
    <JobDetail 
      job={jobData}
      onBack={handleBack}
    />
  </MainContent>
  <Footer />
</Layout>
```

**JobDetail Component:**
```
┌─────────────────────────────────────┐
│ [← Back to listings]                │
├─────────────────────────────────────┤
│ [RoleBadge]                         │
│                                     │
│ Job Title (h1)                      │
│                                     │
│ Facility: [Name]                    │
│ Location: [LocationTag]             │
│                                     │
│ Description:                        │
│ [Full description text]             │
│                                     │
│ ─────────────────────────────────── │
│                                     │
│ [Zobacz ofertę na stronie źródłowej]│
│ (External link, opens in new tab)   │
└─────────────────────────────────────┘
```

**Information Hierarchy:**
1. Back navigation
2. Role badge
3. Job title
4. Facility and location
5. Full description
6. Source link (prominent CTA)

**Component Composition:**
- Layout
- Breadcrumb (Home > Job)
- JobDetail
  - RoleBadge
  - Title
  - Metadata (facility, location)
  - Description
  - ExternalLink (source URL)

**Interaction Rules:**
- Back button → return to listing with filters preserved
- Source link → open in new tab
- Share functionality (future)

---

## Scalability Rules

### 1. Dynamic Data
**Never hardcode:**
- Role names → fetch from API or enum
- City names → extract from job data
- Filter options → generate from available data

**Implementation:**
```typescript
// Extract unique values from jobs
const availableRoles = [...new Set(jobs.map(j => j.role))];
const availableCities = [...new Set(jobs.map(j => j.city))];
```

### 2. Filter System
**Design for extensibility:**
- Filter component accepts array of filter definitions
- Each filter is independent
- Easy to add new filter types

**Future filters:**
- Date posted
- Facility type
- Employment type
- Salary range

### 3. Sorting
**Prepare for:**
- Sort by date (newest first)
- Sort by relevance
- Sort by facility name

**Implementation:**
- Sort component (future)
- URL query params for sort state
- Preserve sort when filtering

### 4. Pagination / Infinite Scroll
**Design considerations:**
- Pagination component (future)
- Infinite scroll option (future)
- URL-based page state
- Loading states for next page

### 5. Saved Searches (Future)
**Architecture:**
- Search state in URL
- Bookmarkable URLs
- Share functionality

---

## Naming Conventions

### Components
- PascalCase: `JobCard`, `FiltersPanel`, `RoleBadge`
- Descriptive: `JobDetailPage`, not `Detail`
- Consistent suffixes: `*Panel`, `*Card`, `*Badge`, `*Tag`

### Files
- Component files: `JobCard.tsx`, `FiltersPanel.tsx`
- Page files: `page.tsx` (Next.js convention)
- Utility files: `utils.ts`, `constants.ts`

### CSS Variables
- Kebab-case: `--color-primary`, `--spacing-4`
- Grouped by type: `--color-*`, `--spacing-*`, `--font-*`

### TypeScript Types
- Interfaces: `JobCardProps`, `FiltersPanelProps`
- Types: `MedicalRole`, `JobOffer`
- Enums: `MedicalRole` (matches backend)

---

## Interaction Rules

### Filtering
1. User selects filter → Update URL query params
2. URL change → Trigger data fetch
3. Show loading state
4. Update job list
5. Update result count
6. Preserve filters in URL (shareable/bookmarkable)

### Navigation
1. Click job card → Navigate to `/job/[id]`
2. Preserve current filters in URL state
3. Back button → Return with filters intact

### External Links
1. Source URL link → Open in new tab
2. Clear visual indication (external icon)
3. Accessibility: "Opens in new window"

### Responsive Behavior
1. Desktop: Filters sidebar always visible
2. Tablet: Filters collapsible above content
3. Mobile: Filters in drawer/modal, toggleable

---

## Implementation Plan

### Phase 1: Foundation
1. Set up Next.js project structure
2. Create design system (CSS variables/Tailwind config)
3. Create Layout component
4. Create Header and Footer

### Phase 2: Core Components
1. RoleBadge
2. LocationTag
3. Button
4. JobCard
5. JobList

### Phase 3: Filters
1. FiltersPanel
2. Filter components (role, location)
3. URL state management
4. API integration

### Phase 4: Pages
1. Homepage with JobList
2. Job detail page
3. Navigation between pages

### Phase 5: Polish
1. Loading states
2. Empty states
3. Error handling
4. Responsive refinements

---

## Technical Stack Recommendations

- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS (with custom variables) or CSS Modules
- **State Management:** URL query params + React state
- **Data Fetching:** Server Components + API routes
- **Type Safety:** TypeScript (match backend types)

---

## Accessibility Considerations

- Semantic HTML (header, main, nav, article)
- ARIA labels for filters and actions
- Keyboard navigation support
- Focus indicators
- Color contrast (WCAG AA minimum)
- Screen reader friendly

---

## Performance Considerations

- Server-side rendering for initial load
- Client-side filtering for instant updates
- Image optimization (if needed)
- Lazy loading for job cards (if many)
- Minimal JavaScript bundle

---

This architecture provides:
✅ Scalable component system
✅ Consistent design language
✅ Future-proof structure
✅ Clear separation of concerns
✅ Easy to maintain and extend

