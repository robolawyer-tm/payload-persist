#!/bin/bash

echo "========================================="
echo "  Secret Server Uninstallation"
echo "========================================="
echo ""

INSTALL_DIR="$HOME/payload-persist"
BASHRC="$HOME/.bashrc"
BOOT_SCRIPT="$HOME/.termux/boot/termux_boot.sh"

# Confirm uninstallation
read -p "⚠️  This will remove Secret Server and all data. Continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Uninstallation cancelled."
    exit 0
fi

echo ""
echo "🗑️  Removing Secret Server..."

# 1. Remove boot script
if [ -f "$BOOT_SCRIPT" ]; then
    echo "  - Removing boot script..."
    rm -f "$BOOT_SCRIPT"
fi

# 2. Remove alias from .bashrc
if [ -f "$BASHRC" ]; then
    echo "  - Removing 'secret-server' command..."
    sed -i '/alias secret-server=/d' "$BASHRC"
fi

# 3. Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "  - Removing installation directory..."
    rm -rf "$INSTALL_DIR"
fi

echo ""
echo "========================================="
echo "✅ Secret Server has been uninstalled"
echo "========================================="
echo ""
echo "Note: Python, GPG, and Git were NOT removed."
echo "      (They may be used by other apps)"
echo ""
echo "To reinstall, run:"
echo "  curl -sSL https://raw.githubusercontent.com/JohnBlakesDad/payload-persist/secret-server/install.sh | bash"
echo ""
