PYTHON=python3
PYTHON=python2

all:
	$(PYTHON) lib.py

h:
	$(PYTHON) hypergeometrictest.py 1000 100 50 30
