from qiskit import QuantumCircuit
from isomorphism import histogram, pattern_counter, match
# from utils import get_bits_mapping
from utils import *
from circuit_to_dagnc import circuit_to_dagnc


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
qc_dag = circuit_to_dagnc(qc)
for i in qc_dag.get_nodes():
    print(i.node_id)
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
print("--------------------------------------------------------")
print("1. Output details of all matching\n")
for i, matching in enumerate(match(qc, pt)):
    print("Matching " + str(i+1))
    print(matching)
    mapping = get_bits_mapping(matching)
    print("qubit mapping is: ")
    print(mapping[0])
    print("clbit mapping is: ")
    print(mapping[1])
    print()

# 2. Pattern counter:
#       Count how many patterns in the quantum circuit.
print("--------------------------------------------------------")
print("2. Pattern counter\n")
print("The pattern count in the quantum circuit is: " + str(pattern_counter(qc, pt, matcher="networkx")))
print()

# 3. Pattern histogram:
#       Histogram of the pattern in the circuit.
#       The return value is a dict, whose keys are how many times the pattern appears in series
#       and values are the counts for them.
print("--------------------------------------------------------")
print("3. Pattern histogram\n")
print("The return value is a dict, whose keys are how many times the pattern appears in series and values are the counts for them.")
print(histogram(qc, pt, matcher="networkx"))