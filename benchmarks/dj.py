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
sys.path.append('./qc-antivirus/antivirus')
import search_pattern

#sample pattern
pt = QuantumCircuit(2)
pt.cx(1, 0)
pt.cx(1, 0)


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
    
def dj(case, n):
    n = int(n)
    oracle = dj_oracle(case,n)
    dj_circuit = dj_algorithm(oracle,n)
    aer_sim = Aer.get_backend('aer_simulator')
    transpiled_dj = transpile(dj_circuit, aer_sim) 
    # f = open("transpiled_dj.json", "w")
    # f.write(str(assemble(transpiled_dj)))
    # f.close()
    total_pattern = 0
    print("Search Pattern:") 
    print(pt)
    for i in range(0,n-1):
        for j in range(i+1, n):
            # print(i,j)
            pattern = search_pattern.search_pattern_defined_bits(transpiled_dj, pt, [j,i])
            print("No. of patterns detected between Qbit",i,"and Qbit",j, "are", pattern)
            total_pattern = total_pattern + pattern
    
    print("Total Number of Pattern detected", total_pattern)
    return 

parser = argparse.ArgumentParser()
parser.add_argument('-c','--case', type=str, required=True, help='Select one from two options: 1. "balanced" 2. "constant" ')
parser.add_argument('-w','--width', type=int, required=True, help='Width of input string')
args = parser.parse_args()
dj(args.case, args.width)