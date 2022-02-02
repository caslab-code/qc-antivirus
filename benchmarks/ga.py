#initialization
import matplotlib.pyplot as plt
import numpy as np
import argparse

# importing Qiskit
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy

# import basic plot tools
from qiskit.visualization import plot_histogram

#importing from Search Pattern
import sys
sys.path.append('../antivirus/previous_antivirus')
import search_pattern

sys.path.append('../antivirus')
from pattern_matching import pattern_counter, match 


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
    
# def grover_2qbit():
    # grover_circuit = grovers_algorithm()
    # aer_sim = Aer.get_backend('aer_simulator')
    # tranpiled_grover_circuit = transpile(grover_circuit, aer_sim)
    ##FIXME antivirus should go here I think 
    ##f = open("transpiled_grover_2qbit.json", "w")
    ##f.write(str(assemble(tranpiled_grover_circuit)))
    ##f.close()
    # print("Search Pattern:") 
    # print(pt)
    # pattern = search_pattern.search_pattern_defined_bits(tranpiled_grover_circuit, pt, bit_map)
    # print("No. of patterns detected between Qbit 0 and Qbit 1 are", pattern)
    ##if (pattern > 0):
    ##    print("Malicious Code")
    ##else:
    ##    print("Safe Code")
    # return 

def ga(mal_type ="M1", copies =1):
    qc = grovers_algorithm()
    pt = malicious_circuit_gen(copies, mal_type)
    
    print("--------------------------------------------------------")
    print("Grover's 2-Qubit Circuit \n") 
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
parser.add_argument('-m','--mal_type', type=str, required=True, help='Malicious Circuit type options M1 - M10')
parser.add_argument('-k','--copies', type=int, required=True, help='Defines depth of the malicious circuit')


args = parser.parse_args()
ga(args.mal_type, args.copies)

# grover_2qbit()    
