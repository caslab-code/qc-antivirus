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
sys.path.append('./qc-antivirus/antivirus')
import search_pattern

#pattern
pt = QuantumCircuit(2)
pt.cx(1, 0)
pt.cx(1, 0)

#bitmap [1,0] = we are searching for series of CNOT gates connect between Qbit-0 and Qbit-1
bit_map = [1, 0]

def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc
 
    
def grovers_algorithm():
    n = 2
    grover_circuit = QuantumCircuit(n)
    grover_circuit = initialize_s(grover_circuit, [0,1])
   
    grover_circuit.cz(0,1) # Oracle

    # Diffusion operator (U_s)
    grover_circuit.h([0,1])
    grover_circuit.z([0,1])
    grover_circuit.cz(0,1)
    grover_circuit.h([0,1])
    return grover_circuit
    
def grover_2qbit():
    grover_circuit = grovers_algorithm()
    aer_sim = Aer.get_backend('aer_simulator')
    tranpiled_grover_circuit = transpile(grover_circuit, aer_sim)
    # FIXME antivirus should go here I think 
    # f = open("transpiled_grover_2qbit.json", "w")
    # f.write(str(assemble(tranpiled_grover_circuit)))
    # f.close()
    print("Search Pattern:") 
    print(pt)
    pattern = search_pattern.search_pattern_defined_bits(tranpiled_grover_circuit, pt, bit_map)
    print("No. of patterns detected between Qbit 0 and Qbit 1 are", pattern)
    # if (pattern > 0):
        # print("Malicious Code")
    # else:
        # print("Safe Code")
   
    return 

    

grover_2qbit()    
