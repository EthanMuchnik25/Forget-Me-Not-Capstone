# open python config.txt as json

import json
import subprocess
with open('config.json') as f:
    config = json.load(f)

print(config)

# run python command based on parameters
index = 0
for i in config:
    command = "python3 " + i["trainVal"]
    args = i["args"]
    for j in args:
        if type(args[j]) == str:
            command += " " + j + " " + args[j]
        elif type(args[j]) == bool:
            if args[j]:
                command += " " + str(j)
        else:
            command += " " + j + " " + str(args[j])
        # command += " " + j + " " + str(i[j])
    print(command)
    print(f"Starting command: {command}")
    
    # Run with output capture
    process = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Print output and error if any
    # print("STDOUT:", process.stdout)
    # print("STDERR:", process.stderr)
    # print(f"Return code: {process.returncode}")
    print("finished running command with index: ", index)
    index += 1
