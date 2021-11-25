SHELL := /bin/bash

n = 4
s = "1001"
case = "balanced" # other option is balanced


default: run

run: 
	python bv.py bv $(s) $(n)
	python dj.py dj $(case) $(n)


clean:
	rm -rf *.json

