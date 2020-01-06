#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, json
import argparse
import os
import sys
import time
import stat
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
        vprint("Downloading BioConda metadata")
        r = requests.get(url='https://api.anaconda.org/packages/bioconda')
        data = r.json()
    except Exception as e:
        eprint("FATAL ERROR: Unable to download BioConda metadata:\n {}".format(e))
        exit(2)
	
    try:
        with open(destination, 'w') as outfile:
            vprint("Saving BioConda metadata to {}".format(destination))
            outfile.write(json.dumps(data, indent=4, sort_keys=True))
    except Exception as e:
        eprint("FATAL ERROR: Unable to save BioConda metadata to {}:\n {}".format(destination, e))
        exit(2)


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
    vprint("bioconda.json is {} days old".format(age))
    if age > opt.dbdays:
        vprint("bioconda.json will be redownloaded...")
        copyfile(biocondafile, biocondafile + '.back')
        downloadBioconda(biocondafile)    
        
else:
    vprint("{} not found: downloading".format(biocondafile))
    downloadBioconda(biocondafile)
    


        


exit()
 
for i in data:
    name = i['name']
    filename ='{}/{}.json'.format(opt.outdir, name)
    vprint(" - Downloading {}".format(name) )
    r = requests.get(url='https://api.anaconda.org/package/bioconda/{}'.format(name))
    try:
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(r.json(), indent=4, sort_keys=True))
            #json.dump(data, outfile, indent=4)
    except Exception as e:
        eprint("Unable to save {} metadata to {}: {}".format(name, filename, e))
        exit(3)

