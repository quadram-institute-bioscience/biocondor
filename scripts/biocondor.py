#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, json
import pdb
import codecs


def getBiocondaPackageInfo(PackageName):
    """
    getBiocondaPackageInfo(PackageName):
     - PackageName: Str, Name of the 'bioconda' package
     
    Output:
     - Raw JSON answer from anaconda API
    """
    if PackageName == None:
        return 0
        
    r = requests.get(url='https://api.anaconda.org/package/bioconda/{}'.format(PackageName))
    return r.json()
    
def printPackage(PackageName):
    json = getBiocondaPackageInfo(PackageName)
    return ''.format()

try:
    with open('bioconda.json', mode="r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        print("Loaded")
except Exception as e:
    print('{}'.format(e))
    exit()
    r = requests.get(url='https://api.anaconda.org/packages/bioconda')
    data = r.json()
    print("Downloaded")


#[u'app_entry', u'package_types', u'full_name', u'owner', u'home', 
#u'source_git_url', u'id', u'app_type', u'source_git_tag', u'app_summary', 
#u'public', u'revision', u'conda_platforms', u'description', u'html_url', u'name',
# u'dev_url', u'builds', u'license', u'versions', u'url', u'latest_version', u'summary', 
#u'license_url', u'doc_url']
c=0
for i in data:
    c+=1
    print('{}\t{}:{}'.format(c,i['name'], i['latest_version']))
    print('{} ({})\nHome:\t{};{}\nDescription:\t{}\nSummary:\t{}'.format(
        i['full_name'], i['id'], 
        i['home'], i['source_git_url'],
        i['description'],
        i['summary']

    ))
    print('')
    package = getBiocondaPackageInfo(i['name'])
    print('{}'.format({}))
    assert()
    print('-')


