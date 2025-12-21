#!/data/data/com.termux/files/usr/bin/sh

# This file is for the 'Termux:Boot' app.
# It tells the phone: "When you wake up, run this server."

# 1. Acquire Wake Lock
# This keeps the CPU running even if the screen turns off.
termux-wake-lock

# 2. Move to the project folder
# We need to be in the folder where the code lives.
# Adjust 'payload-persist' if you named the folder something else on your phone.
cd ~/payload-persist

# 3. Start the server in the background
# The '&' symbol means "run this in the background so I can still use the terminal"
# We save the output to a log file so we can check for errors later.
python web_server.py > boot_log.txt 2>&1 &
