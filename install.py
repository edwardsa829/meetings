#!/bin/bash
import os
if os.system('python3.7 -m pip install -r requirements.txt') == 0:
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


os.system('mv dist/JW\ Meetings.app .')
os.system('rm -r build __pycache__ .eggs dist')
os.system('rm -r .git')
os.system('rm app.py Icon.icns Logo.png links.txt metadata.py .gitignore requirements.txt')
os.system('rm install.py')
print("\n\nINSTALL COMPLETE!\n\n")





