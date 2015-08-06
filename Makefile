.PHONY: clobber install
venv:
	virtualenv -p python2.7 venv

install: venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	mkdir -p tmp
	git clone https://github.com/thom-nic/python-xbee.git tmp/python-xbee
	cd tmp/python-xbee; ../../venv/bin/python setup.py install
	#this isn't optimal but later we'll test for existance of tmp/python-xbee before cloning with git (which will fail if python-xbee directory exists)
	rm -rf tmp

clobber:
	rm -rf venv/
