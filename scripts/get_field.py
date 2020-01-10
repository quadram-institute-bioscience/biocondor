#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  A script to check all packages in bioconda.json cache and extract
  a specific key (e.g. 'license')
  It will print the values in abundance order, reporting
  if the key was found, if it was a string and not "None"...
"""
import json
import argparse
import os, os.path
import sys

def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)

def vprint(*args, **kwargs):
    if not opt.verbose:
        return 0 
    eprint(*args, **kwargs)


def loadJsonFile(pathname):
    try:
        #vprint("Loading JSON data from {}".format(pathname))
        with open(pathname, 'r') as f:
            data = json.load(f)   
            return data
    except Exception as e:
        eprint("Unable to load JSON from {}:\n{}".format(pathname, e))
        exit(1)

# Get script directory, and assume cache_dir is in ./bioconda_cache
script_dir = os.path.dirname(os.path.realpath(__file__))
default_cache_dir = os.path.join(script_dir, '../bioconda_cache')


# Script arguments
opt_parser = argparse.ArgumentParser(description='Generate BioCondor cache')


opt_parser.add_argument('-c', '--cachedir',
                        help='Path to the cache directory[default: {}]'.format(default_cache_dir),
                        default=default_cache_dir,)

opt_parser.add_argument('-k', '--key',
                        help='Property to be scanned',
                        required=True)

opt_parser.add_argument('-r', '--reverse',
                        help='Reverse output',
                        action='store_true')

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
strings = {}

for package in bioconda:
    counters['total'] += 1
    if opt.key in package:
        value = package[opt.key]
        counters['has_key'] +=1
        if value != None:
            counters['is_defined'] +=1
            if not isinstance(value, str):
                vprint("Not a string: {}\t{}\t{}".format(package['name'],type(value),value) )
            else:
                counters['is_string'] +=1
                if value != 'None' and value != 'none' and value != '':
                    counters['is_valid'] += 1
                    vprint("#{}\t{}\t{}".format(package['name'],type(value),value) )
                    if value in strings:
                        strings[value] += 1
                    else:
                        strings[value] = 1



reverse = not opt.reverse

#https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
for item in {k: v for k, v in sorted(strings.items(), key=lambda item: item[1],reverse=reverse) }:
    counters['output'] += 1
    print('#{}\t{}\t{}'.format(counters['output'],strings[item], item))


# Print counters to STDERR
eprint("""
Packages:      {}
 - With Key:   {}
  - Defined:   {}
   - String:   {}
    - Valid:   {}
""".format(counters['total'], counters['has_key'], counters['is_defined'],counters['is_string'], counters['is_valid']))