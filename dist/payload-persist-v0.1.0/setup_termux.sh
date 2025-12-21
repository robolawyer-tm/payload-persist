#!/bin/bash

# 1. Update Termux's list of apps
# Think of this like checking the app store for updates
echo "Step 1: Updating package list..."
pkg update -y && pkg upgrade -y

# 2. Install the necessary 'programs'
# python: runs your code
# gnupg: handles the encryption
# git: helps download/update files (good practice to have)
echo "Step 2: Installing Python and GPG..."
pkg install python gnupg git -y

# 3. Install the specific Python libraries your project needs
# This reads requirements.txt and downloads the exact tools required
echo "Step 3: Installing Python libraries..."
pip install -r requirements.txt

echo "---------------------------------------------------"
echo "Setup Complete! You can now run the server with:"
echo "./start_server.sh"
echo "---------------------------------------------------"
