#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Seed dealership settings and sample cars (safe: checks if exist)
python manage.py seed_data

# Optional: Auto-create dealer superuser if env vars are provided
if [ -n "$DEALER_USERNAME" ] && [ -n "$DEALER_PASSWORD" ]; then
    python manage.py create_dealer
fi
