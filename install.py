#!/bin/bash
import os
if os.system('python3.7 -m pip3 install -r requirements.txt') == 0:
    print("Downloaded packages")
else:
    print("\nERROR: Make sure you are connected to the internet!\n")
from setuptools import setup
import requests
import metadata


response = requests.get("https://api.github.com/repos/edwardsa829/JWMeetings/releases").json()
VERSION = response[0]["tag_name"]
CF = {
        'CFBundleVersion': VERSION,
        'CFBundleShortVersionString': VERSION
}
metadata.OPTIONS["plist"].update(CF)

setup(
    app=metadata.APP,
    name=metadata.APP_NAME,
    version=VERSION,
    author=metadata.AUTHOR,
    description=metadata.DESCRIP,
    long_description=metadata.L_DESCRIP,
    url=metadata.URL,
    options={'py2app': metadata.OPTIONS},
    data_files=metadata.DATA_FILES,
    setup_requires=metadata.SETUP,
    install_requires=metadata.REQUIREMENTS
)

for x in range(10):
    os.system(f'/Applications/Python\ 3.{x}/Install\ Certificates.command')
    os.system(f'/Applications/Python\ 3.{x}/Update\ Shell\ Profile.command')

os.system('mv dist/JW\ Meetings.app ..')
os.system('cd .. ; rm JWMeetings-main.zip ; rm -r JWMeetings-main')

print("\n\nINSTALL COMPLETE!\n\n")





