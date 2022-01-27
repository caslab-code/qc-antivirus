# This code was modified based on ``qiskit.converters.circuit_to_dagdependency``.
# Main modification is to convert the quantum circuit to DAGNC instead of DAGDependency.
# Below is the license part of previous Qiskit file.
# -------------------------------------------------------------------------------
# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Helper function for converting a circuit to a DAGNC"""

from dagnc import DAGNC

def circuit_to_dagnc(circuit):
    """Build a ``DAGNC`` object from a ``QuantumCircuit``.

    Args:
        circuit (QuantumCircuit): the input circuits.

    Return:
        DAGNC: the ``DAGNC`` representing the input circuit as a dag with non-commutativity.
    """
    dagdependency = DAGNC()
    dagdependency.name = circuit.name
    dagdependency.metadata = circuit.metadata

    dagdependency.add_qubits(circuit.qubits)
    dagdependency.add_clbits(circuit.clbits)

    for register in circuit.qregs:
        dagdependency.add_qreg(register)

    for register in circuit.cregs:
        dagdependency.add_creg(register)

    for operation, qargs, cargs in circuit.data:
        dagdependency.add_op_node(operation, qargs, cargs)

    dagdependency._add_successors()

    dagdependency.calibrations = circuit.calibrations

    return dagdependency
