#! /bin/env python3
from pathlib import Path
import os
import sys
import subprocess

def call_on_file(command_parts, file, async=False):
	command_parts = list(command_parts) # Don't modify the original, just in case.
	function = subprocess.Popen if async else subprocess.call
	if Path(file).owner() == 'root':
		command_parts.insert(0, 'sudo')
	function(command_parts + [file])

def start_file(path):
	if subprocess.check_output(['file', '-i', path]).endswith(b'charset=binary\n'):
		call_on_file(['xdg-open'], path, async=True)
	else:
		call_on_file([os.getenv('EDITOR')], path)

def find_replace(pattern, replacement, paths):
	command = '%s/{}/{}/gc'.format(*inputs)
	for path in map(Path, paths):
		if path.is_dir():
			find_replace(pattern, replacement, map(str, path.iterdir()))
		else:
			call_on_file(['vim', '-c', command, '-c', 'wq'], path)

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
	call_on_file(['ls', '-lah', '--color', 'always'], existing[0])
elif not inputs and not new and len(existing) == 1 and existing[0].endswith(('.zip', '.tar.gz', '.tar.bz2', '.7z', '.rar')):
	file, = existing
	if file.endswith('.zip'):
		call_on_file(['zipinfo'], file)
		if input('Extract? [y/N]')[0].lower() == 'y':
			call_on_file(['unzip'], file)
	else:
		raise ValueError(file)
elif not inputs and not new and len(existing) == 1 and os.path.isfile(existing[0]):
	start_file(existing[0])
elif len(inputs) == 1 and not new and not existing and not Path(inputs[0]).suffix:
	try:
		os.makedirs(inputs[0])
	except PermissionError:
		subprocess.call(['sudo', 'mkdir', '-p', inputs[0]])
elif len(new) == 1 and existing and not inputs and new[0].endswith('.zip'):
	subprocess.call(['zip', '-r'] + new + existing)
elif len(inputs) == 1 and existing and not new:
	subprocess.call(['grep', '-r'] + inputs + existing)
elif len(inputs) == 2 and existing and not new:
	pattern, replacement = inputs
	find_replace(pattern, replacement, map(Path, existing))
elif not inputs and ((len(new) == 1 and not Path(new[0]).suffix) or (not new and len(existing) > 1 and os.path.isdir(existing[-1]))):
	if new:
		os.makedirs(new[0])
	subprocess.call(['mv'] + existing + new)
else:
	print("Unexpected commands. Don't know what to do.")
	print('inputs:', inputs)
	print('existing:', existing)
	print('new:', new)
