import os
from distutils.core import setup
import py2exe

Mydata_files = []
for files in os.listdir('D:/Lycee/1G7/NSI/GITHUB/Jeu-Python/jeu/media/'):
    f1 = 'D:/Lycee/1G7/NSI/GITHUB/Jeu-Python/jeu/media/' + files
    if os.path.isfile(f1): # skip directories
        f2 = 'images', [f1]
        Mydata_files.append(f2)

setup(
    console=['START.py'],
    data_files = Mydata_files,
    options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
                        "excludes": ["email"]
                }
        }
)