
#!/bin/bash

# start_system.sh
echo "🔮 Initializing WEION Civilization Engine..."

# 1. Start Backend (Background)
echo "🧠 Starting Logic Core (Backend)..."
python3 -m uvicorn backend.main:app --port 8000 &
BACKEND_PID=$!

# 2. Start Frontend
echo "🌐 Launching Portal (Frontend)..."
cd frontend
npm run dev

# Cleanup on exit
kill $BACKEND_PID
