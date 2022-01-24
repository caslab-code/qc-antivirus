from itertools import permutations
from typing import Dict, Generator, List, Tuple, Union, Optional
from qiskit import QuantumCircuit, assemble
from qiskit.qobj import Qobj
from qiskit.qobj.qasm_qobj import QasmQobj, QasmQobjInstruction

from networkx.algorithms.isomorphism import DiGraphMatcher

from circuit_to_dagdependency_antivirus import circuit_to_dagdependency_antivirus
from utils import circuit_to_networkx, check_matching



def match(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    pt: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    ) -> Generator:
    """Yield the matching of a pattern in a quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched.
    
    Yiled:
        The matching of a pattern in a quantum circuit.
    """

    qc_net = circuit_to_networkx(qc)
    pt_net = circuit_to_networkx(pt)

    def _gate_match(n1, n2):
        # def _arg_order(args):
        #     # return the order of the args indices
        #     indices = [bit.index for bit in args]
        #     return sorted(range(len(indices)), key = lambda x: indices[x])

        # only when all the following conditions are satified, we said that two nodes are equal:
        # 1. gate names are the same
        # 2. for multi-qubit gates, qubit orders are the same
        # 3. for multi-clbit gates, clbit orders are the same
        # return n1['name'] == n2['name'] and _arg_order(n1['qargs']) == _arg_order(n2['qargs']) and _arg_order(n1['cargs']) == _arg_order(n2['cargs'])
        return n1['name'] == n2['name']

    matcher = DiGraphMatcher(qc_net, pt_net, node_match=_gate_match)

    for matching in matcher.subgraph_isomorphisms_iter():
        if check_matching(matching):
            yield matching



def pattern_counter(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    pt: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    ) -> int:
    """Count the appearances of a pattern in a given quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched.
    
    Returns:
        The number of appearances of a pattern in a given quantum circuit.
    """

    return len(list(match(qc, pt)))