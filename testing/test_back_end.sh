#!/bin/bash

echo "Starting venv, servers, and running tests..."

# --- Activate Virtual Environment ---
# (Path is relative to the script's location *before* cd)
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "../venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        source ../venv/bin/activate
    else
        echo "Error: ../venv/bin/activate not found."
        echo "Please make sure the venv is in the parent directory."
        exit 1
    fi
fi

# --- Change to Project Root ---
# This is vital for Python imports AND all relative file paths
echo "Changing to project root directory..."
cd ..

# --- Cleanup Function ---
# This will run when the script exits (from trap)
cleanup() {
    echo -e "\nShutting down servers..."
    # 'kill 0' sends the signal to all processes in the script's process group
    kill 0
    echo "Done."
}

# Trap script exit (EXIT) to run the cleanup function
trap cleanup EXIT

# --- 1. Start Server ---
echo "Starting backend server (dev) on http://127.0.0.1:8000..."
uvicorn back_end.REST_API.main:back_end --reload --port 8000 &

# --- 2. Wait for Server to be Ready ---
echo "Waiting for server to be ready (pinging http://127.0.0.1:8000/docs)..."
# We ping the /docs endpoint until it returns a 200 OK
# --silent: Don't show progress
# --fail: Exit with an error if the HTTP code is not 2xx
# > /dev/null: Dump the (successful) HTML output
while ! curl --silent --fail http://127.0.0.1:8000/docs > /dev/null; do
    printf "."
    sleep 1
done

echo -e "\nServer is up!"

# --- 3. Run Python Tests ---
echo "---------------------------------------------------"
echo "Running testing/test_back_end.py..."
echo "---------------------------------------------------"

# We run the test script *from the root directory*,
# so we must include the 'testing/' path.
python testing/testing_back_end.py

# --- 4. Shutdown ---
echo "---------------------------------------------------"
echo "Tests finished. Shutting down."
echo "---------------------------------------------------"

# The script will now exit, which automatically triggers
# the 'trap' and runs the 'cleanup' function.