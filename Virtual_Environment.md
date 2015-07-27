## Python Virtual Environment

All libraries and versions used can be put under revision control among
other benefits.

__To initialize:__
1. - install _python-virtualenv_ (fedora package name, ymmv)

2. run
```make venv"```
the virtual environment will be installed in the the
same directory as the makefile under the directory name 'venv' and pip
will install all packages listed under _requirements.txt_

To remove the venv directory:
A. run "make clobber"
or
B. run "rm -rf venv"
A is preferred, for prevention of fatfingering the wrong files while
typing the 'rm' command

To install new libraries:
1. search for it using "venv/bin/pip"
2. install it using "venv/bin/pip"
3. update requirements.txt by running
"venv/bin/pip freeze>requirements.txt"
4. make a commit updating requirements.txt in git (please don't add more
than needed)

To run any of the scripts using the virtual environment, put
"#!venv/bin/python" as a shebang line in the file, mark the file
executable, and run it from the project's root directory. You can also
run a script manually with venv/bin/python or venv/bin/ipython

You may also enter into the virtual environment by running
venv/bin/activate. Which will put venv/bin at the begining of your $PATH
so that when you run just "python," the python executable in venv/bin is
used. To leave the virtual environment one would subsequently run
"deactivate" to restore $PATH and other settings to normal.

NOTE: pip in our virtualenv will compile matplotlib and numpy from scratch, care should be taken when you clobber a virtualenv on a system
due to the resources required for compiling.
