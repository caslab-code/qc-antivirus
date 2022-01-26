SHELL := /bin/bash

width = 2
string = "01"
case = "balanced" # other option is constant
copies = 1


default: run

run: 
	python bv.py -s $(string) -w $(width)
	python dj.py -c $(case) -w $(width) -m $(mal_type) -k $(copies)
	python grover_2qbit.py
	python grover_3qbit.py

clean:
	rm -rf *.json

