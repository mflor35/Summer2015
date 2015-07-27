# Python Virtual Environment

All libraries and versions used can be put under revision control among
other benefits.

## To initialize
1. Install __python-virtualenv__ (fedora package name, ymmv)

2. run
```make venv```
The virtual environment will be installed in the the
same directory as the makefile under the directory name __*venv*__ and pip
will install all packages listed under __requirements.txt__

To remove the venv directory:

__(A)__ run ``` make clobber ```

_or_

__(B)__  run ``` rm -rf venv ```

_(A)_ is preferred, for prevention of fatfingering the wrong files while
typing the ``` rm ``` command.


## To install new libraries:

1. Search for it using ``` venv/bin/pip ```

2. Install it using ``` venv/bin/pip ```

3. Update __requirements.txt__ by running
``` venv/bin/pip freeze>requirements.txt ```

4. Make a commit updating __requirements.txt__ in git (please don't add more
than needed)

To run any of the scripts using the virtual environment, put
``` #!venv/bin/python ``` as a shebang line in the file, mark the file
executable, and run it from the project's root directory. You can also
run a script manually with ``` venv/bin/python ``` _or_ ``` venv/bin/ipython ```.

You may also enter into the virtual environment by running
``` venv/bin/activate ```. Which will put ``` venv/bin ``` at the beginning of your ``` $PATH ```
so that when you run just ``` python ``` the python executable in ``` venv/bin ``` is
used. To leave the virtual environment one would subsequently run
``` deactivate ``` to restore ``` $PATH ``` and other settings to normal.

__NOTE:__  pip in our virtualenv will compile matplotlib and numpy from scratch, care should be taken when you clobber a virtualenv on a system
due to the resources required for compiling.
