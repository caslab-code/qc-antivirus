# initialization
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, assemble

# import basic plot tools
from qiskit.visualization import plot_histogram

#importing from Search Pattern
import sys
sys.path.append('../antivirus')
import search_pattern

#sample pattern
pt = QuantumCircuit(2)
pt.cx(1, 0)
pt.cx(1, 0)

def bv_algorithm(s, n):
    # We need a circuit with n qubits, plus one auxiliary qubit
    # Also need n classical bits to write the output to
    bv_circuit = QuantumCircuit(n+1, n)

    # put auxiliary in state |->
    bv_circuit.h(n)
    bv_circuit.z(n)

    # Apply Hadamard gates before querying the oracle
    for i in range(n):
        bv_circuit.h(i)

    # Apply barrier 
    bv_circuit.barrier()

    # Apply the inner-product oracle
    s = s[::-1] # reverse s to fit qiskit's qubit ordering
    for q in range(n):
        if s[q] == '0':
            bv_circuit.i(q)
        else:
            bv_circuit.cx(q, n)

    # Apply barrier 
    bv_circuit.barrier()

    #Apply Hadamard gates after querying the oracle
    for i in range(n):
        bv_circuit.h(i)
    
    # Measurement
    for i in range(n):
        bv_circuit.measure(i, i)
    
    return bv_circuit
 
    
def bv(s, n):
    n = int(n)
    bv_circuit = bv_algorithm(s, n)
    aer_sim = Aer.get_backend('aer_simulator')
    tranpiled_bv = transpile(bv_circuit, aer_sim)
    
    # FIXME antivirus should go here I think 
    # f = open("transpiled_bv.json", "w")
    # f.write(str(assemble(tranpiled_bv)))
    # f.close()
    
    total_pattern = 0
    print("Search Pattern:") 
    print(pt)
    for i in range(0,n-1):
        for j in range(i+1, n):
            pattern = search_pattern.search_pattern_defined_bits(tranpiled_bv, pt, [i,j])
            print("No. of patterns detected between Qbit",i,"and Qbit",j, "are", pattern)
            total_pattern = total_pattern + pattern
    
    print("Total Number of Patterns detected", total_pattern)
    
    return 

    
parser = argparse.ArgumentParser()
parser.add_argument('-s','--string', type=str, required=True, help='Hidden binary String')
parser.add_argument('-w','--width', type=int, required=True, help='Width of binary string')
args = parser.parse_args()
bv(args.string, args.width)    
