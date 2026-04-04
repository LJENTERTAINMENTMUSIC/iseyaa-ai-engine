#!/usr/bin/env bash

# setup_github.sh – initialize git repos and push to GitHub

set -e

# Prompt for GitHub username (default to current git config user.name)
read -p "Enter your GitHub username (default: $(git config user.name)): " GITHUB_USER
GITHUB_USER=${GITHUB_USER:-$(git config user.name)}

# Backend repository
cd "$(dirname "$0")/../iseyaa-ai-engine"
if [ ! -d ".git" ]; then
  git init
  git add .
  git commit -m "Initial commit – ISEYAA AI Engine"
fi
REPO_BACKEND="${GITHUB_USER}/iseyaa-ai-engine"
if ! gh repo view "$REPO_BACKEND" > /dev/null 2>&1; then
  gh repo create "$REPO_BACKEND" --public --source=. --push
else
  git remote add origin "https://github.com/$REPO_BACKEND.git" || true
  git push -u origin main
fi

# Frontend repository
cd "$(dirname "$0")/../iseyaa-web-core"
if [ ! -d ".git" ]; then
  git init
  git add .
  git commit -m "Initial commit – ISEYAA Web Core"
fi
REPO_FRONTEND="${GITHUB_USER}/iseyaa-web-core"
if ! gh repo view "$REPO_FRONTEND" > /dev/null 2>&1; then
  gh repo create "$REPO_FRONTEND" --public --source=. --push
else
  git remote add origin "https://github.com/$REPO_FRONTEND.git" || true
  git push -u origin main
fi

echo "✅ GitHub repositories created and initial code pushed."
