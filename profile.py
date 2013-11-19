import sys
import os
import argparse
from gevent import monkey
monkey.patch_socket()


def main():
    # adding treeherder module to the pythonpath
    treeherder_path = os.path.abspath('./treeherder-service')
    sys.path.append(treeherder_path)

    from profiler.log_parser import ParseLogProfiler

    parser = argparse.ArgumentParser(description='Profile a parse_log run on the given job type.')
    parser.add_argument('--jobtype', '-j',
                        type=str,
                        help='Tells the parser to select a log belonging to this job type',
                        choices=['build', 'mochitest', 'reftest', 'talos', 'all'],
                        required=True)
    parser.add_argument('--failing', '-f',
                        action='store_true',
                        default=False,
                        help='Tells the parser to select a log containing failures',
                        required=False)

    parser.add_argument('--output', '-o',
                        action='store',
                        default='stdout',
                        help='Tells the parser to output the profile data to this file.',
                        required=False)

    parser.add_argument('--configfile', '-c',
                        type=argparse.FileType('rt'),
                        default='log_sources.json',
                        help='Load the configuration from this file')

    args = parser.parse_args()

    profiler = ParseLogProfiler(args.configfile)
    profiler.run(args.jobtype, args.failing)
    if args.output == 'stdout':
        profiler.print_stats()
    else:
        profiler.dump_stats(args.output)


if __name__ == "__main__":
    main()
