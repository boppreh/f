#! /bin/env python3
import pathlib
import sys
import subprocess

def open(path):
    if path.owner() == 'root':
        subprocess.call(['sudo', 'xdg-open', str(path)])
    else:
        subprocess.Popen(['xdg-open', str(path)])


args = [pathlib.Path(a).absolute() for a in sys.argv[1:]]

if not args:
    print('Welcome to f.')
    exit()

if all(arg.is_file() for arg in args):
    for arg in args:
        open(arg)
