# WEION AI - Project Structure

The codebase is split into a Next.js frontend and a FastAPI backend with SQLite database.

## 📂 Backend (`api/`)
This folder contains the core logic, API endpoints, and database models.

```bash
api/
├── server.py          # Main entry point (Mounts routers, WebSockets, background loop)
├── database.py        # Database connection (SQLite + SQLAlchemy)
├── models.py          # Database Tables (Memory, Goal, Task, Log, Setting, Notification)
├── auth.py            # API Key Authentication Logic
├── system.py          # Shared System State & Logging (prevents circular imports)
├── routers/           # API Endpoints (Modularized)
│   ├── analytics.py   # System stats endpoints
│   ├── goals.py       # Goal CRUD
│   ├── memories.py    # Memory CRUD
│   ├── tasks.py       # Task CRUD
│   ├── settings.py    # Settings/Config endpoints
│   └── notifications.py # Notification endpoints
├── services/          # Business Logic (Autonomy, LLM calls)
│   └── (autonomy logic resides in parent `autonomy/` folder for now)
└── uploads/           # Directory for uploaded files
```

## 📂 Frontend (`frontend/`)
Next.js 14 App Router application.

```bash
frontend/src/
├── app/
│   ├── (dashboard)/   # Protected dashboard routes
│   │   ├── dashboard/ # Main chat interface
│   │   ├── memory/    # Memory explorer
│   │   ├── goals/     # Goal tracker
│   │   ├── analytics/ # System stats
│   │   └── settings/  # Config page
│   ├── login/         # Login page
│   └── layout.tsx     # Main layout wrapper
├── components/        # Reusable UI components
│   ├── console/       # Chat interface components
│   ├── ui/            # Buttons, Cards, Inputs
│   └── ...
└── lib/               # Utilities (API client, helpers)
```

## 📂 Data Storage
- `data/weion.db` (SQLite Database - Created automatically)
- `uploads/` (Uploaded files)
