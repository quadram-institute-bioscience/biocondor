#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate a bioconda cache file for all the packages in the bioconda channel.
Updated version 2021
"""

import os, sys
import json
import requests
import argparse
import logging
from rich.console import Console
from rich.progress import track

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def getJsonFromUrl(uri):
    """
    Get the json from the url.
    """
    response = requests.get(uri)
    if response.status_code == 200:
        logging.info("Downloaded Json data from: " + uri)
        return response.json()

    else:
        logging.error("Error downloading URI {}: {}".format(uri, response.status_code))
        return None

def getSubdirsFromDict(dict, subdir):
    dirs = []
    for f in dict['tree']:
        if f['path'].startswith(subdir + '/') and f['type'] == 'tree':
            path_parts = f['path'].split('/')
            dirs.append(path_parts[1]) if len(path_parts) == 2 else None
    return dirs

def getBiocondaRecipe(recipe):
    """
    Get the bioconda recipe from the bioconda channel.
    """
    uri = "https://api.anaconda.org/package/bioconda/" + recipe
    return getJsonFromUrl(uri)

def validJsonFile(filename):
    """
    Check if the json file is valid.
    """
    try:
        with open(filename) as json_file:
            json.load(json_file)
            return True
    except ValueError as e:
        logging.error("Error parsing JSON file: " + filename)
        return False
    except IOError as e:
        logging.error("JSON file not found: " + filename)
        return False
    

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Generate a bioconda cache file for all the packages in the bioconda channel.')
    args.add_argument('-o', '--output', help='Output directory', default='biocondor_cache')
    args.add_argument('-l', '--log', help='Log file', default='biocondor_cache.log')
    args.add_argument('--verbose'    , help='Print more information', action='store_true')
    opts = args.parse_args()


    # Rich console
    console = Console()

    # Create log file
    if opts.verbose:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    # Set log format
    logging.basicConfig(filename=opts.log, filemode='w', level=logging_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')


    # Create output directory
    if not os.path.exists(opts.output):
        try:
            os.makedirs(opts.output)
        except OSError as e:
            logging.error("Error creating output directory %s: %s" % opts.output, e)
            sys.exit(1)
        
        logging.info("Creating output directory: %s" % opts.output)
    else:
        logging.warning("Output directory already found: {}".format(opts.output))

    github_dirs = getJsonFromUrl('https://api.github.com/repos/bioconda/bioconda-recipes/git/trees/master?recursive=1')
    recipes = getSubdirsFromDict(github_dirs, 'recipes')

    for recipe in track(recipes, description="Downloading...", total=len(recipes)):
        # Update progressbar name
        
        
        outputfile = os.path.join(opts.output, recipe + '.json')


        if not validJsonFile(outputfile):
            logging.info("Downloading recipe: " + recipe)
            data = getBiocondaRecipe(recipe)
            if data is not None:
                with open(outputfile, 'w') as f:
                    json.dump(data, f)
            else:
                logging.error("Error downloading recipe: {}".format(recipe))
                continue
        else:
            logging.info("Recipe already downloaded: {}".format(recipe))