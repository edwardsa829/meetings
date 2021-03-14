from setuptools import setup


APP = ['app.py']
DATA_FILES = ['links.txt']
OPTIONS = {
    'argv_emulation': True,
    # 'iconfile': '.icns',
    # 'plist': {
    #     'LSUIElement': True
    # },
    'packages': ['certifi', 'urllib3', 'requests', 'rumps']
}

setup(
    app=APP,
    name='JW Meetings',
    options={'py2app': OPTIONS},
    data_files=DATA_FILES,
    setup_requires=['py2app'], 
    install_requires=['certifi', 'urllib3', 'requests', 'rumps']
)