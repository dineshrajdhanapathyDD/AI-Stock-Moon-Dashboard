#!/bin/bash
export PYTHONPATH=/opt/python:/opt/python/lib/python3.9/site-packages:$PYTHONPATH
export DASH_DEBUG=False
export DASH_HOST=0.0.0.0
export PORT=${PORT:-8050}
export DASH_COMPRESS=True
export DASH_SERVE_LOCALLY=False

echo "Starting Stock Moon Dashboard..."
echo "Dashboard will be available at: http://$DASH_HOST:$PORT"

python3 app.py