# Webserver TODO

## For discussion - hot topics
- implement real mic pipeline?
- "realistic trace?"
- database discussion 
  - check extra features?
- Raspi case
  - test?
- Website flow
  - see TODO list -> Website: user flow
  - Discuss frontend impl
  - Discuss login behavior
    - see TODO list -> Website: Increase security -> Security steps
- ML - ethan training

## TODO list

This hopes to document some of the things we probably eventually have to get sorted out

### Bug fix
- [ ] Demo database iterates through images in forwards-time order instead of reverse-time order I think
- [ ] It seems like YOLO resizes the images to only work on 384x640
  - Is this intentional?
  - If so, should we decrease image size?

### Proof of concept
(Mostl are done - see Complete)
- [ ] Mic pipeline
  - [x] Show we can send-recieve mic queries
  - [ ] Show we can reason on mic queries
    - Is it easier to do this in the context of the system?
    - Do we need additional components?
      - A list of possible objects?


### Objective: Get a fully functional system up and running
- [x] Design decisions cleared up
  - [x] database remote/local, sql/nosql, 
- [x] Docker containerize app, we have made modularity a priority
- [ ] Database solidified and implemented
  - [x] Mock database made
  - [ ] Real databases implemented
    - [ ] SQLITE
    - [ ] RDS
- [x] mic/recieve workflow
- [ ] Run on cloud
  - [ ] Discuss:
    - Will we have to change how our app is set up to get it deployed on a cloud machine? 
    - Do we have to buy a domain? Do just have an IP address? 
  - [ ] Actually get the system running on the cloud
- [x] test NVIDIA jetson nano
  - I give up this shit was stupid
  - weekly writeup material in the text file

### Order necessary components
- [ ] Make sure we have all components we may need
  - [ ] mic and speaker
  - [x] SD card 
  - [x] jetson dongle

### Software Engineering - increase speed of development
- [ ] Add versions for all the python packages
- [x] Refactor database layout - each version gets it's own dir
- [ ] Re-refactor database layout
  - [ ] 1 table for all users
  - [ ] no tuples to strings, col for each
  - [ ] integer ids
    - one table has per-user info: uname -> id | pw
    - other has id -> [object record]
  - [ ] don't open and close connection every time?

### Website: user flow
How should a user interact with our website?

- [x] Discuss: Should we invest time in a fancy web framework?
- [ ] Implement basic web framework
- [ ] What pages should our website have?
  - Will we have a top-level website? Must we buy a domain?
  - home page, login, auth, eventually our other webpage
  - do urls make sense?
- [ ] How should UI look? 
  - [ ] How should users be able to find what they want?
    - Thumbnails?
    - Date entry?
    - Dropdown?
    - Should users be able to pick which cameras to search?
      - Many policy ideas required to implement this... table join? weird query?
- [ ] What differences should there be for web vs local versions?
  - How can I implement those differences?
- [ ] UI sketches
- [ ] Discussion points for when frontend is implemented 
  - How exactly should the average api response look?
  - What code does what?
    - 422 -> no auth?
    - 400 -> bad? more specific necessary?
    - 200 -> good? more specific necessary?
  -  differentiate between no error and create successful
    - 300 -> exists for some purpose? check...


### Website: Increase security

#### Security steps

- [x] Discuss desired capabilities
  * RESULT: KISS for now -> add/delete user, login/logout
  - Implemented login, create account
  - Delete account?
  - Change username?
    - race conditions? Be careful
  - Change password?
    - raspi must change creds... Can this be improved?
  - 2fa?
- [ ] Discuss how login flow should go
  - [x] Discuss what should happen when someone deletes their account
  - [x] Discuss what should happen when someone logs out
    - Should all things log out?
      - Kind of ok. Our scripts re-authenticate
      - I don't want to store 1000 tokens. Can we just store user+last logout for invalidation?
    - Should we have two different types of logins?
- [x] Discuss potential improved database interface
  - Should we try to decouple fns that maybe involve both user/pw db and user/objs db? (imgs?)
- [ ] Discuss and implement http interfaces
  - [ ] Discuss what error codes should be
  - [ ] Discuss/research possible standard for error messages
    - jsonify vs not? "error" vs "msg"? error codes?
