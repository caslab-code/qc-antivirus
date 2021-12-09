from itertools import permutations
from typing import Dict, List, Tuple, Union, Optional
from qiskit import QuantumCircuit, assemble
from qiskit.qobj import Qobj
from qiskit.qobj.qasm_qobj import QasmQobj, QasmQobjInstruction

# TODO:
# search_pattern_defined_bits() with string pt for one gate



def _count_num_bits(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]],
    bit_type: str = 'qubit'
    ) -> int:
    """Return the number of qubits of the given input.

    Args:
        qc: The input to count qubits. 
        bit_type: The type of the bits: one of ```qubit```, ```clbit```.

    Returns:
        The number of qubits in the given input.
    """
    if bit_type == 'qubit':
        if isinstance(qc, QuantumCircuit):
            num_bits = qc.num_qubits
        elif isinstance(qc, (QasmQobj, Qobj)):
            num_bits = qc.config.n_qubits
        elif isinstance(qc, List) and isinstance(qc[0], QasmQobjInstruction):
            num_bits = 0
            qubit_set = []
            for ins in qc:
                if hasattr(ins, 'qubits'):
                    for qubit in ins.qubits:
                        if qubit not in qubit_set:
                            num_bits += 1
                            qubit_set.append(qubit)
    elif bit_type == 'clbit':
        if isinstance(qc, QuantumCircuit):
            num_bits = qc.num_clbits
        elif isinstance(qc, (QasmQobj, Qobj)):
            num_bits = qc.config.memory_slots
        elif isinstance(qc, List) and isinstance(qc[0], QasmQobjInstruction):
            num_bits = 0
            clbit_set = []
            for ins in qc:
                if hasattr(ins, 'memory'):
                    for clbit in ins.memory:
                        if clbit not in clbit_set:
                            num_bits += 1
                            clbit_set.append(clbit)

    return num_bits



def parse_qc(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]]
    ) -> List[QasmQobjInstruction]:
    """Return the instruction set of the given quantum circuit.

    Args:
        qc: The quantum circuit to be parsed.

    Returns:
        A ``list`` that contains a series of ``QasmQobjInstruction``, which are all
        instructions in the quantum circuits.

    Raises:
        QiskitError: if the input cannot be interpreted as either circuits or schedules.
    """

    if isinstance(qc, QuantumCircuit):
        qc = assemble(qc)
    elif isinstance(qc, (QasmQobj, Qobj)):
        pass
    elif isinstance(qc, List) and isinstance(qc[0], QasmQobjInstruction):
        return qc
    else:
        raise TypeError("qc should be either QuantumCircuit or Qobj")

    instruction_set = qc.experiments[0].instructions
    
    return instruction_set



def map_bits(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    qubit_map: Optional[List[int]] = None,
    register_map: Optional[List[int]] = None,
    memory_map: Optional[List[int]] = None
    ) -> List[QasmQobjInstruction]:
    """Return the instruction set after bit mapping.

    Args:
        qc : The quantum circuit to be searched through.
        pt : The pattern to be searched.
        qubit_map : The qubits indices mapping from the pattern to the quantum circuit.
            qubit_map[i] is the qubit index in the quantum circuit of the qubit i in the pattern.
        register_map : The register indices mapping from the pattern to the quantum circuit.
            register_map[i] is the register index in the quantum circuit of the qubit i in the pattern.
        memory_map : The memory indices mapping from the pattern to the quantum circuit.
            bit_map[i] is the memory index in the quantum circuit of the qubit i in the pattern.
    
    Returns:
        A ``list`` that contains a series of ``QasmQobjInstruction``, which are all
        instructions in the quantum circuits after qubit mapping.
    """

    ins_set_qc = parse_qc(qc)

    ins_set = []
    for ins in ins_set_qc:
        if qubit_map and hasattr(ins, 'qubits'):
            ins.qubits = [qubit_map[i] for i in ins.qubits]
        if register_map and hasattr(ins, 'register'):
            ins.register = [register_map[i] for i in ins.register]
        if memory_map and hasattr(ins, 'memory'):
            ins.memory = [memory_map[i] for i in ins.memory]
        ins_set.append(ins)
    
    return ins_set



