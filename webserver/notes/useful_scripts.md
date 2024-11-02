# Useful Scripts

This document primarily speaks about some of the useful files in the webserver/scripts directory.


TODO go through structure, what is in each directory

### `benchmarks/`
This directory will contain full benchmarks. As of right now, the workloads we can support, and objectives we can test are limited, as we don't have a "realistic workload". However, once we have one, it should go here.

### Proposed Workload Types
- Server Performance: Latency/throughput
  - In general, spam requests 
    - Varying or specific endpoints
  - Test Parallelism scaling for workers
  - Test latency differences in implementations
- Memory Workloads
  - Test optimizations
    - How many images/rows do we store
  - How low can we keep the memory footprint for large test runs
  - **Requires realistic trace**
- ML Accuracy Workloads
  - How many objects do we successfully detect and have available for the user to find when querying

### `helper/`
This directory contains some helper functions, which implement commonly used functionality. These include:
- `send_to_api.py`:
  - Wrappers around our server's api calls. Use these instead of creating the calls yourself
- `perf_parse.py`:
  - These help with parsing performance data.
- etc.

### `imgs/`
I place some sample images here for testing. You can put whatever you want here lol.

### `scripts/`
This directory should contain useful scripts that implement some complete, not-very-reuseable functionality. For example:
- `analyze_logs.py`
  - Prints out logs from a directory and number determined by cmdline args.
- `send_jpd_dir.py`
  - Sends the server `n` images from one directory. This is easier than having to list paths yourself.