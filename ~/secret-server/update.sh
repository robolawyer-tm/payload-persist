#!/bin/bash
# Simple "One-Click" Updater for Secret Server
# This script ensures your phone/server is always on the latest polished version.

echo "🔄 Syncing Secret Server to the latest polished version..."

# Ensure we are on the main branch
git checkout main &>/dev/null

# Force sync with the latest on GitHub
git fetch origin
git reset --hard origin/main

echo "✅ App is now updated to the final polished copy!"
echo "🚀 Restarting server..."

# Restart the server (adjust if your start script naming is different)
if [ -f "./start_server.sh" ]; then
    ./start_server.sh
else
    python3 web_server.py
fi
