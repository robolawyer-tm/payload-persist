#!/bin/bash

DEST="/home/john/secret-server"

# Create directories if needed
mkdir -p "$DEST/static"
mkdir -p "$DEST/templates"

# Copy core server files
cp web_server.py "$DEST"/
cp start_server.sh "$DEST"/
cp requirements.txt "$DEST"/

# Copy optional client/UI files if they exist
[ -f client.py ] && cp client.py "$DEST"/
[ -f main.py ] && cp main.py "$DEST"/
[ -f install.sh ] && cp install.sh "$DEST"/
[ -f update.sh ] && cp update.sh "$DEST"/

# Copy static assets
cp -r static/* "$DEST/static"/ 2>/dev/null

# Copy templates if present
[ -d templates ] && cp -r templates/* "$DEST/templates"/ 2>/dev/null

echo "Stable files copied into $DEST"

