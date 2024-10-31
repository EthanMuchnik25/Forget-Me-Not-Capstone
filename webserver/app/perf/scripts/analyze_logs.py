import os

def parse_log_files(directory):    # Dictionary to hold the results
    name_map = {}
    # TODO have a second name map that maps the thing to none if its not there
    
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

# Directory containing the log files
log_directory = "../logs/1"

# Parse the logs and print the resulting map
parsed_data = parse_log_files(log_directory)
print(parsed_data)
