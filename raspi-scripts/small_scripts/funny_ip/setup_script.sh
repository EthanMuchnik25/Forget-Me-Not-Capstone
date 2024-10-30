#!/bin/bash

# NOTE: run with sh setup_script.sh

cd "$(dirname "$0")"
CURRENT_DIR=$(pwd)

echo "current dir $CURRENT_DIR"

echo "creating virtualenv"
python3 -m venv .venv || { echo "Failed to create virtual environment"; exit 1; }

echo "activating virtualenv"
. ./.venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

echo "installing dependancies"
pip install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

echo "chmod recurring script"
chmod +x ./recurrent_script.sh

CRON_SCRIPT="0 * * * * $CURRENT_DIR/recurrent_script.sh"
# CRON_SCRIPT="* * * * * $CURRENT_DIR/recurrent_script.sh"

echo "creating crontab"
if ! crontab -l | grep -q "$CURRENT_DIR/recurrent_script.sh"; then
    (crontab -l; echo "$CRON_SCRIPT") | crontab - || { echo "Failed to add cron job"; exit 1; }
else
    echo "Cron job already exists."
fi
