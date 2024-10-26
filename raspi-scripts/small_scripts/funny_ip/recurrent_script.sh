#!/bin/bash


cd "$(dirname "$(readlink -f "$0")")"
. ./.venv/bin/activate

python3 ip.py || { echo "failed to run python script" ; }