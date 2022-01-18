from qiskit import QuantumCircuit
import search_pattern
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

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
print("Patter Circuit")
print(pt)
print("Input Circuit")
print(qc)
print(search_pattern.search_pattern_defined_bits(qc, pt, qubit_map))

cx_hist = search_pattern.pattern_histogram(qc, 'cx', qubit_map)
print(cx_hist)

plt.bar(cx_hist.keys(), cx_hist.values())
plt.xlabel('Number of CX gates')
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.ylabel('Count')
plt.gca().yaxis.set_major_locator(MultipleLocator(1))
plt.title('Histogram of CX Gates')
plt.show()


# print(search_pattern.pattern_histogram(qc, pt, qubit_map)) # this can also be used

