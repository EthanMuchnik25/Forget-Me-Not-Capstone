#!/bin/bash

# NOTE: run with bash ... , otherwise your shell will get nuked with wrong args

# Check if the user provided enough arguments
if [ $# -lt 3 ]; then
  echo "Usage: $0 <number_of_times> <server_address> <interval between image>"
  exit 1
fi

# Get the number of times to run the script from the first parameter
NUM_TIMES=$1

# Get the server address from the second parameter
SERVER_ADDRESS=$2

IMG_INTERVAL=$3

# Path to your Python script
SCRIPT_PATH="send_jpg_dir.py"

# Create a function to kill all background jobs when Ctrl+C is pressed
cleanup() {
  echo "Cleaning up... Killing all background jobs."
  # Kill all background jobs by their PID
  kill $(jobs -p) 2>/dev/null
  # exit 1
}

# Trap SIGINT (Ctrl+C) and call cleanup function
trap cleanup SIGINT

# Run the Python script the specified number of times
for ((i = 1; i <= NUM_TIMES; i++)); do
  echo "Running Python script $i/$NUM_TIMES with server address $SERVER_ADDRESS"
  python3 $SCRIPT_PATH -s $SERVER_ADDRESS -i $IMG_INTERVAL &
done

# Wait for all background jobs to finish (if running in parallel)
wait
echo "All $NUM_TIMES runs complete."
