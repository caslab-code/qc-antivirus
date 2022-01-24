from itertools import permutations
from typing import Dict, Generator, List, Tuple, Union, Optional
from qiskit import QuantumCircuit, assemble
from qiskit.qobj import Qobj
from qiskit.qobj.qasm_qobj import QasmQobj, QasmQobjInstruction

from networkx.algorithms.isomorphism import DiGraphMatcher
from retworkx import vf2_mapping

from circuit_to_dagdependency_antivirus import circuit_to_dagdependency_antivirus
from utils import circuit_to_network, check_matching



def match(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    pt: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    matcher : Optional[str] = "networkx"
    ) -> Generator:
    """Yield the matching of a pattern in a quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched.
        matcher: The algorithm to do the subgraph isomorphism searching. If set to ``networkx``,
            ``networkx.algorithms.isomorphism.DiGraphMatcher`` is used; if set to ``retworkx``,
            ``retworkx.vf2_mapping`` is used.
    
    Yiled:
        The matching of a pattern in a quantum circuit.
    """

    if matcher == 'networkx':
        qc_net = circuit_to_network(qc, network_type="networkx")
        pt_net = circuit_to_network(pt, network_type="networkx")

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

        matcher = DiGraphMatcher(qc_net, pt_net, node_match = _gate_match)

        for matching in matcher.subgraph_isomorphisms_iter():
            if check_matching(matching):
                yield matching
    elif matcher == 'retworkx':

        # retworkx representation for matching is under construction.
        # The main thing is that the output of vf2_mapping() in retworkx is the indices.
        # It is hard for us to check mapping with only indices instead of qargs for multi-qubit gates,

        raise Exception("retworkx representation for matching is underf construction!")

        # def _gate_match(n1, n2):
        #     # def _arg_order(args):
        #     #     # return the order of the args indices
        #     #     indices = [bit.index for bit in args]
        #     #     return sorted(range(len(indices)), key = lambda x: indices[x])

        #     # only when all the following conditions are satified, we said that two nodes are equal:
        #     # 1. gate names are the same
        #     # 2. for multi-qubit gates, qubit orders are the same
        #     # 3. for multi-clbit gates, clbit orders are the same
        #     # return n1['name'] == n2['name'] and _arg_order(n1['qargs']) == _arg_order(n2['qargs']) and _arg_order(n1['cargs']) == _arg_order(n2['cargs'])
        #     return n1.name == n2.name

        # qc_net = circuit_to_network(qc, network_type="retworkx")
        # pt_net = circuit_to_network(pt, network_type="retworkx")
        # for matching in vf2_mapping(qc_net, pt_net, node_matcher = _gate_match, subgraph = True):
        #     if check_matching(matching):
        #         yield matching
    else:
        raise Exception("Please specify the correct matcher!")



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