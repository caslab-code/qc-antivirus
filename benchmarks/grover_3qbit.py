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

def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc

def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
    qc.h(nqubits-1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "U$_s$"
    return U_s
    
def grovers_algorithm_3():
    n = 3 #number of qbits
    qc = QuantumCircuit(n)
    qc.cz(0, 2)
    qc.cz(1, 2)
    oracle_ex3 = qc.to_gate()
    oracle_ex3.name = "U$_\omega$"
    grover_circuit = QuantumCircuit(n)
    grover_circuit = initialize_s(grover_circuit, [0,1,2])
    grover_circuit.append(oracle_ex3, [0,1,2])
    grover_circuit.append(diffuser(n), [0,1,2])
    grover_circuit.measure_all()
    return grover_circuit
    
def grover_3qbit():
    n = 3
    grover_circuit = grovers_algorithm_3()
    aer_sim = Aer.get_backend('aer_simulator')
    tranpiled_grover_circuit = transpile(grover_circuit, aer_sim)
    total_pattern = 0
    print("Search Pattern:") 
    print(pt)
    total_pattern = 0
    for i in range(0,n-1):
        for j in range(i+1, n):
            pattern = search_pattern.search_pattern_defined_bits(tranpiled_grover_circuit, pt, [j,i])
            print("No. of patterns detected between Qbit",i,"and Qbit",j, "are", pattern)
            total_pattern = total_pattern + pattern
    
    print("Total Pattern", total_pattern)
    # pattern1 = search_pattern.search_pattern_defined_bits(tranpiled_grover_circuit, pt, [1,0])
    # pattern2 = search_pattern.search_pattern_defined_bits(tranpiled_grover_circuit, pt, [2,1])
    # pattern3 = search_pattern.search_pattern_defined_bits(tranpiled_grover_circuit, pt, [2,0])
    # print("No. of patterns detected between Qbit 0 and Qbit 1 are", pattern1)
    # print("No. of patterns detected between Qbit 1 and Qbit 2 are", pattern2)
    # print("No. of patterns detected between Qbit 2 and Qbit 0 are", pattern3)
    
    # if (pattern1 + pattern2 + pattern3 > 0):
        # print("Malicious Code")
    # else:
        # print("Safe Code")
   
    return 

    
grover_3qbit()    
