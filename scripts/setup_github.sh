#!/bin/bash
# GitHub setup script for NewDriver

set -e

cd /Users/leod/Documents/Dev/NewDriver

echo "=== GitHub setup for NewDriver ==="

# Initialize Git if not already done
if [ ! -d ".git" ]; then
    echo "Initializing Git..."
    git init
else
    echo "Git already initialized"
fi

# Add all files (.gitignore will exclude images)
echo "Adding files..."
git add .

# First commit
echo "Creating commit..."
git commit -m "Initial commit - NewDriver YOLO car game"

# Main branch
git branch -M main

# Add remote
echo "Configuring remote..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/LeoD-h/New-Driver.git

# Push
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "=== Setup complete! ==="
echo "Repository: https://github.com/LeoD-h/New-Driver"
