# initialization
import matplotlib.pyplot as plt
import numpy as np
import os,sys

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, assemble

# import basic plot tools
from qiskit.visualization import plot_histogram


def bv_algorithm(s, n):
    # We need a circuit with n qubits, plus one auxiliary qubit
    # Also need n classical bits to write the output to
    bv_circuit = QuantumCircuit(n+1, n)

    # put auxiliary in state |->
    bv_circuit.h(n)
    bv_circuit.z(n)

    # Apply Hadamard gates before querying the oracle
    for i in range(n):
        bv_circuit.h(i)

    # Apply barrier 
    bv_circuit.barrier()

    # Apply the inner-product oracle
    s = s[::-1] # reverse s to fit qiskit's qubit ordering
    for q in range(n):
        if s[q] == '0':
            bv_circuit.i(q)
        else:
            bv_circuit.cx(q, n)

    # Apply barrier 
    bv_circuit.barrier()

    #Apply Hadamard gates after querying the oracle
    for i in range(n):
        bv_circuit.h(i)
    
    # Measurement
    for i in range(n):
        bv_circuit.measure(i, i)
    
    return bv_circuit
 
    
def bv(s, n):
    n = int(n)
    bv_circuit = bv_algorithm(s, n)
    aer_sim = Aer.get_backend('aer_simulator')
    tranpiled_bv = transpile(bv_circuit, aer_sim)
    # FIXME antivirus should go here I think 
    f = open("transpiled_bv.json", "w")
    f.write(str(assemble(tranpiled_bv)))
    f.close()
    return tranpiled_bv

if __name__ == '__main__':
    bv(sys.argv[2], sys.argv[3])
    
    
