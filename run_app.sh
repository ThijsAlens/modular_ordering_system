#!/bin/bash

# ------------------------------------------------------------- #
#                Run the full application                       #
# ------------------------------------------------------------- #

echo "Starting the application..."

# --- Activate Virtual Environment ---
# (Assuming venv is in the same directory as this script)
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    else
        echo "Error: venv/bin/activate not found."
        echo "Please run this script from the project root."
        exit 1
    fi
fi

# --- Check for development or production mode ---
if [ "$1" == "dev" ]; then
    # -----------------
    #  DEVELOPMENT MODE
    # -----------------
    echo "Starting application in development mode..."

    # Function to kill all child processes on exit
    cleanup() {
        echo -e "\nShutting down servers..."
        # 'kill 0' sends the signal to all processes in the script's process group
        kill 0
        echo "Done."
    }

    # Trap Ctrl+C (SIGINT) and script exit (EXIT) to run the cleanup function
    trap cleanup SIGINT EXIT

    # Start backend server in background with hot-reload
    echo "Starting backend server (dev) on http://127.0.0.1:8000..."
    uvicorn back_end.REST_API.main:back_end --reload --port 8000 &

    # Start front_end server in background with hot-reload on a different port
    echo "Starting front_end server (dev) on http://127.0.0.1:9000..."
    uvicorn front_end.REST_API.main:front_end --reload --port 9000 &

    echo "---------------------------------------------------"
    echo "Both servers running. Press Ctrl+C to stop them all."
    echo "Backend:  http://127.0.0.1:8000"
    echo "front_end: http://127.0.0.1:9000"
    echo "---------------------------------------------------"
    
    # Wait for any child process to exit, then the trap will clean up the rest
    wait -n

else
    # -----------------
    #  PRODUCTION MODE
    # -----------------
    echo "Starting application in production mode..."

    # Start backend server with Gunicorn in background
    # Binds to 0.0.0.0 to be accessible from outside (e.g., Nginx)
    echo "Starting backend server (prod) on http://0.0.0.0:8000..."
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 back_end.REST_API.main:back_end &
    
    # Start front_end server with Gunicorn in foreground
    # This keeps the script alive and attached to this process.
    echo "Starting front_end server (prod) on http://0.0.0.0:9000..."
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9000 front_end.REST_API.main:front_end
fi