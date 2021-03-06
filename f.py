#! /bin/env python3
from pathlib import Path
import os
import sys
import subprocess
import re

def call_on_file(command_parts, file, async=False):
    command_parts = list(command_parts) # Don't modify the original, just in case.
    function = subprocess.Popen if async else subprocess.call
    if Path(file).owner() == 'root':
        command_parts.insert(0, 'sudo')
    function(command_parts + [str(file)])

def start_file(path):
    if subprocess.check_output(['file', '-i', path]).endswith(b'charset=binary\n'):
        call_on_file(['xdg-open'], path, async=True)
    else:
        call_on_file([os.getenv('EDITOR')], path)

def find_replace(pattern, replacement, paths):
    for path in map(Path, paths):
        if path.is_dir():
            yield from find_replace(pattern, replacement, map(str, path.iterdir()))
        else:
            with path.open() as f:
                try:
                    contents = f.read()
                except UnicodeDecodeError:
                    continue

            # Yep, I know this is very inefficient. This function is not
            # supposed to be used on larger files, and we are generally
            # willing to pay for better user experience.
            matches = len(re.findall(pattern, contents))
            with path.open('w') as f:
                f.write(re.sub(pattern, replacement, contents))
            yield path, matches

            # Alternative: use vim to find replace.
            # Downside: every single file requires input from the user,
            # the interface is very confusing, errors are shown in a scary way,
            # and it's hard to cancel.
            #command = '%s/{}/{}/gc'.format(pattern, replacement)
            #call_on_file(['vim', '-c', command, '-c', 'wq'], path)

def convert(file, new_file):
    if os.path.isdir(new_file):
        subprocess.call(['mv', file, new_file])

    if '.' + new_file in image_extensions + doc_extensions:
        new_file = '.' + new_file

    if new_file in image_extensions + doc_extensions:
        new_file = str(Path(file).with_suffix(new_file))

    file_ext = Path(file).suffix
    new_file_ext = Path(new_file).suffix
    if file_ext in image_extensions and new_file_ext in image_extensions:
        try:
            subprocess.call(['convert', file, new_file])
        except FileNotFoundError:
            print('Conversion failed. You need ImageMagick installed for this (`convert` binary).')
    elif file_ext in doc_extensions and new_file_ext in doc_extensions:
        try:
            subprocess.call(['pandoc', '-o', new_file, file])
        except FileNotFoundError:
            print('Conversion failed. You need pandoc installed for this.')
    else:
        os.makedirs(new_file)
        subprocess.call(['mv', file, new_file])

DEFAULT_LS = ['ls', '-oAhFv', '--color=auto']

image_extensions = ['.jpg', '.jpeg', '.gif', '.png']
doc_extensions = ['.txt', '.md', '.rst', '.html', '.pdf', '.docx', '.odt']

def invoke(args):
    inputs = []
    existing = []
    new = []

    while args and not os.path.exists(args[0]):
        inputs.append(args.pop(0))

    while args and os.path.exists(args[0]):
        existing.append(os.path.abspath(args.pop(0)))

    while args and not os.path.exists(args[0]):
        new.append(args.pop(0))

    assert len(args) == 0, 'Unexpected existing paths at the end of command: ' + ' '.join(args)

    if not inputs and not existing and not new:
        subprocess.call(DEFAULT_LS)
        if os.path.isdir('.git'):
            subprocess.call(['git', 'status'])
    elif not inputs and not new and len(existing) == 1 and os.path.isdir(existing[0]):
        call_on_file(DEFAULT_LS, existing[0])
    elif not inputs and not new and len(existing) == 1 and existing[0].endswith(('.zip', '.tar.gz', '.tar.bz2', '.7z', '.rar')):
        file, = existing
        if file.endswith('.zip'):
            call_on_file(['zipinfo'], file)
            # TODO: create a folder when extracting individual files.
            if input('\n=====\nExtract? [y/N]').lower().startswith('y'):
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
    elif len(new) == 1 and existing and not inputs and (new[0].endswith('.zip') or new[0] == 'zip'):
        new_file, = new
        if new_file == 'zip':
            new_file = '.' + new_file
        if new_file == '.zip':
            base_name = existing[0] if len(existing) == 1 else os.path.basename(os.path.commonpath(existing))
            new_file = str(Path(base_name).with_suffix(new_file))
        subprocess.call(['zip', '-r'] + [new_file] + existing)
    elif len(inputs) == 1 and existing and not new:
        grep = subprocess.Popen(['grep', '-I', '--color=auto', '--exclude-dir=.git', '-r'] + inputs + existing, stdout=subprocess.PIPE)
        tee = subprocess.Popen(['tee', '/dev/tty'], stdin=grep.stdout, stdout=subprocess.PIPE)
        linecount = int(subprocess.check_output(['wc', '-l'], stdin=tee.stdout))
        grep.wait()
        tee.wait()
        print('{:,} matches'.format(linecount))
    elif len(inputs) == 2 and existing and not new:
        pattern, replacement = inputs
        for path, matches in find_replace(pattern, replacement, map(Path, existing)):
            print('{} - {} matches'.format(path, matches))
    elif not inputs and not new and existing and os.path.isdir(existing[-1]):
        for file in existing[:-1]:
            subprocess.call(['mv', file, existing[-1]])
    elif not inputs and len(new) == 1 and existing:
        for file in existing:
            convert(file, new[0])
    else:
        print("Unexpected commands. Don't know what to do.")
        print('inputs:', inputs)
        print('existing:', existing)
        print('new:', new)


if __name__ == '__main__':
    invoke(list(sys.argv[1:]))