- [ ] Discuss how images should be encrypted
- [x] Discuss potential optimizations
  - [x] Should user be represented by single id number?
- [ ] Do we need a robot.txt
- [x] Inspect edge case behaviors
  - Token rejected code (Standard?)
  - Token expired code (standard?)
    - both are same
  

#### Looking forwards
- Unless we are using https, our http requests pass unencrypted over the network. To prevent this, we should use https. To use https, we should configure nginx. To configure nginx, we need an SSL. To get an ssl "for free", we can go to "Let's Encrypt" For more information go to [THIS DOCUMENT](./notes_private/chattyg_response/ssl_encrypt.md)


### Performance testing: latency

#### Performance counters
- [x] Discuss what performance counters we want
- [x] Design performance counting in a way that won't slow everything down a ton
  - real-time?
  - interactive?
- [ ] Add the discussed performance counters

#### Raspi: Get testing
- [ ] Could we literally run the whole system on a raspberry pi?
  - [ ] Ensure tests fall within guidelines
    - observe latencies
- [ ] Check scaling for parallel
- [ ] inspect for bottleneck

#### Cloud: Get testing
- [ ] Make sure testing perf runs on cloud
  - [ ] Ensure tests fall within guidelines
- [ ] Discover what components are taking up most of each resource
  - [ ] Is model in memory once per thread?
  - [ ] Are things parallelizing the way we expect?
- [ ] Test scalability
  - [ ] Build framework to test stress test our systems
    - Spawn many querying users
    - Submit many images from many users to many users
    - ***** Investigate amazon Selenium!!!  ****
  - [ ] Run tests
    - How many of each thing can we spawn until we saturate machine?
    - How What could be decoupled?


### Performance testing: accuracy
- [ ] Ethan is on it! ?
  - ethan ml models, can help us make traces... 
  - [ ] todo figure out testing method closer to real life use case


### Performance testing: data
- [ ] come up with """normal trace"""



### Optimizations
- [ ] Discuss optimizations, implement, and test
  - [ ] Data storage
    - check light levels
    - only people move things, delete any image where there isn't a person
    - check image difference (questionable) (maybe less questionable for 1 camera)
    - NOTE: testing should be done once we have """normal trace"""
  - [ ] Latency
    - FIRST TEST LATENCY and then determine what path to take
    - Pending:
      - Tensorrt
      - Model server
        - impl
          - internal queue (file locking?)
          - maybe no model process is fine?
          - grpc server?
          - celery for async?
          - triton?
        - framework
          - tensorrt?
          - onnx?
            - GPT says faster on cpu
          - Can do both!
      - Database optimization
  - [ ] Model
    - Quantization?
    - tensorrt?
  


### Documentation maintenance
- [ ] Isolate install instructions from run instructions
  - Excuse: waiting for design to solidify
- [x] Add documentation for dockerization
- [ ] Update the things in the repo level readme
- [ ] Ensure websierver-level readme is up to date
  - [ ] Ensure file diagram in README.MD are up to date
  - [ ] Ensure list of docs are up to date
- [x] Document user workflow
  - Good for end users also
- [ ] Improve documentation for groupmates
  - [ ] Document how authentication is done
    - [ ] For the purposes of DB
      - tokens, expiring, etc.
    - [ ] For the purposes of FE
      - index.html, id token
- [ ] Clean up repository
  - webserver/app/random_scripts?
- [ ] webserver/app/database/debug_db/convenient_scripts
- [ ] document anything someone would need to get up and running with the system
  - [ ] document the raspi script 
  - [ ] document the convenient script for testing -> modify the convenient script so that it makes an account

### Not mine

#### Presentability
- [ ] Hardware
  - [x] Design raspi case
  - [x] Print raspi case
  - [ ] Test raspi case
  - [ ] Repeat above steps


## Design decisions
- [ ] Make a stored record for design decisions that happened
- Current list
  - jwt over flask-login due to transparency, flask uses things in a funny pythonic way
  - TODO



## Completed

### MVP System
We need a basic system up and running before we can elaborate on specific improvements/desired behaviors

### Proof of concept
- [x] Webserver
  - Show we can send/recieve basic request from a different machine
  - Show we can send files, recieve files
- [x] raspi
  - Show we can take photos and send them to a different machine
