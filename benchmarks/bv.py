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
sys.path.append('../antivirus/previous_antivirus')
import search_pattern

sys.path.append('../antivirus')
from isomorphism import pattern_counter, match 


def malicious_circuit_gen(copies, mal_type): # copies- decides the depth of the malicious circuit and mal_type decides which malicious circuit
    
    if (mal_type == 'M10'):
        n = 4
    
    elif (mal_type == 'M9'):
        n = 3
    
    elif (mal_type == 'M5' or mal_type == 'M6' or mal_type == 'M7' or mal_type == 'M8'  ):
        n = 1     
    
    else:
        n = 2
    mal_circuit = QuantumCircuit(n)
    
############ MALICIOUS CIRCUIT #####################
    for i in range(copies):
        if (mal_type == 'M1'):
            mal_circuit.cx(0,1)
        
        if (mal_type == 'M2'):
            mal_circuit.cx(0,1)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M3'):
            mal_circuit.cx(0,1)
            mal_circuit.cx(1,0)
        
        if (mal_type == 'M4'):
            mal_circuit.cx(0,1)
            mal_circuit.h(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
            mal_circuit.h(0)
        
        if (mal_type == 'M5'):
            mal_circuit.x(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M6'):
            mal_circuit.y(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M7'):
            mal_circuit.z(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M8'):
            mal_circuit.h(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M9'):
            mal_circuit.cx(0,1)
            mal_circuit.cx(1,2)
        
        if (mal_type == 'M10'):
            if i%2==1:
                mal_circuit.cx(1,0)
                mal_circuit.cx(2,1)
                mal_circuit.cx(3,2)
                mal_circuit.delay(0, qarg = 3)
            else:
                mal_circuit.cx(3,2)
                mal_circuit.cx(2,1)
                mal_circuit.cx(1,0)
                mal_circuit.delay(0, qarg = 0)
####################################################

#     mal_circuit.barrier()
#     mal_circuit.measure_all()
    
    return mal_circuit

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
 
    
# def bv_old(s, n):
    # n = int(n)
    # bv_circuit = bv_algorithm(s, n)
    # aer_sim = Aer.get_backend('aer_simulator')
    # tranpiled_bv = transpile(bv_circuit, aer_sim)
    
    ##FIXME antivirus should go here I think 
    ##f = open("transpiled_bv.json", "w")
    ##f.write(str(assemble(tranpiled_bv)))
    ##f.close()
    
    # total_pattern = 0
    # print("Search Pattern:") 
    # print(pt)
    # for i in range(0,n-1):
        # for j in range(i+1, n):
            # pattern = search_pattern.search_pattern_defined_bits(tranpiled_bv, pt, [i,j])
            # print("No. of patterns detected between Qbit",i,"and Qbit",j, "are", pattern)
            # total_pattern = total_pattern + pattern
    
    # print("Total Number of Patterns detected", total_pattern)
    
    # return 

def bv(s, n, mal_type, copies):
    #for our application s = "01", n = 2
    n = int(n)
    qc = bv_algorithm(s, n)
    pt = malicious_circuit_gen(copies, mal_type)
    print("--------------------------------------------------------")
    print("Bernstein-Vazarani Circuit", "\n Search String = ", s, "\n Number of Qubits =", n) 
    print(qc)
    
    print("Search Pattern:") 
    print(pt)
    
    for matching in match(qc, pt):
        print(matching)

    # 2. Pattern counter:
    #       Count how many patterns in the quantum circuit.
    print("--------------------------------------------------------")
    print("2. Pattern counter\n")
    print("The pattern count in the quantum circuit is: " + str(pattern_counter(qc, pt)))    
   
    
    return 

    
parser = argparse.ArgumentParser()
parser.add_argument('-s','--string', type=str, required=True, help='Hidden binary String')
parser.add_argument('-w','--width', type=int, required=True, help='Width of binary string')
parser.add_argument('-m','--mal_type', type=str, required=True, help='Malicious Circuit type options M1 - M10')
parser.add_argument('-k','--copies', type=int, required=True, help='Defines depth of the malicious circuit')

args = parser.parse_args()
bv(args.string, args.width, args.mal_type, args.copies)    
