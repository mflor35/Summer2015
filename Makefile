.PHONY: venv clobber
venv:
	virtualenv -p python2.7 venv
	venv/bin/pip install -r requirements.txt

clobber:
	rm -rf venv/
