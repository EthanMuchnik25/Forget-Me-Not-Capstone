import os
import argparse
import sys
sys.path.append('../')
# TODO see if we can from ..helper.perf_parse, also for the webserver if things
#  can be accessed relatively that would be good
from helper.perf_parse import get_run_dir, parse_log_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=int, default=None, help='Which log number to pull from')
    parser.add_argument('-d', type=str, default=None, help='Directory containing the log files')

    args = parser.parse_args()

    # Directory containing the log files
    log_directory = ""
    if args.d == None:
        # Pray this doesn't move
        log_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app/perf/logs'))
    else:
        log_directory = args.d

    log_directory = get_run_dir(log_directory, args.c)


    # Parse the logs and print the resulting map
    parsed_data = parse_log_files(log_directory)
    for key in parsed_data:
        # print(key, parsed_data[key])

        # Calculate averages
        l = parsed_data[key]
        print(key, sum([t[1] for t in l])/len(l), len(l))

if __name__ == '__main__':
    main()
