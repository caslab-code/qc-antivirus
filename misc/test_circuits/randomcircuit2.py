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

    
def malicious_circuit():
    n = 4
    mc = QuantumCircuit(n)
    mc.cx(2,3)
    mc.cx(2,3)
    mc.cx(2,3)
    mc.cx(2,3)
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
    mc.cx(1,2)
    mc.cx(1,2)
    mc.cx(1,2)
    mc.cx(1,2)

    return mc
    
def randomcircuit2():
    n = 4
    malicious = malicious_circuit()
    # aer_sim = Aer.get_backend('aer_simulator')
    # transpiled_malicious = transpile(malicious, aer_sim)
    # transpiled_pt = transpile(pt, aer_sim)
    
    print("Input Circuit:") 
    print(malicious)
    
    total_pattern = 0
    print("Search Pattern:") 
    print(pt2)
    for i in range(0,n-1):
        for j in range(i+1, n):
            # print(i,j)
            pattern = search_pattern.search_pattern_defined_bits(malicious, pt, [j,i])
            print("No. of patterns detected between Qbit",i,"and Qbit",j, "are", pattern)
            total_pattern = total_pattern + pattern
    
    print("Total Patterns detected = ", total_pattern)
    if (pattern > 0):
        print("Malicious Circuit Detected")
    else:
        print("Safe Circuit")
   
    return 

    

randomcircuit2()    
