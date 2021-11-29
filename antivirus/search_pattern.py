from logging import error
from typing import List, Union
from qiskit import QuantumCircuit, assemble
from qiskit.qobj import Qobj
from qiskit.qobj.qasm_qobj import QasmQobjInstruction



def parse_qc(qc: Union[QuantumCircuit, Qobj]) -> List:
    """Return the instruction set of the given quantum circuit.

    Args:
        qc: The quantum circuit to be parsed

    Returns:
        A ``list`` that contains a series of ``QasmQobjInstruction``, which are all
        instructions in the quantum circuits.

    Raises:
        QiskitError: if the input cannot be interpreted as either circuits or schedules
    """

    if isinstance(qc, QuantumCircuit):
        qc = assemble(qc)
    elif isinstance(qc, Qobj):
        pass
    else:
        raise TypeError("qc should be either QuantumCircuit or Qobj")

    instruction_set = qc.experiments[0].instructions
    
    return instruction_set



def map_bits(
    qc: Union[QuantumCircuit, Qobj], 
    bit_map: List[int]
    ) -> List[QasmQobjInstruction]:
    """Return the instruction set after bit mapping.

    Args:
        qc : The quantum circuit to be searched through
        pt : The pattern to be searched
        bit_map : The qubits indices mapping from the pattern to the quantum circuit.
            bit_map[i] is the nex qubit index in the quantum circuit of the qubit i in the pattern
    
    Returns:
        A ``list`` that contains a series of ``QasmQobjInstruction``, which are all
        instructions in the quantum circuits after qubit mapping.
    """

    ins_set_qc = parse_qc(qc)

    ins_set = []
    for ins in ins_set_qc:
        ins_set.append(QasmQobjInstruction(name = ins.name, qubits = [bit_map[i] for i in ins.qubits]))
    
    return ins_set



def _pattern_matching_bf(
    string: List, 
    pt: List
    ) -> int:
    """Count the appearance of a pattern in a string using the brute force method.

    Args:
        string (list): The string to be searched through
        pt (list): The pattern to be searched

    Returns:
        The number of appearance of the pattern in the string.
    """

    count = 0
    for i in range(len(string) - len(pt) + 1):
        j = 0
        while j < len(pt):
            if string[i+j] != pt[j]:
                break
            j += 1
        if j == len(pt):
            count += 1
    
    return count



def search_pattern_defined_bits(
    qc: Union[QuantumCircuit, Qobj], 
    pt: Union[QuantumCircuit, Qobj], 
    bit_map: List[int]
    ) -> int:
    """Count the appearance of a pattern in a given quantum circuit.

    Args:
        qc (QuantumCircuit): The quantum circuit to be searched through
        pt (QuantumCircuit): The pattern to be searched
        bit_map (list): The qubits indices mapping from the pattern to the quantum circuit.
            bit_map[i] is the nex qubit index in the quantum circuit of the qubit i in the pattern
    """

    ins_set_qc = parse_qc(qc)
    ins_set_pt = map_bits(pt, bit_map)

    # create the reduced instruction set of the quantum circuit
    # the reduced instruction set contains all instructions in qc that involve target qubits
    ins_set_qc_reduced = []
    for ins in ins_set_qc:
        for qubit in ins.qubits:
            if qubit in bit_map:
                ins_set_qc_reduced.append(ins)
                break
    
    # use common pattern matching algorithms to find the count
    # this method is strict, which means only the same pattern is counted
    count = _pattern_matching_bf(ins_set_qc_reduced, ins_set_pt)

    return count


