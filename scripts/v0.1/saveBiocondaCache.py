#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, json
import argparse
import os
import sys
import time
import stat
import pdb
from shutil import copyfile

"""
A program to download JSON metadata for BioConda and all its packages.
By default:
 - will re-download bioconda.json if not found or older than 3 days
 - will re-download {package}.json if bioconda has new
"""
def eprint(*args, **kwargs):
	"""print to STDERR"""
	print(*args, file=sys.stderr, **kwargs)	
	
	
def vprint(*args, **kwargs):
	"""print verbose text to STDERR"""
	if not opt.verbose:
	    return 0
	print(*args, file=sys.stderr, **kwargs)	
	
def fileAgeDays(pathname):
    return int( (time.time() - os.stat(pathname)[stat.ST_MTIME]) / 3600)
    
def downloadBioconda(destination):
    try:
        vprint("Downloading BioConda main file")
        r = requests.get(url='https://api.anaconda.org/packages/bioconda')
        r.raise_for_status()
        if 'application/json' not in r.headers.get('content-type', ''):
            eprint("FATAL ERROR: Invalid content type. Expected JSON, but got:")
            eprint(r.headers.get('content-type'))
            eprint("Response text was:")
            eprint(r.text)
            exit(2)
        data = r.json()
    except requests.exceptions.HTTPError as errh:
        eprint("FATAL ERROR: HTTP Error:", errh)
        exit(2)
    except requests.exceptions.ConnectionError as errc:
        eprint("FATAL ERROR: Error Connecting:", errc)
        exit(2)
    except requests.exceptions.Timeout as errt:
        eprint("FATAL ERROR: Timeout Error:", errt)
        exit(2)
    except requests.exceptions.RequestException as err:
        eprint("FATAL ERROR: Something Else", err)
        exit(2)
    except json.JSONDecodeError as e:
        eprint("FATAL ERROR: Unable to download BioConda metadata:\n ".format(e))
        eprint("Response text was:")
        eprint(r.text)
        exit(2)

    try:
        with open(destination, 'w') as outfile:
            vprint("Saving BioConda metadata to {}".format(destination))
            outfile.write(json.dumps(data, indent=4, sort_keys=True))
    except Exception as e:
        eprint("FATAL ERROR: Unable to save BioConda metadata to {}:\n ".format(destination, e))
        exit(2)
    return data

def downloadPackage(name, filename):
    vprint(" - Downloading {}".format(name) )
    r = requests.get(url='https://api.anaconda.org/package/bioconda/{}'.format(name))
    try:
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(r.json(), indent=4, sort_keys=True))
            vprint("OK")
    except Exception as e:
        eprint("Unable to save {} metadata to {}: {}".format(name, filename, e))
        exit(3)

def loadJsonFile(pathname):
    try:
        #vprint("Loading JSON data from {}".format(pathname))
        with open(pathname, 'r') as f:
            data = json.load(f)   
            return data
    except Exception as e:
        eprint("Unable to load JSON from {}:\n{}".format(pathname, e))
        exit(1)

def getCache(package):
    for i in data:
        if i['name'] == package:
            return i 
        
           
opt_parser = argparse.ArgumentParser(description='Generate BioCondor cache')


opt_parser.add_argument('-o', '--outdir',
                        help='Path to the output directory ',
                        required=True)

opt_parser.add_argument('-d', '--dbdays',
                        type=int,
                        help='Re-download bioconda.json if older than DAYS days',
                        default=3)
                        

                        
opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action="store_true")



opt = opt_parser.parse_args()

# Check output directory
if not os.path.isdir(opt.outdir):
    try:
        os.mkdir(opt.outdir)
    except Exception as e:
        print("Unable to create output directory {}".format(opt.outdir))
        exit(2)
    vprint("Created output directory: {}".format(opt.outdir))
else:
    vprint("Output directory found: {}".format(opt.outdir))
    
# Check 'bioconda.json'
biocondafile = opt.outdir + '/bioconda.json'

if os.path.isfile(biocondafile):
    age = fileAgeDays(biocondafile)
    
    if age > opt.dbdays:
        eprint("bioconda.json will be redownloaded: is {} days old".format(age))
        copyfile(biocondafile, biocondafile + '.back')
        data = downloadBioconda(biocondafile)    
    else:
        eprint("bioconda.json is only {} days old: skipping download".format(age))
        data = loadJsonFile(biocondafile)    
else:
    eprint("{} not found: downloading".format(biocondafile))
    data = downloadBioconda(biocondafile)
    


        
 
 
for i in data:
    name = i['name']
    filename ='{}/{}.json'.format(opt.outdir, name)
    
    if os.path.isfile(filename):
        vprint("'{}' found in {}: checking for updates...".format(name,filename))
        package = loadJsonFile(filename)
        cached = getCache(name)
        if ( (package['latest_version'] == cached['latest_version']) and (package['revision'] == cached['revision'])):
            vprint("Cached version {}, rev {} is already updated".format(package['latest_version'],cached['revision']))
        else:
            vprint("Downloading new package {}: cached version {}/{} is different from BioConda ({}/{})".format(
                name,
                cached['latest_version'], cached['revision'],
                package['latest_version'], package['revision']         ))
            downloadPackage(name, filename)
    else:
        vprint("Downloading new package {}".format(name))
        downloadPackage(name, filename)
    
 
