#!/bin/bash

# GitHub Repository Setup Script
# This script will initialize your git repository and push to GitHub

echo "=========================================="
echo "GitHub Portfolio Setup"
echo "=========================================="
echo ""

# Step 1: Organize files
echo "Step 1: Organizing files..."
mkdir -p webscraper
if [ -f "Webscrapper.py" ]; then
    cp Webscrapper.py webscraper/webscrapper.py
    echo "✓ Copied webscrapper.py to webscraper/ folder"
else
    echo "⚠ Webscrapper.py not found in current directory"
fi

# Step 2: Initialize Git
echo ""
echo "Step 2: Initializing Git repository..."
git init
echo "✓ Git repository initialized"

# Step 3: Add files
echo ""
echo "Step 3: Adding files to Git..."
git add .
echo "✓ Files staged for commit"

# Step 4: Show what will be committed
echo ""
echo "Files that will be committed:"
git status --short

# Step 5: Create initial commit
echo ""
echo "Step 4: Creating initial commit..."
git commit -m "Initial commit: Add intelligent web scraper

- Production-ready web scraper with retry logic and error handling
- Multi-site support with flexible CSS selectors
- Comprehensive documentation and setup guides
- MIT licensed for open-source use"

echo "✓ Initial commit created"

# Step 6: Instructions for GitHub
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "Choose one of the following options to create your GitHub repository:"
echo ""
echo "OPTION 1: Using GitHub CLI (Recommended)"
echo "  gh auth login"
echo "  gh repo create python-portfolio --public --source=. --remote=origin --push"
echo ""
echo "OPTION 2: Using GitHub Web Interface"
echo "  1. Go to https://github.com/new"
echo "  2. Repository name: python-portfolio"
echo "  3. Description: Production-ready Python projects demonstrating web scraping, automation, and AI integration"
echo "  4. Make it Public"
echo "  5. DO NOT initialize with README"
echo "  6. Click 'Create repository'"
echo ""
echo "  Then run these commands:"
echo "  git remote add origin https://github.com/YOUR_USERNAME/python-portfolio.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "=========================================="
echo "Setup complete! Ready to push to GitHub."
echo "=========================================="
