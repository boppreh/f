# f

`f` is the worst possible Unix program. The Unix philosophy says:

> - Write programs that do one thing and do it well.
> - Write programs to work together.
> - Write programs to handle text streams, because that is a universal interface.

More informal principles involve accepting many command line arguments to fine tune execution, outputting as little as possible, not second guessing the user.

`f` performs file management while doing the exact opposite of each of those principles. It replaces many of the standard tools:

- `ls` -> `f`
- `cd directory` -> `f directory` (still working on this one)
- `vim file.txt` -> `f file.txt`
- `sudo nano /etc/networks` -> `f /etc/networks`
- `mkdir -p directory/dir` -> `f directory/dir`
- `mv file1.txt file2.txt directory` -> `f file1.txt file2.txt directory`
- `tar -xvf file.tar.gz` -> `f file.tar.gz`
- `zip -r directory.zip directory` -> `f directory`
- `unzip directory.zip` -> `f directory.zip
- `grep "pattern" file1.txt file2.txt` -> `f "pattern" file1.txt file2.txt`
- `grep -r "pattern" directory` -> `f "pattern" directory`