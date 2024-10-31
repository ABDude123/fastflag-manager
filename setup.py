from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('data', ['data/fastflags.json', 'data/pro_fastflags.json']),
    ('resources', ['resources/app.png', 'resources/search.png', 'resources/favorite.png',
                  'resources/unfavorite.png', 'resources/exploit.png', 'resources/performance.png',
                  'resources/graphics.png', 'resources/network.png', 'resources/debug.png',
                  'resources/apply.png', 'resources/import.png', 'resources/export.png',
                  'resources/pro.png', 'resources/lock.png'])
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt6'],
    'iconfile': 'resources/app.png',
    'plist': {
        'CFBundleName': 'FastFlag Manager',
        'CFBundleDisplayName': 'FastFlag Manager',
        'CFBundleIdentifier': 'com.fastflagmanager',
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHighResolutionCapable': True,
    }
} 