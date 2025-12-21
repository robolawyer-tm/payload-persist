#!/bin/bash
# create_dist.sh - Configures a clean tarball for manual distribution

VERSION="0.1.0"
DIST_NAME="payload-persist-v${VERSION}"
mkdir -p dist

echo "Creating distribution package: ${DIST_NAME}.tgz"

# Create a temporary directory for clean packaging
rm -rf "dist/${DIST_NAME}"
mkdir -p "dist/${DIST_NAME}"

# Copy essential files
cp \
  requirements.txt \
  web_server.py \
  setup_termux.sh \
  start_server.sh \
  termux_boot.sh \
  README.md \
  "dist/${DIST_NAME}/"

# Copy directories
cp -r lib static "dist/${DIST_NAME}/"

# Create DB directory structure
mkdir -p "dist/${DIST_NAME}/db"

# Create the tarball
cd dist
tar -czf "${DIST_NAME}.tgz" "${DIST_NAME}"
cd ..

echo "---------------------------------------------------"
echo "Package created at: dist/${DIST_NAME}.tgz"
echo "To install on phone:"
echo "1. Copy tgz to phone"
echo "2. Run: tar -xzf ${DIST_NAME}.tgz"
echo "3. Run: cd ${DIST_NAME} && ./setup_termux.sh"
echo "---------------------------------------------------"