def reduce_qc(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    qubit_list: Optional[List[int]] = None,
    register_list: Optional[List[int]] = None,
    memory_list: Optional[List[int]] = None
    ) -> List[QasmQobjInstruction]:
    """Return the reduced instruction set of the quantum circuit, i.e., all instructions that involve qubits in qubit_list.

    Args:
        qc: The quantum circuit to be searched through.
        qubit_list: The list of qubit indices to be considered.
        register_list: The list of register indices to be considered.
        memory_list: The list of memory indices to be considered.
    
    Returns:
        The reduced instruction set of the quantum circuit, i.e., all instructions that involve qubits in qubit_list.
    """
    
    if _count_num_bits(qc, bit_type='qubit') < len(qubit_list):
        raise IndexError("Quantum Circuit has less qubits than qubit mapping")
    if len(set(qubit_list)) < len(qubit_list):
        raise ValueError("There is duplicate in qubit mapping")
    
    if _count_num_bits(qc, bit_type='clbit') < len(memory_list):
        raise IndexError("Quantum Circuit has less memory slots than memory mapping")
    if len(set(memory_list)) < len(memory_list):
        raise ValueError("There is duplicate in memory mapping")

    ins_set_qc = parse_qc(qc)

    ins_set_qc_reduced = []
    for ins in ins_set_qc:
        flag = False
        if qubit_list and hasattr(ins, 'qubits'):
            for qubit in ins.qubits:
                if qubit in qubit_list:
                    flag = True
                    break
        if not flag and register_list and hasattr(ins, 'register'):
            for register in ins.register:
                if register in register_list:
                    flag = True
                    break
        if not flag and memory_list and hasattr(ins, 'memory'):
            for memory in ins.memory:
                if memory in memory_list:
                    flag = True
                    break
        if flag:
            ins_set_qc_reduced.append(ins)
    
    return ins_set_qc_reduced



def _pattern_matching_bf(
    string: List, 
    pt: List,
    is_overlap: Optional[bool] = True
    ) -> int:
    """Count the appearances of a pattern in a string using the brute force method.

    Args:
        strin: The string to be searched through.
        pt: The pattern to be searched.
        is_overlap: Whether the patterns are overlapped. Ex, searching ``aa`` in ``aaa``. If ``True``, 
            it returns 2. Otherwise, it returns 1.

    Returns:
        The number of appearances of the pattern in the string.
    """

    i, count = 0, 0
    while i <= len(string) - len(pt):
        j = 0
        while j < len(pt):
            if string[i+j] != pt[j]:
                break
            j += 1
        if j == len(pt):
            count += 1
            if not is_overlap:
                i += j - 1
        i += 1
    
    return count



def search_pattern_defined_bits(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    pt: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    qubit_map: Optional[List[int]] = None,
    register_map: Optional[List[int]] = None,
    memory_map: Optional[List[int]] = None,
    is_overlap: Optional[bool] = True
    ) -> int:
    """Count the appearances of a pattern in a given quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched.
        qubit_map : The qubits indices mapping from the pattern to the quantum circuit.
            qubit_map[i] is the qubit index in the quantum circuit of the qubit i in the pattern
        register_map : The register indices mapping from the pattern to the quantum circuit.
            register_map[i] is the register index in the quantum circuit of the qubit i in the pattern
        memory_map : The memory indices mapping from the pattern to the quantum circuit.
            bit_map[i] is the memory index in the quantum circuit of the qubit i in the pattern
        is_overlap: Whether the patterns are overlapped. Ex, searching ``aa`` in ``aaa``. If ``True``, 
            it returns 2. Otherwise, it returns 1.
    
    Returns:
        The number of appearances of the pattern in the quantum circuit.
    """

    if not qubit_map:
        qubit_map = list(range(_count_num_bits(pt, bit_type='qubit')))
    if not memory_map:
        memory_map = list(range(_count_num_bits(pt, bit_type='clbit')))

    ins_set_pt = map_bits(pt, qubit_map=qubit_map, register_map=register_map, memory_map=memory_map)

    # create the reduced instruction set of the quantum circuit
    # the reduced instruction set contains all instructions in qc that involve target qubits
    ins_set_qc_reduced = reduce_qc(qc, qubit_list=qubit_map, register_list=register_map, memory_list=memory_map)
    
    # use common pattern matching algorithms to find the count
    # this method is strict, which means only the same pattern is counted
    count = _pattern_matching_bf(ins_set_qc_reduced, ins_set_pt, is_overlap)

    return count



