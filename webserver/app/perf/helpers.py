import os


def get_max_log_dir_num(base_dir):
    # Ensure the base logs directory exists
    os.makedirs(base_dir, exist_ok=True)
    os.chmod(base_dir, 0o777)
    
    # List all subdirectories in the base logs directory
    existing_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    # Filter to only directories that are numeric
    numeric_dirs = [int(d) for d in existing_dirs if d.isdigit()]
    
    dir_number = max(numeric_dirs, default=0)
    
    return dir_number