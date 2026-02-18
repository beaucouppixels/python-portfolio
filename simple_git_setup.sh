#!/bin/bash

# Simple Git Setup Script (No GitHub CLI required)

echo "=========================================="
echo "Git Repository Setup"
echo "=========================================="
echo ""

# Step 1: Organize files
echo "Step 1: Organizing files..."
mkdir -p webscraper
if [ -f "Webscrapper.py" ]; then
    cp Webscrapper.py webscraper/webscrapper.py
    echo "✓ Copied webscrapper.py to webscraper/ folder"
else
    echo "⚠ Webscrapper.py not found"
fi

# Step 2: Initialize Git
echo ""
echo "Step 2: Initializing Git..."
if [ -d ".git" ]; then
    echo "⚠ Git already initialized"
else
    git init
    echo "✓ Git initialized"
fi

# Step 3: Add files
echo ""
echo "Step 3: Staging files..."
git add .
echo "✓ Files staged"

# Step 4: Show what will be committed
echo ""
echo "Files to be committed:"
git status --short

# Step 5: Commit
echo ""
echo "Step 4: Creating commit..."
git commit -m "Initial commit: Add intelligent web scraper

- Production-ready web scraper with retry logic and error handling
- Multi-site support with flexible CSS selectors
- Comprehensive documentation and setup guides
- MIT licensed for open-source use"

echo "✓ Commit created"

echo ""
echo "=========================================="
echo "NEXT: Create GitHub Repository"
echo "=========================================="
echo ""
echo "1. Go to: https://github.com/new"
echo ""
echo "2. Fill in these details:"
echo "   Repository name: python-portfolio"
echo "   Description: Production-ready Python projects demonstrating web scraping, automation, and AI integration"
echo "   ✓ Public"
echo "   ✗ DO NOT check 'Add a README file'"
echo "   ✗ DO NOT add .gitignore"
echo "   ✗ DO NOT choose a license"
echo ""
echo "3. Click 'Create repository'"
echo ""
echo "4. GitHub will show you commands. Come back here and run:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/python-portfolio.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Replace YOUR_USERNAME with your actual GitHub username!"
echo ""
echo "=========================================="
