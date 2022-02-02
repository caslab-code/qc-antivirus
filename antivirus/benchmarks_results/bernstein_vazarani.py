from qiskit import QuantumCircuit
from malicious_circuit_gen import malicious_circuit_gen

import sys
sys.path.append('../')
from pattern_matching import pattern_counter, bar_graph



def bv_circ(s, n, mal_type = None, copies = None, is_mal = False):
    # We need a circuit with n qubits, plus one auxiliary qubit
    # Also need n classical bits to write the output to
    bv_circuit = QuantumCircuit(n+1)

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
    

    # # Measurement
    # for i in range(n):
    #     bv_circuit.measure(i, i)
    
    if is_mal:
        victim_circ = bv_circuit
        malicious_circ = malicious_circuit_gen(mal_type, copies)
        circuit = QuantumCircuit(malicious_circ.num_qubits + victim_circ.num_qubits, malicious_circ.num_qubits + victim_circ.num_qubits)
        circuit.barrier()
        circuit.append(victim_circ, list(range(victim_circ.num_qubits)))
        circuit.append(malicious_circ, list(range(victim_circ.num_qubits, victim_circ.num_qubits + malicious_circ.num_qubits)))
        circuit = circuit.decompose()
        circuit.barrier()
        circuit.measure_all()
    else:
        circuit = bv_circuit
        circuit.measure_all()
    
    return circuit



def bv_pattern_matching(s, n, mal_type, copies, is_mal):
    #for our application s = "01", n = 2
    qc = bv_circ(s, n, mal_type, copies, is_mal)
    pt = malicious_circuit_gen(mal_type, 1)

    print("Malicious Circuit Type: " + mal_type + ". Pattern Count: " + str(pattern_counter(qc, pt)) + ". Bar graph: " + str(bar_graph(qc, pt)))
