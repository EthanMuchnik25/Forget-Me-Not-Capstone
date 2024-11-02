# Server Layout

## Runtime

I may elaborate more on this section in the future

One very important detail is that worker processes are independant python PROCESSES. Any synchronization between them will be difficult, and probably require file locks. If possible, try to set up any relevant shared state before the processes fork off. See [gunicorn.conf.py](../gunicorn.conf.py).

## Architecture


### Entrypoint

The entrypoint to the server is located at `webserver/myapp.py`. This is what our gunicorn command latches onto. It greates the flask app, and imports `routes` from the `app/` directory.

Also importantly, the code in `gunicorn.conf.py` runs at app startup.

### `app/` Directory

Within the `app/` directory, the most important file is `routes.py`. This file contains all of our api endpoints for the flask app. If you would like to add an endpoint to the server, you would add it here. However, in general, try not to add all of the logic to the endpoint function. Use it mostly to extract/sanitize your inputs, and pass it onto some helper function.

As such, within the top level of the `app/` directory, there are other files which simply exist to take some of the logic out of `routes.py`. If you forsee yourself adding enough functionality to one of these files to justify adding more files, consider making a directory for the files.

### `database/` Directory

This directory contains all of our database implementations. Each database implementation should implement the same interface. 

#### `debug_db` Database

This is a very simple database I made, which stores files locally (unencrypted), and tables in JSON form when the server exits.

!!!**IMPORTANT**!!! This database wil not work for more than one worker. Do not try to use it as such.

#### TODO database

### `model/` Directory

This directory should be where our ML model code goes. For now it is not very fleshed out. In the future we will consider offloading inference work to a separate server to decrease latency.

### `perf/` Directory

This directory contains the code used to measure the performance of our code, and the directories where the timed runs are stored in file format.

A 'run' includes all of the timed calls made between when the server is started (with gunicorn) and stopped.

- `perf/logs/` Contains all runs
- `perf/logs/<num>/` Contains a single run. Higher nums mean more recent runs.
- `perf/logs/<num>/<pid>.log` Contains all the calls in a run for a single worker process.

For utilities to easily parse `perf` information see the [useful scripts](../notes/useful_scripts.md) document.



## Configs

There are multiple different ways to configure the server.

### config.py

This is a global config class that is included by many files in the server. It allows you to set fields such as
- What database is being used (debug, sqlite, etc.)
- Whether to have performance measurements on or off
- What hash function to use for authentication

### nginx.conf

This file contains settings for nginx, which routes incoming requests to our flask runtime. If you ever see an http error with nginx on it, it is likely you need to change something in the config.

### gunicorn

You can control a few properties through the launch command, such as:
- What ports the server will expect to use
- How many worker processes to spawn