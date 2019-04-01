#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os

import urllib
import requests

"""
This script mainly fetches a access token from the API and
secondly update the msrun metadata via API endpoint
"""

base_url = "https://www.ebi.ac.uk/pride/ws/archive/v2/"

def getToken(username, password):
    token = ""

    # get token to access the api
    url = base_url + "getAAPToken?username=" + username + "&password=" + password
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    response = requests.post(url, headers=headers)

    if (not response.ok) or response.status_code != 200:
        response.raise_for_status()
        sys.exit()
    else:
        token = response.text
    return token


def validateToken(token):
    # get token to access the api
    url = base_url + "token-validation"
    headers = {'Authorization': 'Bearer ' + token}

    response = requests.post(url, headers=headers)

    return response.ok and response.status_code == 200 and response.text == 'Token Valid'


def updateMsrunMetadata(filename, token):
    # get project file accession from the prefix of the file name
    accession = filename.split('-', 1)[0]

    url = base_url + "msruns/" + accession + "/updateMetadata"
    headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer ' + token}

    with open(filename) as json_file:
        data = json.load(json_file)
        print(json.dumps(data))
        response = requests.put(url, data=json.dumps(data), headers=headers)

        if (not response.ok) or response.status_code != 200:
            response.raise_for_status()
            sys.exit()
        else:
            print(response)


def wrapWithMSRunMetadata(filename):
    line_prepender(filename, '{"MSRunMetadata":')
    line_postpender(filename, "}")


def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + content)


def line_postpender(filename, line):
    with open(filename, "a") as myfile:
        myfile.write(line)

def main():
    # get metadata file name
    filename = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    token = getToken(username, password)
    print(token)
    isvalid = validateToken(token)
    print(isvalid)
    wrapWithMSRunMetadata(filename)
    updateMsrunMetadata(filename, token)

if __name__ == '__main__':
    main()