def search_pattern_permutated(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    pt: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    is_overlap: Optional[bool] = True
    ) -> List[Tuple[int]]:
    """Count the appearances of a pattern in a given quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched.
        is_overlap: Whether the patterns are overlapped. Ex, searching ``aa`` in ``aaa``. If ``True``, 
            it returns 2. Otherwise, it returns 1.
    
    Returns:
        A list of tuples where the first item of the tuple is the qubit map, the second item of the tuple
            is the memory map, and the second item of the tuple is the number of appearances of the pattern
            in the quantum circuit for this qubit map.
    """

    num_qubits = _count_num_bits(qc, bit_type='qubit')
    num_memories = _count_num_bits(qc, bit_type='clbit')

    count = []
    for qubit_map in permutations(range(num_qubits), _count_num_bits(pt, bit_type='qubit')):
        for memory_map in permutations(range(num_memories), _count_num_bits(pt, bit_type='clbit')):
            count_defined_bits = search_pattern_defined_bits(qc, pt, qubit_map=qubit_map, memory_map=memory_map, is_overlap=is_overlap)
            if count_defined_bits > 0:
                count.append((qubit_map, memory_map, count_defined_bits))

    return count



def count_pattern(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    pt: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    is_overlap: Optional[bool] = True
    ) -> List[Tuple[int]]:
    """Count the appearances of a pattern in a given quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched.
        is_overlap: Whether the patterns are overlapped. Ex, searching ``aa`` in ``aaa``. If ``True``, 
            it returns 2. Otherwise, it returns 1.
    
    Returns:
        The number of appearances of a pattern in a given quantum circuit.
    """

    num_qubits = _count_num_bits(qc, bit_type='qubit')
    num_memories = _count_num_bits(qc, bit_type='clbit')

    count = 0
    for qubit_map in permutations(range(num_qubits), _count_num_bits(pt, bit_type='qubit')):
        for memory_map in permutations(range(num_memories), _count_num_bits(pt, bit_type='clbit')):
            count += search_pattern_defined_bits(qc, pt, qubit_map=qubit_map, memory_map=memory_map, is_overlap=is_overlap)

    return count



def pattern_histogram(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    pt: Union[QuantumCircuit, Qobj, List[QasmQobjInstruction], str], 
    qubit_map: Optional[List[int]] = None,
    register_map: Optional[List[int]] = None,
    memory_map: Optional[List[int]] = None,
    ) -> Dict[int, int]:
    """Return the histogram of the number of appearances of the pattern in the quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched. ``str`` type input only applies to one gate pattern.
        qubit_map (list): The qubits indices mapping from the pattern to the quantum circuit.
            bit_map[i] is the nex qubit index in the quantum circuit of the qubit i in the pattern
        register_map : The register indices mapping from the pattern to the quantum circuit.
            register_map[i] is the register index in the quantum circuit of the qubit i in the pattern
        memory_map : The memory indices mapping from the pattern to the quantum circuit.
            bit_map[i] is the memory index in the quantum circuit of the qubit i in the pattern
    
    Returns:
        The histogram of the number of appearances of the pattern in the quantum circuit.
    """

    if not qubit_map:
        qubit_map = list(range(_count_num_bits(pt, bit_type='qubit')))
    if not memory_map:
        memory_map = list(range(_count_num_bits(pt, bit_type='clbit')))

    if isinstance(pt, str):
        pt_circ = QuantumCircuit(2)
        try:
            getattr(pt_circ, pt)()
        except:
            getattr(pt_circ, pt)(0, 1)
        pt = pt_circ
    ins_set_pt = map_bits(pt, qubit_map=qubit_map, register_map=register_map, memory_map=memory_map)

    # create the reduced instruction set of the quantum circuit
    # the reduced instruction set contains all instructions in qc that involve target qubits
    ins_set_qc_reduced = reduce_qc(qc, qubit_list=qubit_map, register_list=register_map, memory_list=memory_map)
    ins_set_qc_reduced.append(None) # always break from the internal while loop and counts
                                    # Otherwise it may skip counting the last pattern
    
    hist = {}
    i, count = 0, 0
    while i <= len(ins_set_qc_reduced) - len(ins_set_pt):
        j = 0
        while j < len(ins_set_pt):
            if ins_set_qc_reduced[i+j] != ins_set_pt[j]:
                break
            j += 1
        if j == len(ins_set_pt):
            count += 1
            i += j - 1
        else:
            if count in hist.keys():
                hist[count] += 1
            else:
                hist[count] = 1
            count = 0
        i += 1

    if 0 in hist.keys():
        del hist[0]

    return hist
