#! /bin/env python3
from pathlib import Path
import os
import sys
import subprocess

def start_file(path):
	parts = []
	if Path(path).owner() == 'root':
		parts.append('sudo')
	
	if subprocess.check_output(['file', '-i', path]).endswith(b'charset=binary\n'):
		parts.append('xdg-open')
		subprocess.Popen(parts + existing)
	else:
		parts.append(os.getenv('EDITOR'))
		subprocess.call(parts + existing)

args = list(sys.argv[1:])

inputs = []
existing = []
new = []

while args and not os.path.exists(args[0]):
	inputs.append(args.pop(0))

while args and os.path.exists(args[0]):
	existing.append(args.pop(0))

while args and not os.path.exists(args[0]):
	new.append(args.pop(0))

assert len(args) == 0, 'Unexpected existing paths at the end of command: ' + ' '.join(args)

if not inputs and not existing and not new:
	subprocess.call(['ls', '-lah'])
elif not inputs and not new and len(existing) == 1 and os.path.isdir(existing[0]):
	print("cd functionality not working at the moment.")
elif not inputs and not new and len(existing) == 1 and os.path.isfile(existing[0]):
	start_file(existing[0])
elif len(inputs) == 1 and not new and not existing and not Path(inputs[0]).suffix:
	subprocess.call(['mkdir', '-p'] + inputs)
elif len(inputs) == 1 and existing and not new:
	subprocess.call(['grep', '-r'] + inputs + existing)
elif not inputs and ((len(new) == 1 and not Path(new[0]).suffix) or (not new and len(existing) > 1 and os.path.isdir(existing[-1]))):
	if new:
		os.makedirs(new[0])
	subprocess.call(['mv'] + existing + new)
else:
	print("Unexpected commands. Don't know what to do.")
	print('inputs:', inputs)
	print('existing:', existing)
	print('new:', new)
