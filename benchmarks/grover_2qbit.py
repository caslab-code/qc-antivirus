#initialization
import matplotlib.pyplot as plt
import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy

# import basic plot tools
from qiskit.visualization import plot_histogram



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
    f = open("transpiled_grover_2qbit.json", "w")
    f.write(str(assemble(tranpiled_grover_circuit)))
    f.close()
    return tranpiled_grover_circuit

    

grover_2qbit()    
