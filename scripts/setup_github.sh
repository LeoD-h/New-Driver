#!/bin/bash
# Script de setup GitHub pour NewDriver

set -e

cd /Users/leod/Documents/Dev/NewDriver

echo "=== Setup GitHub pour NewDriver ==="

# Initialiser Git si pas deja fait
if [ ! -d ".git" ]; then
    echo "Initialisation de Git..."
    git init
else
    echo "Git deja initialise"
fi

# Ajouter tous les fichiers (le .gitignore exclura les images)
echo "Ajout des fichiers..."
git add .

# Premier commit
echo "Creation du commit..."
git commit -m "Initial commit - NewDriver YOLO car game"

# Branche main
git branch -M main

# Ajouter le remote
echo "Configuration du remote..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/LeoD-h/New-Driver.git

# Push
echo "Push vers GitHub..."
git push -u origin main

echo ""
echo "=== Setup termine! ==="
echo "Repository: https://github.com/LeoD-h/New-Driver"
