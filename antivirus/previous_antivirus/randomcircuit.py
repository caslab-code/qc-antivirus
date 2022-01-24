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
# sys.path.append('C:/Users/sd982/OneDrive - Yale University/Desktop/qc-antivirus/antivirus')
sys.path.append('./../../antivirus')
import search_pattern

#pattern
pt = QuantumCircuit(2)
pt.cx(1, 0)
pt.cx(1, 0)
pt.cx(1, 0)
pt.cx(1, 0)


#bitmap [1,0] = we are searching for series of CNOT gates connect between Qbit-0 and Qbit-1
bit_map = [1, 0]

    
def malicious_circuit():
    n = 2
    mc = QuantumCircuit(n)
    mc.cx(0,1)
    mc.h(0)
    mc.cx(0,1)
    mc.h(0)
    mc.cx(0,1)
    mc.cx(0,1)
    mc.cx(0,1)
    mc.h(0)
    mc.cx(0,1)
    mc.cx(0,1)
    mc.cx(0,1)
    mc.h(1)
    mc.cx(0,1)
    mc.cx(0,1)
    mc.cx(0,1)
    mc.cx(0,1)

    return mc
    
def randomcircuit():
    malicious = malicious_circuit()
    aer_sim = Aer.get_backend('aer_simulator')
    tranpiled_malicious = transpile(malicious, aer_sim)
    
    print("Input Circuit:") 
    print(tranpiled_malicious)
    
    print("Search Pattern:") 
    print(pt)
    pattern = search_pattern.search_pattern_defined_bits(malicious, pt, bit_map)
    print("No. of patterns detected between Qbit 0 and Qbit 1 are", pattern)
    if (pattern > 0):
        print("Malicious Code Detected")
    else:
        print("Safe Code")
    
    hist = search_pattern.pattern_histogram(malicious, 'cx', [0, 1])
    print(hist)

    return hist

    

randomcircuit()    
