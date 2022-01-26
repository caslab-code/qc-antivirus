# initialization
import numpy as np
import os
import argparse


# importing Qiskit
import qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, assemble, transpile

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



def dj_oracle(case, n):
    # We need to make a QuantumCircuit object to return
    # This circuit has n+1 qubits: the size of the input,
    # plus one output qubit
    oracle_qc = QuantumCircuit(n+1)
    
    # First, let's deal with the case in which oracle is balanced
    if case == "balanced":
        # First generate a random number that tells us which CNOTs to
        # wrap in X-gates:
        b = np.random.randint(1,2**n)
        # Next, format 'b' as a binary string of length 'n', padded with zeros:
        b_str = format(b, '0'+str(n)+'b')
        # Next, we place the first X-gates. Each digit in our binary string 
        # corresponds to a qubit, if the digit is 0, we do nothing, if it's 1
        # we apply an X-gate to that qubit:
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
        # Do the controlled-NOT gates for each qubit, using the output qubit 
        # as the target:
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
        # Next, place the final X-gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)

    # Case in which oracle is constant
    if case == "constant":
        # First decide what the fixed output of the oracle will be
        # (either always 0 or always 1)
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)
    
    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle" # To show when we display the circuit
    return oracle_gate


def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n+1, n)
    # Set up the output qubit:
    dj_circuit.x(n)
    dj_circuit.h(n)
    # And set up the input register:
    for qubit in range(n):
        dj_circuit.h(qubit)
    # Let's append the oracle gate to our circuit:
    dj_circuit.append(oracle, range(n+1))
    # Finally, perform the H-gates again and measure:
    for qubit in range(n):
        dj_circuit.h(qubit)
    
    for i in range(n):
        dj_circuit.measure(i, i)
    
    return dj_circuit
    
# def dj_old(case, n):
    # n = int(n)
    # oracle = dj_oracle(case,n)
    # dj_circuit = dj_algorithm(oracle,n)
    # aer_sim = Aer.get_backend('aer_simulator')
    # transpiled_dj = transpile(dj_circuit, aer_sim) 
    ##f = open("transpiled_dj.json", "w")
    ##f.write(str(assemble(transpiled_dj)))
    ##f.close()
    # total_pattern = 0
    # print("Search Pattern:") 
    # print(pt)
    # for i in range(0,n-1):
        # for j in range(i+1, n):
            ##print(i,j)
            # pattern = search_pattern.search_pattern_defined_bits(transpiled_dj, pt, [j,i])
            # print("No. of patterns detected between Qbit",i,"and Qbit",j, "are", pattern)
            # total_pattern = total_pattern + pattern
    
    # print("Total Number of Patterns detected", total_pattern)
    # return 
    
def dj(case, n, mal_type ="M1", copies =1):
    #for our application case = "balanced", n = 2
    n = int(n)
    oracle = dj_oracle(case,n)
    qc = dj_algorithm(oracle,n)
    pt = malicious_circuit_gen(copies, mal_type)
    
    print("--------------------------------------------------------")
    print("Deutsch-Josza Circuit", "\n Case = ", case, "\n Number of Qubits =", n) 
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
parser.add_argument('-c','--case', type=str, required=True, help='Select one from two options: 1. "balanced" 2. "constant" ')
parser.add_argument('-w','--width', type=int, required=True, help='Width of input string')
parser.add_argument('-m','--mal_type', type=str, required=True, help='Malicious Circuit type options M1 - M10')
parser.add_argument('-k','--copies', type=int, required=True, help='Defines depth of the malicious circuit')


args = parser.parse_args()
dj(args.case, args.width, args.mal_type, args.copies)