# Optimizations Doc

This doc will hopefully contain a concrete list of optimization we can do, explained in more detail than I wish to permit in the TODO doc.

### Important!
For any feature here, basically the only way we can test its effectiveness (which is something we want to do, more datapoints on more graphs) is by running against a "realistic" trace, where we expect to be able to find certain items in certain circumstances. We should really try to make these traces, and make running them automated if possible.

## Image Storage Optimizations

### Send/store less images initially

#### Camera-Side
(assuming no model on camera (initially))
- Darkness level
- Image Difference
  - Since last sent?
  - Since last taken?

#### Server-Side
- Person present
  - in practice only people can move objects?


### Clean up more images
- TODO: determine policies

## Latency Optimization

#### Important!
For this, I meed the latency benchmarking system working. First figure out what we need to iron out before we can implement latency benchmarking.

### Line storage location
- Which camera vs. user model do we support?
  - 1 camera 1 person
  - 1 camera many person (mandatory non server case)
  - ** many camera 1 person (1 account per household
  - ** many camera many person)
    - Should db lines go per person or per camera
      - Per person means easy query last 100, but duplicated state
      - Per camera saves space, but hard/slow to find "last 35 imgs" compared to before
  - Has impacts on system latency

### ML processing latency
- Can ml processing be delayed?
  - Must ensure latency bounds met
- How would we implement this?
  - New server, server frontend sends reqs to backend server so it can return earlier
  - Somehow have a worker thread on the same server
    - Less scalable


### General perf measurement
- We will probably end up trying to optimize whatever is actually the slowest, amdahl
- TensorRRT?

## Authentication Policy Decisions
- Does camera store plaintext account pass?
- Does camera store permanent 1-time, requires manual login
TODO continue



======

TODO prioritize optimizations
plaintext raspi and log everyone out



-> if we do local 
-> 

deleting an account should wipe everything from the database