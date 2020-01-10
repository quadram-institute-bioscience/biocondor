#!/usr/bin/env python3

import sys
import argparse
import pprint
def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)

def vprint(*args, **kwargs):
    if not opt.verbose:
        return 0 
    eprint(*args, **kwargs)

opt_parser = argparse.ArgumentParser(description='Create a Singularity definition file from a list of Conda packages')

opt_parser.add_argument('-e', '--env-file',
                        help='Conda environment file in YAML format')

opt_parser.add_argument('-c', '--channel',
                        help='Conda channel (when not using --env-file)',
                        action='append')


opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')


opt = opt_parser.parse_args()

if __name__ == '__main__':
    for c in opt.channel:
        vprint(' - Adding channel {}'.format(c))
