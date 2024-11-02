# WEBSERVER README

This readme is the centralized area documenting the work I have done for the webserver. As of right now, everything is a bit disorganized, but I will probably try to organize everything in due time. 

### IMPORTANT NOTE:
This project has a .env file which stores the API keys (and possible some other environment variables to be used in the project)\
As such, make sure that 
1. **You own a copy of the file**\
If you do not, obtain a copy through the gc
2. **You NEVER EVER commit a copy of the file**\
The git repository still stores old commits even if the current branch is not at that commit.



## Useful Instructions:

1. [How to setup/initialize the webserver component {Start here!}](./notes/install_instructions.md)
2. [API Documentation](./notes/api_useage.md)
2. [Useful Scripts](./notes/useful_scripts.md) Easy API send functions, time analysis scripts, etc..
2. [Server Layout]() What is where in the server?
2. [Some useful docker commands](./notes/docker_commands.md)

If you are looking for the microphone/camera scripts that need to be run on a raspberry pi, you are in the wrong place!\
Check [`../raspi-scripts/README.md`](../raspi-scripts/README.md).


## Directory Structure:
WARNING: This is extremely out of date!
```
/webserver
│
├── /static              # Static files - Flask automatically serves files from this directory
│   ├── a.css       # sample for ctrl+c ctrl+v
│   └── b.js        # sample for ctrl+c ctrl+v
│
├── /templates           # Template HTML webpages - sendable with flask fn render_template()
│
├── /notes              # Additional Documentation
├── /file_uploads       # Temporary directory to test file uploads
│
├── myapp.py            # Main Flask application
├── requirements.txt    # Add dependancies here
├── README.md           # Main project documentation
└── TEMP
```
TODO keep this up to date