- [x] Database - show we can store something in a database
  - rds
  - sqllite

### Objective: Get a bunch of useful mocks up and running
- [x] Dummy webserver implementation
  - no real database, 
  - no real yolo
    - mock out YOLO so we know what to send to the database
  - GPT website
    - Get a dumb website with just a query field and an image response/text field up and running
  - mock raspi for local testing purposes
- [x] image workflow

### Software Engineering - increase speed of development

#### Dockerization
- [x] Dockerize project for universal env
- [x] Create prod vs debug dockerfile
  - Prod should just run exactly how we want it to go in production
  - Debug should take in curr repository state so we don't have to edit from within the docker container, and so we don't have to keep rebuilding it

### Authentication

#### Complete initial implementation
- [x] Create login/register screen
- [x] Create new database interface functions + implementation
- [x] Create new authenticated send for raspi
- [x] Refactor old server code to use authentication
- [x] Refactor old website to use authentication
- [x] Implement logout
  - [ ] Implement token blocklist
- [x] Implement delete account

### Bug fix
- [x] When send full-quality raspi image, request_entity_too_large error
  - sends 1.2M images
  - soln: nginx.conf

### Performance Testing: latency

#### Discovery
Designing testing methodology for concurrent testing:
- [x] How does multithread gunicorn work
  - RESULT: each gunicorn is a separate process
- [x] How to ensure atomif read-modify-write
  - RESULT: use a database, store all shared state in a database
  - to objects?
  - to files?

#### NVIDIA Jetson Nano: Get testing
- [x] Could we literally run the whole system on a jetson?
  - [x] Ensure tests fall within guidelines
    - observe latencies
  - RESULT: Giving up on this shit


## Personal notes dump
#### Useful sites:
nginx beginners guide: http://nginx.org/en/docs/beginners_guide.html\
flask mega tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux\
flask quickstart: https://flask.palletsprojects.com/en/3.0.x/quickstart/\
bottom text

## Dump

TODO maybe document jwt...\\
Has fields like this, look in jwt_claims:
```
{
  "message": "You have access to this protected route!",
  "current_user": "testuser",
  "jwt_claims": {
    "exp": 1634567890,
    "iat": 1634564290,
    "jti": "1234567890abcdef",
    "sub": "testuser",
    "fresh": false,
    "type": "access"
  }
}
```
Claims can be found by doing get_jwt in flask app\
Tokens in my case can be manually blacklisted until they expire, but afterwards it is useless to keep them alive.


Right now raspi requires some manual setup:
-> pip install libraries
-> maybe install audio library that python uses


***document the things that everyone has to use
- sending photos
  - add in instructions all the way from the base readme... if there is time
- functionality that I have added
  - logging (how to user perf)
  - analysis script
- update locations
- new gunicorn command
  - new gunicorn command modifiers
- debug database
  - limitations (1 worker)
- where to find camera script
- configs
  - config.py
  - nginx
    - img size
  - gunicorn
    - port
- raspi scripts
  - yep



more database dump:
- blob storage
- indexing
- connection reuseage
- sqlite is sorta aids but at least code is similarly shaped as other relational databases
  - locks entire files

Workloads dump:
create "workloads"
own folders
- performance workloads doesn't matter which images to pick from, just have a pool, and spawn varying amounts of spammers
- memory workloads should be real traces
 - check model detection differences on nearly identical input images, or a series
  - ideally try to correlate at what image difference does the model detect more differences
 - use stats to drive eviction policies
  - maybe have second optimization where if nothing new detected after running model, don't save
  - test how old images get, image amnt in filesystem, etc.

To code
- database update (subset)
- modularize logging init
- optionalize authentication
  - nontrivial, queries change depending on auth, they use username
  - use fn defaults (a little brittle)
- workloads (above)
- take time of processes




DUMP:
logging instructions dump:

    # NOTE:
    # Log folders, located in webserver/app/perf/logs, contain all logs for a single
    #  run of the server. This function determines the name of the next log folder.
    #  It should be 1 greater than the last log directory.
    # The log folder is made in gunicorn.conf.py, this just finds it

eventually test optimizations

input sanitization

Make a module for send fns?
refactor raspi scripts to use std send functions?

make functionality to wipe a database

