SHELL := /bin/bash

width = 4
string = "1001"
case = "balanced" # other option is balanced


default: run

run: 
	python bv.py -s $(string) -w $(width)
	python dj.py -c $(case) -w $(width)
	python grover_2qbit.py
	python grover_3qbit.py

clean:
	rm -rf *.json

