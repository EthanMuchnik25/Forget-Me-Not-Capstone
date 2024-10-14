# Installation Directions

## Hardware Installation
Here is the original documentation I found regarding how to install a camera, and what the commands in the python library do: [Important link](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/0)

## Software Installation (local)

Before running anything in this directory, this seems to be necessary to get the system to work:

```
sudo apt-get install libcap-dev
```

Everything in this directory should be run within a python virtual environment. Next, run this to create a virtual environment, and activate it:
```
python3 -m venv .venv
. ./.venv/bin/activate
```
The virtual environment should be activated whenever running something from this directory.


Run the following command installs python dependancies: 

```
pip3 install -r requirements.txt
``` 

## Software Installation (Docker)
TBD TODO