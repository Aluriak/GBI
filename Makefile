PYTHON=python3
PYTHON=python2

all:
	$(PYTHON) lib.py

h:
	$(PYTHON) hypergeometrictest.py 1000 100 50 30


zip:
	mkdir -p TP1/
	cp ./workingfile.py ./libtp.py ./essentials.txt ./data/graph/biological*.gml ./examples.py TP1/
	zip -r TP1.zip TP1

