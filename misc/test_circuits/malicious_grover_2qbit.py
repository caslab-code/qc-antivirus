#initialization
import matplotlib.pyplot as plt
import numpy as np


# importing Qiskit
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy

# import basic plot tools
from qiskit.visualization import plot_histogram

#importing from Search Pattern
import sys
sys.path.append('../../antivirus')
import search_pattern

#pattern
pt = QuantumCircuit(2)
pt.cx(0,1)
pt.delay(10, unit = 'dt')

#bitmap [1,0] = we are searching for series of CNOT gates connect between Qbit-0 and Qbit-1
# bit_map = [1, 0]

def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc
 
    
def grovers_algorithm(k,d):
    n = 4
    grover_circuit = QuantumCircuit(n)
    grover_circuit = initialize_s(grover_circuit, [0,1])
   
    grover_circuit.cz(0,1) # Oracle

    # Diffusion operator (U_s)
    grover_circuit.h([0,1])
    grover_circuit.z([0,1])
    grover_circuit.cz(0,1)
    grover_circuit.h([0,1])
    
    
    for i in range(k):
    
        grover_circuit.cx(2,3)
        grover_circuit.delay(d, unit = 'dt')
    
    return grover_circuit
    
def grover_2qbit():
    n = 4
    grover_circuit = grovers_algorithm(1,10)   
    print("Search Pattern:") 
    print(pt)
    print("Victim Circuit + Malicious Circuit:") 
    print(grover_circuit)

    total_pattern = 0    
    for i in range(0,n-1):
        for j in range(i+1, n):
            pattern = search_pattern.search_pattern_defined_bits(grover_circuit, pt, [j,i])
            print("No. of patterns detected between Qbit",i,"and Qbit",j, "are", pattern)
            total_pattern = total_pattern + pattern  
    print("Total Patterns", total_pattern)
   
    return 

    

grover_2qbit()    
