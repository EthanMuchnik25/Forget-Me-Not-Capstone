# WEBSERVER README

This readme is the centralized area documenting the work I have done for the webserver. As of right now, everything is a bit disorganized, but I will probably try to organize everything in due time. 

To Organize:
1. File Structure - I want to make sure everything makes sense, and that docker is able to get up and running using this directory with no modifications.
2. Documentation - I would like to organize the documentation a bit more, e.g. add some tables of contents, put stuff in separate files. For example, this file contains install instructions, but they should probably go somewhere else. 

# Install Instructions

# To Run Server Locally:

## Python setup:

These instructions assume you have python already installed.

### Create python virtual environment:

Start by making a python virtual environment:
```
python3 -m venv .venv
```
This creates a python virtual environment in a directory called '.venv'.

### Activate python virtual environment:
Next, activate the environment by typing:
```
. .venv/bin/activate
```
You will always need to type this command when you open up a new terminal and want to run this python stuff locally.

### Install dependncies:

Now that you have the virtual environment set up, install the necessary dependancies by running:
```
pip3 install -r requirements.txt
```
This only needs to be run when you run the server for the first time. If you would like to add more dependancies to the project, add them to requirements.txt

## nginx setup:

Install nginx. On debian-based linux, this can probably be done with:
```
sudo apt-get update
sudo apt-get install nginx
```

Next, we need to ensure nginx is using the correct configuration file. By default, it uses the file in the symlink `/etc/nginx/sites-enabled/default`. We need to either comment out everything in the file, or delete it and replace it with our own. In our case, place `nginx.conf` in `/etc/nginx/sites-available`, symlink it to the `sites-enabled` directory, and delete/comment the default file.
```
sudo rm /etc/nginx/sites-enabled/default
sudo cp nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/
```

Afterwards make sure to reload nginx
```
sudo nginx -t # Test for syntax errors
sudo systemctl reload nginx # Reload nginx to apply changes
```
Note: systemctl may not work if you have a different linux setup. Ask chatgpt what to do in that case or something lmao.

To start nginx running, type:
```
sudo service nginx start
```

## Running gunicorn:

You should run something like:
```
gunicorn --workers 4 --bind 0.0.0.0:8000 myapp:app
```
`myapp` is the name of the python file containing the server stuff, and `app` is the name of the variable bound to `Flask(__name__)` inside the python file.

If we wish to handle websocket connections, we would need to modify something here. We might add a flag like --worker-class eventlet.


## Additional notes:
#### How to know if nginx is running:
```
sudo systemctl status nginx # or
sudo service nginx status
```
To check if the port is listening correctly, type:
```
sudo netstat -tuln | grep 80 # or
curl -I http://localhost
```

#### How to disable nginx run on system reboot
By default, nginx is set to run when your system reboots. To check if this is currently the case, type:
```
sudo systemctl is-enabled nginx
```

To turn this behavior off, type:
```
sudo systemctl disable nginx
```

#### For additional nginx notes and debugging tips, go [here](./notes/nginx_notes.md)


# To Run Server in Docker:

### The docker version is not complete yet! I still have yet to test it out.
