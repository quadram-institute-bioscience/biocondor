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
import datetime
from pprint import pprint

def downloads(package):
    total = 0

    for release in package['files']:
        total += release['ndownloads']
    return total

def downloads_per_version(package):
    """
    Return a dictionary of version -> downloads
    """
    downloads = {}
    for release in package['files']:
        downloads[release['version']] = release['ndownloads']
    return downloads


def import_date_from_json(datetime_string):
    (inputdate, zone) = datetime_string.split('+')
    return datetime.datetime.strptime(inputdate, '%Y-%m-%d  %H:%M:%S.%f')

def print_info(package):
    ColorPrint.print_info('Package_name:\t{}'.format(package['name']))
    attributes = {

 
        'latest_version': 'Version',
        'id': 'Bioconda_ID',
        'description': 'Description',
        'summary': 'Summary',
        'html_url': 'Bioconda_URI',
        'home': 'Package_URI',
        'docs_url':  'Documentation:',
        'ndownloads': 'Downloads',

    }
    for attr, label in attributes.items():
        if attr in package and package[attr] != None and package[attr] != '' and package[attr] != 'None':
            print("{}:\t{}".format(label, package[attr]))


    print("{}:\t{}".format('Downloads', downloads(package)))
    dpv = downloads_per_version(package)
    for version, download in dpv.items():
        print(" - {}:\t{}".format( version, download))

    if 'created_at' in package:
        created = import_date_from_json(package['created_at'])
        diff = datetime.datetime.now() - created
        print("Created:\t{} ({} days)".format(created.date(), diff.days))

    if 'modified_at' in package:
        edited = import_date_from_json(package['modified_at'])
        diff = datetime.datetime.now() - edited
        print("Modified:\t{} ({} days)".format(edited.date(), diff.days))

   

    print("Dependencies")
    for dep in package['files'][-1]['dependencies']['depends']:
        print(" - {}".format(dep['name']))
        for s in dep['specs']:
            print('   - ' + ' '.join(s))
             


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
        eprint("*** FATAL ERROR:\nUnable to load JSON from {}:\n{}".format(pathname, e))
        exit(1)

def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())

# Get script directory, and assume cache_dir is in ./bioconda_cache
script_dir = os.path.dirname(os.path.realpath(__file__))

 

# Script arguments
opt_parser = argparse.ArgumentParser(description='Read package json')

opt_parser.add_argument('-p', '--package', help="Package name")

opt_parser.add_argument('-c', '--cachedir',
                        help='Path to the cache directory[default: {}]'.format(os.path.join(script_dir, '../bioconda_cache')),
                        default=os.path.join(script_dir, '../biocondor_cache'))
 
opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')



opt = opt_parser.parse_args()


if __name__ == '__main__':
    if opt.package == None:
        eprint("Specify a package (-p)")
        exit(1)

    vprint(os.path.join(opt.cachedir, opt.package))
    package = loadJsonFile(os.path.join(opt.cachedir, opt.package + '.json'))

    print_info(package)

exit()
# Output is archived in a dictionary key: occurences
packages = {}
package_data = {}
keys = {}

regex = re.compile(opt.regex, re.IGNORECASE)
for package in bioconda:
    counters['total'] += 1
    for key in package:
        name = package['name']
        
        if isinstance(package[key], str) and regex.search(package[key]):
            match = regex.search(package[key])
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