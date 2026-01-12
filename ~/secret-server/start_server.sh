#!/bin/bash

# This is a simple shortcut to start your server.
# Instead of typing "python web_server.py" every time, you just run this.

echo "Starting Payload Persist Server..."
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 web_server.py
