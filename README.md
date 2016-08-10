# f

`f` is the worst possible Unix program. The Unix philosophy says:

> - Write programs that do one thing and do it well.
> - Write programs to work together.
> - Write programs to handle text streams, because that is a universal interface.

More informal principles involve accepting many command line arguments to fine tune execution, outputting as little as possible, not second guessing the user.

`f` performs file management while doing the exact opposite of each of those principles. It is chatty, doesn't read from stdin, second guesses the user, does too much, has no flags for configuration. It is also surprising useful, replacing (or wrapping) many standard tools.

    f [pattern [replacement]] [existing [...]] [new]

| `f` command | behaves like |
|-----|------|
| `f` | `ls` |
| `f directory` (with `inith.sh`) | `cd directory` |
| `f directory` (without `inith.sh`) | `ls directory` and `git status` if applicable |
| `f directory/new` | `mkdir -p directory/new` |
| `f file.txt` | `vim file.txt` |
| `f /etc/networks` | `sudo vim /etc/networks` |
| `f file1.txt file2.txt directory` | `mv file1.txt file2.txt directory` |
| `f file1.txt file2.txt directory/new` | `mkdir directory/new && mv file1.txt file2.txt directory/new` |
| `f file.tar.gz` | `tar -xvf file.tar.gz` |
| `f file.zip` | `unzip file.zip` |
| `f directory .zip` | `zip -r directory.zip directory` |
| `f image.png .jpg` | `convert image.png image.jpg` |
| `f text.txt .html` | `pandoc -o text.html text.txt` |
| `f "pattern" file1.txt file2.txt` | `grep "pattern" file1.txt file2.txt` |
| `f "pattern" directory` | `grep -r "pattern" directory` |
| `f "pattern" "replacement" directory` | interactive find & replace in `directory` |

To install `f` on your terminal just add the following line to your `~/.bashrc`:

  [ -f ~/f/init.sh ] && . ~/f/init.sh
