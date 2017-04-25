#!/usr/bin/env python3

"""
Ubuntu 64-bit Plex Media Server Updater.

Downloads the latest Plex media server .deb file and installs it.
"""

import json
import os
import subprocess
import sys
import urllib.request

platform = "Linux"
architecture = "linux-ubuntu-x86_64"
distro = 'ubuntu'
plexDownloadApi = "https://plex.tv/api/downloads/1.json?channel=plexpass"

os.chdir(os.getcwd())

print("Looking up available downloads")

try:
    with urllib.request.urlopen(plexDownloadApi) as url:
        data = json.loads(url.read().decode())
except Exception as e:
    print(e)
    sys.exit()

item = data['computer'][platform]
releaseData = item['release_date']
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
    subprocess.run(['dpkg', '-i', file_name])
    os.remove(file_name)
else:
    print('Installation aborted')
