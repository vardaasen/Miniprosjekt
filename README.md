## working with different python versions
change the content of the .pythonversion
to the version python you want to test
```bash
cpython-3.14.0b4+freethreaded-macos-aarch64-none
```
```bash
cpython-3.14.0rc3+freethreaded-windows-x86_64-none
```

## Using uv for python project managment and running/testing python program

### uv manages the installed python versions and vertual environments
- list *some available python versions and determine if any are installed
```bash
uv python list
```
- install a python version listed in the available python list
```bash
uv python install <name of python version>
```
- run a program with the python specified in .pythonversion
```bash
uv run main.py
```

