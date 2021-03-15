from setuptools import setup
import os


VERSION = "v1.0.1"
APP = ['app.py']
APP_NAME = "JW Meetings"
DATA_FILES = ['links.txt']
OPTIONS = {
    'argv_emulation': True,
    # 'iconfile': '.icns',
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleVersion': VERSION,
        'CFBundleShortVersionString': VERSION,
        'NSHumanReadableCopyright': u"Copyright © 2021, Alexander Edwards, All Rights Reserved"
    },
    'packages': ['certifi', 'urllib3', 'requests', 'rumps']
}

setup(
    app=APP,
    name=APP_NAME,
    version=VERSION,
    author='Alexander Edwards',
    description='Playlist generator for JW meetings',
    long_description='Playlist generator for JW meetings',
    url='https://github.com/edwardsa829/JWMeetings',
    options={'py2app': OPTIONS},
    data_files=DATA_FILES,
    setup_requires=['py2app'],
    install_requires=['certifi', 'urllib3', 'requests', 'rumps']
)


os.system('productbuild --component dist/JW\ Meetings.app /Applications/ JW_Meetings-{}.pkg'.format(VERSION))
os.system('rm -r build')
os.system('rm -r .eggs')
os.system('rm -r __pycache__')
os.system('rm -r dist')
os.system(f'zip JW_Meetings-{VERSION}.pkg.zip JW_Meetings-{VERSION}.pkg')
os.system(f'aws s3 cp JW_Meetings-{VERSION}.pkg.zip s3://jw-meetings/versions/ --profile default')
os.system('rm -r JW_Meetings-{}.pkg'.format(VERSION))

