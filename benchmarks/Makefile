SHELL := /bin/bash

width = 2
string = "01"
case = "balanced" # other option is constant
copies = 1
mal_type = "M1"
qnn_type = "short" #possible options "medium" and "long"

default: run

run: 
	python bv.py -s $(string) -w $(width) -m $(mal_type) -k $(copies)
	python dj.py -c $(case) -w $(width) -m $(mal_type) -k $(copies)
	python ga.py -m $(mal_type) -k $(copies)
	python qnn.py -q $(qnn_type) -m $(mal_type) -k $(copies)

clean:
	rm -rf *.json

