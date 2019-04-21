#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import urllib.request

platform = "Linux"
architecture = "linux-x86_64"
distro = 'debian'
plex_download_api = "https://plex.tv/pms/downloads/5.json?channel=plexpass"

os.chdir(os.getcwd())

print("Looking up available downloads")

try:
    with urllib.request.urlopen(plex_download_api) as url:
        data = json.loads(url.read().decode())
except Exception as e:
    print(e)
    sys.exit()

item = data['computer'][platform]
release_date = item['release_date']
version = item['version']

for release in item['releases']:
    if release['build'] == architecture and release['distro'] == distro:
        label = release['label']
        download_url = release['url']
        file_name = download_url.rsplit('/', 1)[1]

if download_url and not os.path.isfile(file_name):
    print('Downloading ' + label + '\n' + file_name)
    urllib.request.urlretrieve(download_url, file_name)

install = input('Install Plex Media Server ' + version + '? Type [Y] to continue: ')

if install == 'y':
    subprocess.run(['sudo', 'dpkg', '-i', file_name])
    os.remove(file_name)
else:
    print('Installation aborted')
