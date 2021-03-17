APP = ['app.py']
APP_NAME = "JW Meetings"
DATA_FILES = ['links.txt']
OPTIONS = {
    'argv_emulation': True,
    # 'iconfile': '.icns',
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'NSHumanReadableCopyright': u"Copyright © 2021, Alexander Edwards, All Rights Reserved"
    },
    'packages': ['certifi', 'urllib3', 'requests', 'rumps']
}
AUTHOR = "Alexander Edwards"
DESCRIP = "Playlist generator for JW meetings"
L_DESCRIP = "Playlist generator for JW meetings"
URL = "https://github.com/edwardsa829/JWMeetings"
SETUP = ['py2app']
REQUIREMENTS = ['certifi', 'urllib3', 'requests', 'rumps']