from dagdependency_antivirus import DAGDependency_antivirus

def circuit_to_dagdependency_antivirus(circuit):
    """Build a ``DAGDependency`` object from a ``QuantumCircuit``.

    Args:
        circuit (QuantumCircuit): the input circuits.

    Return:
        DAGDependency: the DAG representing the input circuit as a dag dependency.
    """
    dagdependency = DAGDependency_antivirus()
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
