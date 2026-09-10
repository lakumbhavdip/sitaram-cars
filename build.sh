#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# Apply database migrations (safe and non-destructive)
python manage.py migrate

# Optional: Auto-create dealer superuser only if credentials are provided and user does not exist
if [ -n "$DEALER_USERNAME" ] && [ -n "$DEALER_PASSWORD" ]; then
    python manage.py create_dealer
fi
