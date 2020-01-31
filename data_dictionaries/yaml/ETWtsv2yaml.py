#!/usr/bin/env python3

# Author: Roberto Rodriguez (@Cyb3rWard0g)
# License: GPL-3.0

import csv
import yaml
import json
import glob
from collections import OrderedDict
import os
import re
import argparse

# Bannner
print(r"""
________________________      __   __                ________  
\_   _____/\__    ___/  \    /  \_/  |_  _________  _\_____  \ 
 |    __)_   |    |  \   \/\/   /\   __\/  ___/\  \/ //  ____/ 
 |        \  |    |   \        /  |  |  \___ \  \   //       \ 
/_______  /  |____|    \__/\  /   |__| /____  >  \_/ \_______ \
        \/                  \/              \/               \/
_____.___.  _____      _____  .____                            
\__  |   | /  _  \    /     \ |    |                           
 /   |   |/  /_\  \  /  \ /  \|    |                           
 \____   /    |    \/    Y    \    |___                        
 / ______\____|__  /\____|__  /_______ \                       
 \/              \/         \/        \/  V0.1
 
 Creator: Roberto Rodriguez @Cyb3rWard0g
 License: GPL-3.0
 """)

# Initial description
text = "This script allows you to translate and transform etw tsv files to yaml files.."
example_text = '''example:

 python3 ETWtsv2yaml -d Windows10EtwEvents/ -o yaml/
 '''
# Initiate the arguments parser
parser = argparse.ArgumentParser(description=text,epilog=example_text,formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-d", "--tsv-directory", help="path to a directory where the tsv files exist", type=str , required=True)
parser.add_argument("-o", "--output-directory", help="path to a directory where you want to create the yaml files", type=str , required=True)
args = parser.parse_args()

print("[+] Processing all TSV files.. ")
schemafiles = glob.glob("{}/**/*.tsv".format(args.tsv_directory), recursive=True)

for sf in schemafiles:
    print("[  >>] Reading contents of {}.. ".format(sf))
    filename = os.path.splitext(os.path.basename(sf))[0]
    providerFolder = '{}/{}'.format(args.output_directory, filename)
    os.makedirs(providerFolder, exist_ok=True) 
    with open(sf) as tsvfile:
        reader = list(csv.DictReader(tsvfile, delimiter="\t"))
        for r in reader:
            if 'event(fields)' in r.keys():
                r['event_fields'] = []
                reFields = re.search('.*\((.*)\).*', r['event(fields)'], re.IGNORECASE).group(1)
                if reFields:
                    fieldsList = reFields.split(',')
                    for fl in fieldsList:
                        fieldDict = dict()
                        newField = (fl.strip()).split(" ")
                        fieldDict['field_type'] = newField[0]
                        fieldDict['field_name'] = newField[1]
                        r['event_fields'].append(fieldDict)
            if 'event_id' in r.keys():
                if r['version'] == '0':
                    yamlFile = r['event_id']
                else:
                    yamlFile = '{}_v{}'.format(r['event_id'],r['version'])
            else:
                yamlFile = filename
            with open('{}/{}.yaml'.format(providerFolder,yamlFile), 'w') as file:
                yaml.dump(dict(r), file, default_flow_style=False, sort_keys=False)