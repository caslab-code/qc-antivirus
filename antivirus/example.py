from qiskit import QuantumCircuit
from pattern_matching import  match, pattern_counter, bar_graph
from utils import get_bits_mapping, dump


# ------------------------------------------------------------------------------------
# Define the circuit and the pattern
# ------------------------------------------------------------------------------------

# define circuit on which we perform pattern matching
# example circuit is:
#      ┌───┐          ┌───┐
# q_0: ┤ H ├──■────■──┤ H ├──■────■──
#      └───┘┌─┴─┐┌─┴─┐├───┤┌─┴─┐┌─┴─┐
# q_1: ─────┤ X ├┤ X ├┤ H ├┤ X ├┤ X ├
#           ├───┤└───┘├───┤├───┤└───┘
# q_2: ─────┤ X ├─────┤ X ├┤ H ├─────
#      ┌───┐└─┬─┘┌───┐└─┬─┘└───┘
# q_3: ┤ H ├──■──┤ H ├──■────────────
#      └───┘     └───┘
# q_4: ──────────────────────────────

qc = QuantumCircuit(5)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.h(1)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.h(3)
qc.cx(3, 2)
qc.h(3)
qc.cx(3, 2)
qc.h(2)
# print(qc.draw('text'))


# define pattern to be matched
# example circuit is:
#      ┌───┐     
# q_0: ┤ H ├──■──
#      └───┘┌─┴─┐
# q_1: ─────┤ X ├
#           └───┘

pt = QuantumCircuit(2)
pt.h(0)
pt.cx(0, 1)
# print(pt.draw('text'))



# ------------------------------------------------------------------------------------
# Examples of antivirus functions
# ------------------------------------------------------------------------------------
print("Examples of antivirus functions\n")
print("The quantum circuit is:")
print(qc.draw('text'))
print("\nThe pattern is:")
print(pt.draw('text'))
print()

# 1. Output details of all matching:
#       Return a generator which generates the matching. Each item is a dict, whose
#       key is the corresponding matching node in the quantum circuit and value is
#       the node in the pattern. The type of the node is ``qiskit.dagcircuit.dagdepnode.DAGDepNode``.
print("--------------------------------------------------------------------------------------------------")
print("\n1. Output details of all matching\n")
for i, matching in enumerate(match(qc, pt)):
    print("Matching " + str(i+1) + ":\n")
    print("(a) Node mapping ({node in the quantum circuit: node in the pattern}):")
    print(matching)
    print("\n(b) Qubit and clbit index mapping:")
    mapping = get_bits_mapping(matching)
    print("Qubit index mapping is ({index in the quantum circuit: index in the pattern}): ")
    print(mapping[0])
    print("Clbit index mapping is ({index in the quantum circuit: index in the pattern}): ")
    print(mapping[1])
    print()
    print()
    print()



# 2. Pattern counter:
#       Count how many patterns in the quantum circuit.
print("--------------------------------------------------------------------------------------------------")
print("\n2. Pattern counter\n")
print("The appearances of the pattern in the quantum circuit is: " + str(pattern_counter(qc, pt, matcher="networkx")))
print()



# 3. Pattern histogram:
#       Histogram of the pattern in the circuit.
#       The return value is a dict, whose keys are how many times the pattern appears in series
#       and values are the counts for them.
print("--------------------------------------------------------------------------------------------------")
print("\n3. Pattern histogram\n")
print("{Number of the pattern in a continuous appearance: count for this appearance}")
print(bar_graph(qc, pt, matcher="networkx"))



# 4. Dump the results as a json file
print("--------------------------------------------------------------------------------------------------")
print("\n4. Dump the results as a json file\n")
dump(qc, pt, "example_matching.json")
print('Please find the file "example_matching.json"')