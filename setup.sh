#!/bin/bash

# ------------------------------------------------------------- #
#          Setup for the application dependencies               #
# ------------------------------------------------------------- #

# Create a virtual environment if none exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install required packages
pip install fastapi "uvicorn[standard]" gunicorn