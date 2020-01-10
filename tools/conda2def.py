#!/usr/bin/env python3

import sys
import argparse
import pprint
import yaml

def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)

def vprint(*args, **kwargs):
    if not opt.verbose:
        return 0 
    eprint(*args, **kwargs)

def makeDefFromYaml():
    print("""
Bootstrap: docker

From: continuumio/miniconda3

%files
 {0}

%environment
 PATH=/opt/conda/envs/{1}/bin:$PATH

%post
 echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc
 echo "source activate {1}" > ~/.bashrc
 /opt/conda/bin/conda env create -n {1} {2} {3}

%runscript
 exec "$@"
""".format(
    opt.env_file,
    env_name,
    channels_string,
    packages_string,
))
    

def makeDefFromList():
    pass

opt_parser = argparse.ArgumentParser(description='Create a Singularity definition file from a list of Conda packages')

opt_parser.add_argument('-e', '--env-file',
                        help='Conda environment file in YAML format')

opt_parser.add_argument('-c', '--channel',
                        help='Conda channel (when not using --env-file)',
                        action='append')

opt_parser.add_argument('-p', '--package',
                        help='Conda package(s) (when not using --env-file)',
                        action='append')


opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')


opt = opt_parser.parse_args()

if __name__ == '__main__':
    
    if opt.env_file != None:
        vprint('loading: {}'.format(opt.env_file))
        try:
            with open(opt.env_file, 'r') as stream:
                try:
                    data = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    eprint('\nFATAL YAML ERROR:\ntrying to parse <{}>:\n{}'.format(opt.env_file,exc))
        except Exception as exc:
                    eprint('\nFATAL ERROR:\nTrying to read {}:\n{}'.format(opt.env_file,exc))

        env_name = data['name']
        channels_string = ''
        packages_string = ''
        if opt.channel != None:
            for c in opt.channel:
                channels_string += ' -c {} '.format(c)

        for p in data['dependencies']:
            packages_string += ' {} '.format(p)

        makeDefFromYaml()
    else:
        if opt.package == None:
            eprint("FATAL ERROR:\nSpecify at least a package with -p PACKAGE (or env file)\nTry --help")
            exit()
        else:
            pass
