from collections import OrderedDict
from typing import Dict, Generator, List, Tuple, Union, Optional
from qiskit import QuantumCircuit, assemble
from qiskit.qobj import Qobj
from qiskit.qobj.qasm_qobj import QasmQobj, QasmQobjInstruction
# from qiskit.dagcircuit.dagdepnode import DAGDepNode

from networkx.algorithms.isomorphism import DiGraphMatcher
from retworkx import vf2_mapping

from circuit_to_dagnc import circuit_to_dagnc
from utils import circuit_to_network, check_matching, get_bits_mapping, nxmatching_to_id, reduce_qc



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
    matcher : Optional[str] = "networkx"
    ) -> int:
    """Count the appearances of a pattern in a given quantum circuit.

    Args:
        qc: The quantum circuit to be searched through.
        pt: The pattern to be searched.
        matcher: The algorithm to do the subgraph isomorphism searching. If set to ``networkx``,
            ``networkx.algorithms.isomorphism.DiGraphMatcher`` is used; if set to ``retworkx``,
            ``retworkx.vf2_mapping`` is used.
    
    Returns:
        The number of appearances of a pattern in a given quantum circuit.
    """

    return len(list(match(qc, pt, matcher=matcher)))



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

        # step (1)
        # Find all correct subgraph isomorphism, and group node mapping together if their qubit
        # and clbit mapping are the same

        mapping = [] # store all mappings of currently iterated matchings
        id_matchings = [] # store all id matchings with the same bits mappings
                        # the first dimension is for different bits mappings
                        # the second dimension is for different subgraph isomorphism with
                        # the same bits mappings, and they are in ascending order
        for matching in match(qc, pt, matcher="networkx"):
            # the mappings in bits_mapping and id_matchings with the same index are the same
            bits_mapping = get_bits_mapping(matching)
            if bits_mapping in mapping:
                id_matchings[mapping.index(bits_mapping)].append(sorted(nxmatching_to_id(matching).keys()))
            else:
                mapping.append(bits_mapping)
                id_matchings.append([sorted(nxmatching_to_id(matching).keys())])

        for matchings_with_same_mapping in id_matchings:
            matchings_with_same_mapping.sort(key = lambda x: x[0])

        # step (2)
        # calculate the histogram

        def _get_bit_indices(id_mapping):
            """Return all indices of the mapping
            """
            return [id for id in id_mapping]

        # now mapping contains all correct matching
        qc_dagnc = circuit_to_dagnc(qc)
        hist = {} # store the histogram

        for mapp, id_matching in zip(mapping, id_matchings):
            qubit_list = _get_bit_indices(mapp[0].keys())
            clbit_list = _get_bit_indices(mapp[1].keys())
            reduced_node_ids = reduce_qc(qc_dagnc, qubit_list, clbit_list, is_node_id=True)
            # node_ids store the found pattern node ids as a two-level list
            # the first dimension stores all matchings with the same mapping
            # the second dimension stores the ordered node ids of each pattern

            num_pt_op = pt.size()
            curr = 0 # index of the current start of the histogram
            count = 1
            id_matching.append([-1]) # to make it consistent
            for i in range(1, len(id_matching)):
                if i == len(id_matching) - 1:
                    if count in hist:
                        hist[count] += 1
                    else:
                        hist[count] = 1
                    break
                curr_start = reduced_node_ids.index(id_matching[curr][0])
                p_start = reduced_node_ids.index(id_matching[i][0])
                if p_start - curr_start == num_pt_op:
                    count += 1
                else:
                    if count in hist:
                        hist[count] += 1
                    else:
                        hist[count] = 1
                    count = 1
                curr += 1
        return hist

    elif matcher == 'retworkx':

        # retworkx representation for matching is under construction.
        # The main thing is that the output of vf2_mapping() in retworkx is the indices.
        # It is hard for us to check mapping with only indices instead of qargs for multi-qubit gates,

        raise Exception("retworkx representation for matching is underf construction!")
    else:
        raise Exception("Please specify the correct matcher!")