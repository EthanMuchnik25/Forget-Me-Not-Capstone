#!/bin/bash

cd "$(dirname "$(readlink -f "$0")")"
CURRENT_DIR=$(pwd)

python3 -m venv .venv || { echo "Failed to create virtual environment"; exit 1; }

source ./.venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

chmod +x ./recurrent_script.sh

# CRON_SCRIPT="0 * * * * $CURRENT_DIR/recurrent_script.sh"
CRON_SCRIPT="* * * * * $CURRENT_DIR/recurrent_script.sh"


if ! crontab -l | grep -q "$CURRENT_DIR/recurrent_script.sh"; then
    (crontab -l; echo "$CRON_SCRIPT") | crontab - || { echo "Failed to add cron job"; exit 1; }
else
    echo "Cron job already exists."
fi
