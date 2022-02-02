from qiskit import QuantumCircuit
from malicious_circuit_gen import malicious_circuit_gen
import numpy as np

import sys
sys.path.append('../')
from pattern_matching import pattern_counter, bar_graph



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



def dj_circ(case, n,mal_type = None, copies = None, is_mal = False):
    dj_circuit = QuantumCircuit(3)
    # Set up the output qubit:
    dj_circuit.x(2)
    dj_circuit.h(2)
    # And set up the input register:
    for qubit in range(2):
        dj_circuit.h(qubit)
    # Let's append the oracle gate to our circuit:
    oracle = dj_oracle(case, n)
    dj_circuit.append(oracle, [0,1,2])
    # Finally, perform the H-gates again and measure:
    for qubit in range(2):
        dj_circuit.h(qubit)
    
    if is_mal:
        victim_circ = dj_circuit
        malicious_circ = malicious_circuit_gen(mal_type, copies)
        circuit = QuantumCircuit(malicious_circ.num_qubits + victim_circ.num_qubits, malicious_circ.num_qubits + victim_circ.num_qubits)
        circuit.barrier()
        circuit.append(victim_circ, list(range(victim_circ.num_qubits)))
        circuit.append(malicious_circ, list(range(victim_circ.num_qubits, victim_circ.num_qubits + malicious_circ.num_qubits)))
        circuit = circuit.decompose()
        circuit.barrier()
        circuit.measure_all()
    else:
        circuit = dj_circuit
        circuit.measure_all()
    
    return circuit



def dj_pattern_matching(case, n, mal_type, copies, is_mal):
    #for our application case = "balanced", n = 2
    qc = dj_circ(case, n, mal_type, copies, is_mal)
    pt = malicious_circuit_gen(mal_type, 1)

    print("Malicious Circuit Type: " + mal_type + ". Pattern Count: " + str(pattern_counter(qc, pt)) + ". Bar graph: " + str(bar_graph(qc, pt)))
