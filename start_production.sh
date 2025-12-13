#!/bin/bash
# Production startup script for Stock Moon Dashboard

export PYTHONPATH=/opt/python:$PYTHONPATH
export DASH_DEBUG=False
export DASH_HOST=0.0.0.0
export DASH_PORT=${PORT:-8050}
export DASH_COMPRESS=True
export DASH_SERVE_LOCALLY=False

echo "Starting Stock Moon Dashboard in production mode..."
echo "Dashboard will be available at: http://$DASH_HOST:$DASH_PORT"
echo "Loading optimized components..."

python app.py
