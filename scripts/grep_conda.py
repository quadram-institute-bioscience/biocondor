#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Scan all packages for a regular expression
"""
import re
import json
import argparse
import os, os.path
import pdb
import sys

class ColorPrint:

    @staticmethod
    def print_fail(message, end = '\n'):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, end = '\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)

def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)

def vprint(*args, **kwargs):
    if not opt.verbose:
        return 0 
    eprint(*args, **kwargs)


def increment(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1

def count(key):
    increment(counters, key)

def loadJsonFile(pathname):
    try:
        #vprint("Loading JSON data from {}".format(pathname))
        with open(pathname, 'r') as f:
            data = json.load(f)   
            return data
    except Exception as e:
        eprint("Unable to load JSON from {}:\n{}".format(pathname, e))
        exit(1)

def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())
# Get script directory, and assume cache_dir is in ./bioconda_cache
script_dir = os.path.dirname(os.path.realpath(__file__))

 

# Script arguments
opt_parser = argparse.ArgumentParser(description='Generate BioCondor cache')


opt_parser.add_argument('-c', '--cachedir',
                        help='Path to the cache directory[default: {}]'.format(os.path.join(script_dir, '../bioconda_cache')),
                        default=os.path.join(script_dir, '../bioconda_cache'))

opt_parser.add_argument('-r', '--regex',
                        help="Regular expression",
                        required=True)

opt_parser.add_argument('-k', '--key',
                        help='Properties to be scanned (default: all)',
                        action='append')

opt_parser.add_argument('-m', '--margin',
                        type=int,
                        help="Extract MARGIN chars before and after the match",
                        default=35)
 
opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')



opt = opt_parser.parse_args()


# Check 'bioconda.json'
biocondafile = opt.cachedir + '/bioconda.json'

bioconda = loadJsonFile(biocondafile)

# Initialize counters
counters = {"total": 0, "has_key": 0, "is_defined":0, "is_string": 0, "is_valid": 0, "output": 0}

# Output is archived in a dictionary key: occurences
packages = {}
package_data = {}
keys = {}

regex = re.compile(opt.regex)
for package in bioconda:
    counters['total'] += 1
    for key in package:
        name = package['name']
        
        if isinstance(package[key], str) and regex.search(package[key]):
            match = regex.search(package[key], re.IGNORECASE)
            increment(keys, key)
            increment(packages, name)
            
            if not name in package_data:
                package_data[name] = {}
                package_data[name]['keys'] = []
            package_data[name]['keys'].append(key)
            if key != 'summary':
                package_data[name][key] = package[key]

            package_data[name]['summary'] = package['summary']
            match_context = ''
            if match != None:
                match_context = match.string[match.span()[0]-opt.margin:match.span()[1]+opt.margin]
                package_data[name]['match'] = match_context
            vprint ('#{}\t{}\t...{}...'.format(
                    name, key, 
                    match_context
                    ))
        


#https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
#    counters['output'] += 1
#    print('#{}\t{}\t{}'.format(counters['output'],strings[item], item))



for p in {k: v for k, v in sorted(packages.items(), key=lambda item: item[1],reverse=False) }:
    ColorPrint.print_pass('[{}]'.format(p), end='')
    print(' {} ({})'.format( package_data[p]['summary'], packages[p]))
    counters['output'] += 1
    if not opt.verbose:
        continue
    for key in package_data[p]['keys']:
        if key != 'summary':
            print('{}: {}'.format(key, package_data[p][key]))


eprint("{} packages found".format(counters['output']))