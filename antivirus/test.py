from qiskit import QuantumCircuit
from search_pattern import search_pattern_defined_bits

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.h(1)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)

pt = QuantumCircuit(3)
pt.h(1)
pt.cx(1, 0)
pt.cx(1, 0)

bit_map = [1, 0]

print(search_pattern_defined_bits(qc, pt, bit_map))