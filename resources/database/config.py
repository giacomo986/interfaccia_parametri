#!/usr/bin/python
from configparser import ConfigParser

import os
cwd = os.getcwd()

def config(filename='/resources/database/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(f"{cwd}{filename}")

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
            print(f"{param[0]}:{param[1]}")
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db