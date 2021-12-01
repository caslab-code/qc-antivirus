from typing import List, Union, Optional
from qiskit import QuantumCircuit, assemble
from qiskit.qobj import Qobj
from qiskit.qobj.qasm_qobj import QasmQobjInstruction



def parse_qc(qc: Union[QuantumCircuit, Qobj]) -> List[QasmQobjInstruction]:
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



# TODO： (1) add classical bits and memory mappings
#        (2) qc does not contain less bits, mapping should not be duplicate
def map_bits(
    qc: Union[QuantumCircuit, Qobj], 
    qubit_map: List[int]
    ) -> List[QasmQobjInstruction]:
    """Return the instruction set after bit mapping.

    Args:
        qc : The quantum circuit to be searched through
        pt : The pattern to be searched
        qubit_map : The qubits indices mapping from the pattern to the quantum circuit.
            bit_map[i] is the nex qubit index in the quantum circuit of the qubit i in the pattern
    
    Returns:
        A ``list`` that contains a series of ``QasmQobjInstruction``, which are all
        instructions in the quantum circuits after qubit mapping.
    """

    ins_set_qc = parse_qc(qc)

    ins_set = []
    for ins in ins_set_qc:
        ins_set.append(QasmQobjInstruction(name = ins.name, qubits = [qubit_map[i] for i in ins.qubits]))
    
    return ins_set



def reduce_qc(
    qc: Union[QuantumCircuit, Qobj], 
    qubit_list: List[int],
    ) -> List[QasmQobjInstruction]:
    """Return the reduced instruction set of the quantum circuit, i.e., all instructions that involve qubits in qubit_list.

    Args:
        qc: The quantum circuit to be searched through
        qubit_list (list): The list of qubit indices to be considered.
    
    Returns:
        The reduced instruction set of the quantum circuit, i.e., all instructions that involve qubits in qubit_list.
    """

    ins_set_qc = parse_qc(qc)

    ins_set_qc_reduced = []
    for ins in ins_set_qc:
        for qubit in ins.qubits:
            if qubit in qubit_list:
                ins_set_qc_reduced.append(ins)
                break
    
    return ins_set_qc



def _pattern_matching_bf(
    string: List, 
    pt: List,
    is_overlap: Optional[bool] = True
    ) -> int:
    """Count the appearances of a pattern in a string using the brute force method.

    Args:
        strin: The string to be searched through
        pt: The pattern to be searched
        is_overlap: Whether the patterns are overlapped. Ex, searching ``aa`` in ``aaa``. If ``True``, 
            it returns 2. Otherwise, it returns 1.

    Returns:
        The number of appearances of the pattern in the string.
    """

    count = 0
    i = 0
    while i <= len(string) - len(pt):
        j = 0
        while j < len(pt):
            if string[i+j] != pt[j]:
                break
            j += 1
        if j == len(pt):
            count += 1
            if is_overlap:
                i += 1
            else:
                i += j
    
    return count



def search_pattern_defined_bits(
    qc: Union[QuantumCircuit, Qobj], 
    pt: Union[QuantumCircuit, Qobj], 
    qubit_map: List[int],
    is_overlap: Optional[bool] = True
    ) -> int:
    """Count the appearances of a pattern in a given quantum circuit.

    Args:
        qc: The quantum circuit to be searched through
        pt: The pattern to be searched
        qubit_map (list): The qubits indices mapping from the pattern to the quantum circuit.
            bit_map[i] is the nex qubit index in the quantum circuit of the qubit i in the pattern
        is_overlap: Whether the patterns are overlapped. Ex, searching ``aa`` in ``aaa``. If ``True``, 
            it returns 2. Otherwise, it returns 1.
    
    Returns:
        The number of appearances of the pattern in the string.
    """

    ins_set_pt = map_bits(pt, qubit_map)

    # create the reduced instruction set of the quantum circuit
    # the reduced instruction set contains all instructions in qc that involve target qubits
    ins_set_qc_reduced = reduce_qc(qc, qubit_map)
    
    # use common pattern matching algorithms to find the count
    # this method is strict, which means only the same pattern is counted
    count = _pattern_matching_bf(ins_set_qc_reduced, ins_set_pt, is_overlap)

    return count

