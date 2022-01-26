from itertools import permutations
from typing import Dict, Generator, List, Tuple, Union, Optional
from qiskit import QuantumCircuit, assemble
from qiskit.qobj import Qobj
from qiskit.qobj.qasm_qobj import QasmQobj, QasmQobjInstruction
# from qiskit.dagcircuit.dagdepnode import DAGDepNode

from networkx.algorithms.isomorphism import DiGraphMatcher
from retworkx import vf2_mapping

from circuit_to_dagnc import circuit_to_dagnc
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
    
    Yileds:
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
        # matcher = DiGraphMatcher(qc_net, pt_net, node_match = DAGDepNode.semantic_eq)

        for matching in matcher.subgraph_isomorphisms_iter():
            if check_matching(matching):
                yield matching

    elif matcher == 'retworkx':

        # retworkx representation for matching is under construction.
        # The main thing is that the output of vf2_mapping() in retworkx is the indices.
        # It is hard for us to check mapping with only indices instead of qargs for multi-qubit gates,

        raise Exception("retworkx representation for matching is underf construction!")
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



def histogram(
    qc: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    pt: Union[QuantumCircuit, QasmQobj, Qobj, List[QasmQobjInstruction]], 
    matcher : Optional[str] = "networkx"
    ) -> Dict[int, int]:
    """Return the histogram of the number of appearances of the pattern in the quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched.
        matcher: The algorithm to do the subgraph isomorphism searching. If set to ``networkx``,
            ``networkx.algorithms.isomorphism.DiGraphMatcher`` is used; if set to ``retworkx``,
            ``retworkx.vf2_mapping`` is used.
    
    Returns:
        The histogram of the number of appearances of the pattern in the quantum circuit.
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

        mapping = {} # keys are the mappings from the qc to the pt, and values are the matching
        for matching in matcher.subgraph_isomorphisms_iter():
            qargs = {} # store qubits mapping of currently transversed gates
            cargs = {} # store clbits mapping of currently transversed gates

            # Eaching matching is a ``dict``. The key is the node in the first graph, and the corresponding value is the matching node in the second graph
            for node_qc, node_pt in matching.items():
                for qubit_qc, qubit_pt in zip(node_qc.qargs, node_pt.qargs):
                    if qubit_qc.index in qargs:
                        if qubit_pt.index != qargs[qubit_qc.index]:
                            break
                    else:
                        qargs[qubit_qc.index] = qubit_pt.index
            
                for qubit_qc, qubit_pt in zip(node_qc.cargs, node_pt.cargs):
                    if qubit_qc.index in cargs:
                        if qubit_pt.index != cargs[qubit_qc.index]:
                            break
                    else:
                        cargs[qubit_qc.index] = qubit_pt.index
                
            mapping[[qargs, cargs]] = matching
        
        # now mapping contains all correct matching
        hist = {} # store the histogram


    elif matcher == 'retworkx':

        # retworkx representation for matching is under construction.
        # The main thing is that the output of vf2_mapping() in retworkx is the indices.
        # It is hard for us to check mapping with only indices instead of qargs for multi-qubit gates,

        raise Exception("retworkx representation for matching is underf construction!")
    else:
        raise Exception("Please specify the correct matcher!")