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
