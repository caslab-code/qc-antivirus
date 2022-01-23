from qiskit import QuantumCircuit

from antivirus import pattern_counter

# define circuit on which we perform pattern matching
# example circuit is:
#      ┌───┐          ┌───┐     
# q_0: ┤ H ├──■────■──┤ H ├─────
#      └───┘┌─┴─┐┌─┴─┐├───┤
# q_1: ─────┤ X ├┤ X ├┤ H ├─────
#           └───┘├───┤├───┤┌───┐
# q_2: ──■────■──┤ H ├┤ X ├┤ H ├
#      ┌─┴─┐┌─┴─┐└───┘└─┬─┘└───┘
# q_3: ┤ X ├┤ X ├───────■───────
#      └───┘└───┘
# q_4: ─────────────────────────

qc = QuantumCircuit(5)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)
qc.h(1)
qc.h(0)
qc.cx(2, 3)
qc.cx(2, 3)
qc.h(2)
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

print(pattern_counter(qc, pt))