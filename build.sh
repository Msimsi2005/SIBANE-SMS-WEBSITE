#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
#  Render build script
#  Runs once before the web process starts on every deploy.
# ──────────────────────────────────────────────────────────────
set -o errexit   # abort on any error

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate --no-input

echo "==> Creating admin user if needed..."
python manage.py ensure_admin

echo "==> Build complete."
