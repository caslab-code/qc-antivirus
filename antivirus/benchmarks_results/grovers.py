from qiskit import QuantumCircuit
from malicious_circuit_gen import malicious_circuit_gen

import sys
sys.path.append('../')
from pattern_matching import pattern_counter, bar_graph



def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc



def ga_circ(mal_type = None, copies = None, is_mal = False): # k- decides the depth of the malicious circuit and d is the delay value
    grover_circuit = QuantumCircuit(2)
    grover_circuit = initialize_s(grover_circuit, [0,1])
    grover_circuit.cz(0,1) # Oracle
    grover_circuit.h([0,1])
    grover_circuit.z([0,1])
    grover_circuit.cz(0,1)
    grover_circuit.h([0,1])

    if is_mal:
        victim_circ = grover_circuit
        malicious_circ = malicious_circuit_gen(mal_type, copies)
        circuit = QuantumCircuit(malicious_circ.num_qubits + victim_circ.num_qubits, malicious_circ.num_qubits + victim_circ.num_qubits)
        circuit.barrier()
        circuit.append(victim_circ, list(range(victim_circ.num_qubits)))
        circuit.append(malicious_circ, list(range(victim_circ.num_qubits, victim_circ.num_qubits + malicious_circ.num_qubits)))
        circuit = circuit.decompose()
        circuit.barrier()
        circuit.measure_all()
    else:
        circuit = grover_circuit
        circuit.measure_all()

    return circuit



def ga_pattern_matching(mal_type, copies, is_mal):
    qc = ga_circ(mal_type, copies, is_mal)
    pt = malicious_circuit_gen(mal_type, 1)

    print("Malicious Circuit Type: " + mal_type + ". Pattern Count: " + str(pattern_counter(qc, pt)) + ". Bar graph: " + str(bar_graph(qc, pt)))
    