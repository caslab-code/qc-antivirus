from qiskit import QuantumCircuit
import search_pattern

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.h(1)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.cx(0, 1)

pt = QuantumCircuit(3)
pt.cx(0, 1)


qubit_map = [0, 1]

print(search_pattern.search_pattern_defined_bits(qc, pt, qubit_map))
print(search_pattern.pattern_histogram(qc, 'cx', qubit_map))
# print(search_pattern.pattern_histogram(qc, pt, qubit_map)) # this can also be used