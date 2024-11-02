import os


# NOTE: It is a massive pain to try to import anything from the webserver, my 
#  code could have been better designed for monitoring. This is duplicated but
#  I don't have enough time to worry about it
def get_max_log_dir_num(base_dir):
    # Ensure the base logs directory exists
    if not os.path.isdir(base_dir):
        raise Exception(f"Directory {base_dir} does not exist")
    
    # List all subdirectories in the base logs directory
    existing_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    # Filter to only directories that are numeric
    numeric_dirs = [int(d) for d in existing_dirs if d.isdigit()]
    
    dir_number = max(numeric_dirs, default=0)
    
    return dir_number


# Directory should be the directory containing log for all runs
# If idx not provided, get most recent
def get_run_dir(directory, idx=None):
    dirnum = idx
    if idx == None:
        dirnum = get_max_log_dir_num(directory)
    
    return os.path.join(directory, str(dirnum))

    

# Returns a map of function names to a list of tuples (PID, execution time)
def parse_log_files(directory):
    # Dictionary to hold the results
    name_map = {}
    
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r') as file:
                for line in file:
                    # Split the line into components (PID, name, time)
                    parts = line.strip().split()
                    if len(parts) != 3:
                        continue  # Skip lines that don't have the correct format
                    
                    try:
                        pid = int(parts[0])
                        name = parts[1]
                        time = float(parts[2])
                        
                        if name not in name_map:
                            name_map[name] = []
                        
                        name_map[name].append((pid, time))
                    except ValueError:
                        # Skip lines with invalid numbers
                        continue
    
    return name_map
