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

print("Looking up available downloads")

try:
    with urllib.request.urlopen(plexDownloadApi) as url:
        data = json.loads(url.read())
except:
    print('ERROR: There was an error looking up available downloads. Please try again later')
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
    subprocess.run(['ls', '-l', file_name])
    os.remove(file_name)
else:
    print('Installation aborted')
    #  subprocess.run(['dpkg', '-i', file_name])
    #  subprocess.run(['rm', file_name])
    # use shutil.unlink instead!
    # Also this deletion should happen in a 'finally' block so it always gets deleted
