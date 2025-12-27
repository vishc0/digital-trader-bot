# TradeSense AI - Frontend

Next.js 14 web application for TradeSense AI trading platform.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts + D3.js
- **State**: Zustand
- **Forms**: React Hook Form + Zod
- **Real-Time**: Socket.IO

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth pages (login, signup)
│   ├── dashboard/
│   ├── positions/
│   ├── watchlist/
│   ├── analysis/
│   ├── trade/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── charts/            # Chart components
│   ├── positions/         # Position management
│   ├── ui/                # Reusable UI components
│   └── layout/            # Layout components
├── lib/
│   ├── api.ts             # API client
│   ├── websocket.ts       # WebSocket client
│   └── utils.ts
├── hooks/                 # Custom React hooks
└── store/                 # Zustand stores
```

## Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## Features

- ✅ Dark mode by default
- ✅ Responsive design
- ✅ Real-time data via WebSocket
- ✅ Interactive charts (ORATS-style)
- ✅ AI-powered analysis
- ✅ Options trading tools

## Deployment

Deploy to Vercel (recommended):

```bash
vercel
```

Or use the Vercel GitHub integration for automatic deployments.
