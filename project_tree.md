# Personal AI - Complete Folder Structure

```
personal-ai/
├── agents/                  # AI Agent Implementations
│   ├── critic.py
│   ├── planner.py
│   └── researcher.py
├── api/                     # Backend API (FastAPI)
│   ├── routers/             # Modular API Routes
│   │   ├── analytics.py
│   │   ├── goals.py
│   │   ├── memories.py
│   │   ├── notifications.py
│   │   ├── settings.py
│   │   └── tasks.py
│   ├── services/            # Business Logic
│   ├── auth.py              # Authentication Middleware
│   ├── config.py            # Configuration
│   ├── database.py          # Database Connection (SQLite)
│   ├── models.py            # SQLAlchemy Models
│   ├── ollama_client.py     # LLM Client
│   ├── routes.py            # (Legacy/Partial Routes)
│   ├── schema.py            # Pydantic Schemas
│   ├── server.py            # Main Entry Point
│   ├── system.py            # Shared System State
│   └── uploads.py           # File Upload Handling
├── autonomy/                # Autonomous Agent Loop
│   ├── async_task_runner.py
│   ├── autonomy_loop.py
│   ├── goal_engine.py
│   ├── task_decomposer.py
│   └── task_runner.py
├── brain/                   # Core Logic / Cognitive Engine
│   ├── cache.py
│   ├── model.py
│   ├── multimodal.py
│   └── run_engine.py
├── control/                 # Rules and Evaluation
│   ├── evaluator.py
│   ├── rule_updater.py
│   └── rules.yaml
├── data/                    # Persistent Data Storage
│   └── weion.db             # SQLite Database
├── frontend/                # Frontend (Next.js)
│   ├── public/              # Static Assets
│   └── src/
│       ├── app/             # App Router Pages
│       ├── components/      # UI Components
│       ├── hooks/           # Custom React Hooks
│       ├── lib/             # Utilities
│       ├── services/        # API Clients
│       ├── store/           # State Management
│       └── types/           # TS Types
├── interface/               # (Legacy Interface Code)
├── logs/                    # System Logs & Cache
├── memory/                  # Long-term Memory Logic
│   ├── decision_log.py
│   ├── memory_agent.py
│   ├── store.py
│   └── vector_store.py
├── ui/                      # (Legacy UI Code)
├── uploads/                 # Uploaded User Files
├── main.py                  # CLI Entry Point
└── project_structure.md     # High-level architecture doc
```
