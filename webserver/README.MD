# WEBSERVER README

This readme is the centralized area documenting the work I have done for the webserver. As of right now, everything is a bit disorganized, but I will probably try to organize everything in due time. 

To Organize:
1. File Structure - I want to make sure everything makes sense, and that docker is able to get up and running using this directory with no modifications.
2. Documentation - I would like to organize the documentation a bit more, e.g. add some tables of contents, put stuff in separate files. For example, this file contains install instructions, but they should probably go somewhere else. [done] 


## Useful Instructions:

1. [How to setup/initialize the webserver component {Start here!}](./notes/install_instructions.md)
2. Add additional later for components like fakes, etc


## Directory Structure:

```
/webserver
│
├── /static              # Static files - Flask automatically serves files from this directory
│   ├── a.css       # sample for ctrl+c ctrl+v
│   └── b.js        # sample for ctrl+c ctrl+v
│
├── /templates           # Template HTML webpages - sendable with flask fn render_template()
│
├── /fakes              # Contains dummy implementations of components
├── /notes              # Additional Documentation
├── /file_uploads       # Temporary directory to test file uploads
│
├── myapp.py            # Main Flask application
├── requirements.txt    # Add dependancies here
├── README.md           # Main project documentation
└── TEMP
```








