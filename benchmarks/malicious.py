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
from pattern_matching import match, pattern_counter, bar_graph
from utils import get_bits_mapping

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
    return mal_circuit

 


def malicious(mal_type ="M1", copies =1):
    qc = malicious_circuit_gen(copies,mal_type)
    pt = malicious_circuit_gen(copies,mal_type)
    print(qc)
    print(pt)


    print("--------------------------------------------------------------------------------------------------")
    print("\n1. Output details of all matching\n")
    for i, matching in enumerate(match(qc, pt)):
        print("Matching " + str(i+1) + ":\n")
        print("(a) Node mapping ({node in the quantum circuit: node in the pattern}):")
        print(matching)
        print("\n(b) Qubit and clbit index mapping:")
        mapping = get_bits_mapping(matching)
        print("Qubit index mapping is ({index in the quantum circuit: index in the pattern}): ")
        print(mapping[0])
        print("Clbit index mapping is ({index in the quantum circuit: index in the pattern}): ")
        print(mapping[1])
        print()
        print()
        print()

    
    return 

    
parser = argparse.ArgumentParser()
parser.add_argument('-m','--mal_type', type=str, required=True, help='Malicious Circuit type options M1 - M10')
parser.add_argument('-k','--copies', type=int, required=True, help='Defines depth of the malicious circuit')


args = parser.parse_args()
malicious(args.mal_type, args.copies)

# grover_2qbit()    
