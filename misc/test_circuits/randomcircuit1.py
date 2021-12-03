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
sys.path.append('./../../antivirus')
import search_pattern

import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

#pattern
pt = QuantumCircuit(2)
pt.cx(1, 0)
pt.cx(1, 0)
pt.cx(1, 0)
pt.cx(1, 0)

pt2 = QuantumCircuit(2)
pt2.cx(0,1)
pt2.cx(0,1)
pt2.cx(0,1)
pt2.cx(0,1)

#bitmap [1,0] = we are searching for series of CNOT gates connect between Qbit-0 and Qbit-1
bit_map = [1, 0]

    
def malicious_circuit():
    n = 3
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
    # aer_sim = Aer.get_backend('aer_simulator')
    # transpiled_malicious = transpile(malicious, aer_sim)
    # transpiled_pt = transpile(pt, aer_sim)
    
    print("Input Circuit:") 
    print(malicious)
    
    print("Search Pattern:") 
    print(pt2)
    pattern = search_pattern.search_pattern_defined_bits(malicious, pt, bit_map)
    
    print("No. of patterns detected between Qbit 0 and Qbit 1 are", pattern)
    if (pattern > 0):
        print("Malicious Code Detected")
    else:
        print("Safe Code")
    
    return 

    

randomcircuit()    
