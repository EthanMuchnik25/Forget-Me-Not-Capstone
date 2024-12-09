#!/bin/bash

# Check if the user provided enough arguments
if [ $# -lt 2 ]; then
  echo "Usage: $0 <number_of_times> <server_address>"
  exit 1
fi

# Get the number of times to run the script from the first parameter
NUM_TIMES=$1

# Get the server address from the second parameter
SERVER_ADDRESS=$2

# Path to your Python script
SCRIPT_PATH="send_jpg_dir.py"

# Trap SIGINT (Ctrl+C) and call cleanup function
trap cleanup SIGINT

# Start the timer in nanoseconds
start_time=$(date +%s%N)

# Run the Python script the specified number of times
for ((i = 1; i <= NUM_TIMES; i++)); do
  echo "Running Python script $i/$NUM_TIMES with server address $SERVER_ADDRESS"
  python3 $SCRIPT_PATH -s $SERVER_ADDRESS -n 1 &
done

# Wait for all background jobs to finish (if running in parallel)
wait

# End the timer in nanoseconds
end_time=$(date +%s%N)

# Calculate elapsed time in nanoseconds
elapsed_time=$((end_time - start_time))

# Convert nanoseconds to seconds (with fractional part)
elapsed_time_sec=$(echo "scale=3; $elapsed_time / 1000000000" | bc)

# Print the total time taken in fractional seconds
echo "All $NUM_TIMES runs complete."
echo "Total time taken: $elapsed_time_sec seconds."
