# Raspi Runtime

This documentation is rudimentary because these scripts are in a rudimentary state I don't feel like spending a bunch of time writing.

### Setup

Probably run this in a virtual environment. Don't forget to:
```
python3 -m venv .venv
. ./.venv/bin/activate
pip3 install -r requirements.txt
```
However, note that everything may not install cleanly. If it complains about some header file, and you are running on linux, try running: 
```
sudo apt install portaudio19-dev
```
And rerunning the command to install requirement.txt.

It is needed for the python library that accesses your microphone. In the future, we may want to modularize this functionality. I don't know how microphones work.

TODO config.py is in a state of turmoil, document it once stabilized


## img_send

This file repeatedly takes images using whatever camera your device has, and attempts to send them to a running server's post_img endpoint.

---

Before running this, make sure you have a file called creds.txt, containing:
```
username
password
```
For an existing account. It should be located in the same directory as `img_send.py`

### Run

You should run `python3 img_send.py`

## mic_query

This file repeatedly tries to detect speech. Upon hearing keywords (currently 'hello capstone'), it sends these words to the server's speech query endpoint.

---

Before running this, make sure you have a file called creds.txt, containing:
```
username
password
```
For an existing account. It should be located in the same directory as `img_send.py`

### Run

You should run `python3 mic_query.py`