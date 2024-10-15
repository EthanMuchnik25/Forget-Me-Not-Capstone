# Install Instructions

This file contains instructions on how to install the webserver

### IMPORTANT NOTE:
This project has a .env file which stores the API keys (and possible some other environment variables to be used in the project)\
As such, make sure that 
1. **You own a copy of the file**\
If you do not, obtain a copy through the gc
2. **You NEVER EVER commit a copy of the file**\
The git repository still stores old commits even if the current branch is not at that commit.


# To run with Docker container

### Create Container

cd into this directory and type:
```
docker build -t myapp .
```
my_app is the container name, but you can rename it if you wish

Next, to run the container, type:
```
docker run -p 4000:80 myapp
```
Note that this commands sets port 80 of the docker container as port 4000 of your computer. In this case, you would have to access the website through [http://localhost:4000](http://localhost:4000). If you don't want to have to specify a port, map port 80 directly to port 80.

To enter the docker container like a shell, type:
```
docker exec -it myapp /bin/bash
```

One more potentially useful detail, we can mount a local volume to a docker container when we run it by adding:
```
-v $(pwd)/my-local-dir:/webserver
```
to the `docker run` command.

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

## Querying Server
The server can be sent requests locally at "http://127.0.0.1:8000" or "http://localhost"

To send requests from a different computer, type `ip addr show` in the terminal. The correct ip address is the one on the line starting with `inet`.\
Alternatively, `hostname -I` seems to work as well, pick the first ip address\
Once you have the ip address, you can send requests from a different computer at ["http://\<ip-addr\>"](http://<ip-addr>). 


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
