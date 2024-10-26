# Webserver TODO

## For discussion - hot topics
- add mic pipeline
  - see TODO list -> Proof of concept
- database discussion 
  - brief, ensure none blocked, implementation feasible
- Raspi case
  - get it actually printed
- Component list
  - Is there a reason why we haven't ordered?
  - Might we want anything different?
- Website flow
  - see TODO list -> Website: user flow
- Discuss frontend impl
- Discuss login behavior
  - see TODO list -> Website: Increase security -> Security steps

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
  - [ ] Show we can send-recieve mic queries
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
- [ ] mic/recieve workflow
- [ ] Run on cloud
  - [ ] Discuss:
    - Will we have to change how our app is set up to get it deployed on a cloud machine? 
    - Do we have to buy a domain? Do just have an IP address? 
  - [ ] Actually get the system running on the cloud
- [ ] test NVIDIA jetson nano

### Order necessary components
- [ ] Make sure we have all components we may need
  - [ ] mic and speaker
  - [x] SD card 
  - [ ] jetson dongle

### Software Engineering - increase speed of development
- [ ] Add versions for all the python packages
- [ ] Refactor database layout - each version gets it's own dir

### Website: user flow
How should a user interact with our website?

- [ ] Discuss: Should we invest time in a fancy web framework?
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


### Website: Increase security

#### Security steps

- [ ] Discuss desired capabilities
  - Implemented login, create account
  - Delete account?
  - Change username?
    - race conditions? Be careful
  - Change password?
    - raspi must change creds... Can this be improved?
  - 2fa?
- [ ] Discuss how login flow should go
  - [ ] Discuss what should happen when someone deletes their account
  - [ ] Discuss what should happen when someone logs out
    - Should all things log out?
      - Kind of ok. Our scripts re-authenticate
      - I don't want to store 1000 tokens. Can we just store user+last logout for invalidation?
    - Should we have two different types of logins?
- [ ] Discuss potential improved database interface
  - Should we try to decouple fns that maybe involve both user/pw db and user/objs db? (imgs?)
- [ ] Discuss and implement http interfaces
  - [ ] Discuss what error codes should be
  - [ ] Discuss/research possible standard for error messages
    - jsonify vs not? "error" vs "msg"? error codes?
- [ ] Discuss how images should be encrypted
- [ ] Discuss potential optimizations
  - [ ] Should user be represented by single id number?
- [ ] Do we need a robot.txt
- [ ] Inspect edge case behaviors
  - Token rejected code (Standard?)
  - Token expired code (standard?)

#### Looking forwards
- Unless we are using https, our http requests pass unencrypted over the network. To prevent this, we should use https. To use https, we should configure nginx. To configure nginx, we need an SSL. To get an ssl "for free", we can go to "Let's Encrypt" For more information go to [THIS DOCUMENT](./notes_private/chattyg_response/ssl_encrypt.md)


### Performance testing: latency

#### Discovery
Designing testing methodology for concurrent testing:
- [ ] How does multithread gunicorn work
- [ ] How to ensure atomif read-modify-write
  - to objects?
  - to files?

#### Performance counters
- [ ] Discuss what performance counters we want
- [ ] Design performance counting in a way that won't slow everything down a ton
  - real-time?
  - interactive?
- [ ] Add the discussed performance counters

#### NVIDIA Jetson Nano: Get testing
- [ ] Could we literally run the whole system on a jetson?
  - [ ] Ensure tests fall within guidelines
    - observe latencies

#### Raspi: Get testing
- [ ] Could we literally run the whole system on a raspberry pi?
  - [ ] Ensure tests fall within guidelines
    - observe latencies

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
- ethan ml models, todo figure out testing method closer to real life use case


### Performance testing: data
- [ ] discuss what can be done to optimize data storage
  - check light levels
  - only people move things, delete any image where there isn't a person
  - check image difference (questionable)
- [ ] test storage over time with each optimization




### Documentation maintenance
- [ ] Isolate install instructions from run instructions
  - Excuse: waiting for design to solidify
- [x] Add documentation for dockerization
- [ ] Update the things in the repo level readme
- [ ] Ensure websierver-level readme is up to date
  - [ ] Ensure file diagram in README.MD are up to date
  - [ ] Ensure list of docs are up to date
- [ ] Document user workflow
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

### Not mine

#### Presentability
- [ ] Hardware
  - [ ] Design raspi case
  - [ ] Print raspi case
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

### Bug fix
- [x] When send full-quality raspi image, request_entity_too_large error
  - sends 1.2M images
  - soln: nginx.conf


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

** richard thomson?