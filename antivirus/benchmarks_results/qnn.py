import argparse
from qiskit import QuantumCircuit
from malicious_circuit_gen import malicious_circuit_gen

import sys
sys.path.append('../')
from pattern_matching import pattern_counter, match, bar_graph



def qnn_circ(qnn_type, mal_type = None, copies = None, is_mal = False):

    qnn_circuit_short = """OPENQASM 2.0;
                    include "qelib1.inc";
                    qreg q[2];
                    ry(0.5) q[0];
                    ry(0.5) q[1];
                    rz(0.5) q[0];
                    rz(0.5) q[1];
                    rx(0.5) q[0];
                    rx(0.5) q[1];
                    ry(0.5) q[0];
                    ry(0.5) q[1];
                    rz(0.5) q[0];
                    rz(0.5) q[1];
                    rx(0.5) q[0];
                    rx(0.5) q[1];
                    ry(0.5) q[0];
                    ry(0.5) q[1];
                    rz(0.5) q[0];
                    rz(0.5) q[1];
                    u3(2.4018686,2.6075468,-0.73598874) q[0];
                    u3(2.8859026,-0.68833423,0.63394415) q[1];
                    cu3(-1.5295002,1.8450029,2.7694488) q[0],q[1];
                    cu3(-2.3047609,2.7306604,0.5879783) q[1],q[0];
                    u3(2.3210366,0.4254677,1.5148387) q[0];
                    u3(-0.44356465,2.4218092,0.46435541) q[1];
                    cu3(-1.4666209,0.80078667,-1.4474468) q[0],q[1];
                    cu3(-0.36842355,-1.275984,2.0840414) q[1],q[0];
                    u3(-2.4798796,-1.4483067,-0.88710642) q[0];
                    u3(-1.8889532,0.29651332,-3.1028855) q[1];
                    cu3(2.8372009,-2.6686833,2.4253955) q[0],q[1];
                    cu3(0.52282119,-1.0200894,1.9413471) q[1],q[0];
                    u3(0.48961964,2.5382919,0.34343794) q[0];
                    u3(-0.9907741,0.84409469,-0.85193533) q[1];
                    cu3(1.322163,2.8048835,1.8160276) q[0],q[1];
                    cu3(-1.3734181,1.8135304,0.56211334) q[1],q[0];
                    barrier q[0],q[1];
                    """
    
    qnn_circuit_medium = """OPENQASM 2.0;
                            include "qelib1.inc";
                            qreg q[2];
                            ry(0.5) q[0];
                            ry(0.5) q[1];
                            rz(0.5) q[0];
                            rz(0.5) q[1];
                            rx(0.5) q[0];
                            rx(0.5) q[1];
                            ry(0.5) q[0];
                            ry(0.5) q[1];
                            rz(0.5) q[0];
                            rz(0.5) q[1];
                            rx(0.5) q[0];
                            rx(0.5) q[1];
                            ry(0.5) q[0];
                            ry(0.5) q[1];
                            rz(0.5) q[0];
                            rz(0.5) q[1];
                            u3(2.4018686,2.6075468,-0.73598874) q[0];
                            u3(2.8859026,-0.68833423,0.63394415) q[1];
                            cu3(-1.5295002,1.8450029,2.7694488) q[0],q[1];
                            cu3(-2.3047609,2.7306604,0.5879783) q[1],q[0];
                            u3(2.3210366,0.4254677,1.5148387) q[0];
                            u3(-0.44356465,2.4218092,0.46435541) q[1];
                            cu3(-1.4666209,0.80078667,-1.4474468) q[0],q[1];
                            cu3(-0.36842355,-1.275984,2.0840414) q[1],q[0];
                            u3(-2.4798796,-1.4483067,-0.88710642) q[0];
                            u3(-1.8889532,0.29651332,-3.1028855) q[1];
                            cu3(2.8372009,-2.6686833,2.4253955) q[0],q[1];
                            cu3(0.52282119,-1.0200894,1.9413471) q[1],q[0];
                            u3(0.48961964,2.5382919,0.34343794) q[0];
                            u3(-0.9907741,0.84409469,-0.85193533) q[1];
                            cu3(1.322163,2.8048835,1.8160276) q[0],q[1];
                            cu3(-1.3734181,1.8135304,0.56211334) q[1],q[0];
                            u3(1.5954108,-1.9148166,-3.1098893) q[0];
                            u3(-1.2137874,-2.4096735,2.5777991) q[1];
                            cu3(0.90487719,1.3012903,0.99356383) q[0],q[1];
                            cu3(-0.054651063,2.4586365,-2.2321444) q[1],q[0];
                            u3(0.19780637,-2.1442633,0.96871638) q[0];
                            u3(-1.0819089,0.96263516,-0.65452409) q[1];
                            cu3(2.6056113,-1.862028,-1.8736396) q[0],q[1];
                            cu3(-1.8737527,2.8256829,1.0469393) q[1],q[0];
                            u3(3.0229998,-2.5926819,-3.1160707) q[0];
                            u3(-2.4578683,-2.1133151,1.2724712) q[1];
                            cu3(1.1249285,2.6104259,-1.6223981) q[0],q[1];
                            cu3(-2.1416609,1.6668605,-1.2698458) q[1],q[0];
                            u3(1.9067074,-0.74550194,1.7971354) q[0];
                            u3(-2.440917,-1.585404,0.95779765) q[1];
                            cu3(0.66415638,-0.80097657,1.8726075) q[0],q[1];
                            cu3(2.1356838,-2.2781994,-1.6771964) q[1],q[0];
                            barrier q[0],q[1];
                        """
                    
    qnn_circuit_long = """OPENQASM 2.0;
                        include "qelib1.inc";
                        qreg q[2];
                        ry(0.5) q[0];
                        ry(0.5) q[1];
                        rz(0.5) q[0];
                        rz(0.5) q[1];
                        rx(0.5) q[0];
                        rx(0.5) q[1];
                        ry(0.5) q[0];
                        ry(0.5) q[1];
                        rz(0.5) q[0];
                        rz(0.5) q[1];
                        rx(0.5) q[0];
                        rx(0.5) q[1];
                        ry(0.5) q[0];
                        ry(0.5) q[1];
                        rz(0.5) q[0];
                        rz(0.5) q[1];
                        u3(2.4018686,2.6075468,-0.73598874) q[0];
                        u3(2.8859026,-0.68833423,0.63394415) q[1];
                        cu3(-1.5295002,1.8450029,2.7694488) q[0],q[1];
                        cu3(-2.3047609,2.7306604,0.5879783) q[1],q[0];
                        u3(2.3210366,0.4254677,1.5148387) q[0];
                        u3(-0.44356465,2.4218092,0.46435541) q[1];
                        cu3(-1.4666209,0.80078667,-1.4474468) q[0],q[1];
                        cu3(-0.36842355,-1.275984,2.0840414) q[1],q[0];
                        u3(-2.4798796,-1.4483067,-0.88710642) q[0];
                        u3(-1.8889532,0.29651332,-3.1028855) q[1];
                        cu3(2.8372009,-2.6686833,2.4253955) q[0],q[1];
                        cu3(0.52282119,-1.0200894,1.9413471) q[1],q[0];
                        u3(0.48961964,2.5382919,0.34343794) q[0];
                        u3(-0.9907741,0.84409469,-0.85193533) q[1];
                        cu3(1.322163,2.8048835,1.8160276) q[0],q[1];
                        cu3(-1.3734181,1.8135304,0.56211334) q[1],q[0];
                        u3(1.5954108,-1.9148166,-3.1098893) q[0];
                        u3(-1.2137874,-2.4096735,2.5777991) q[1];
                        cu3(0.90487719,1.3012903,0.99356383) q[0],q[1];
                        cu3(-0.054651063,2.4586365,-2.2321444) q[1],q[0];
                        u3(0.19780637,-2.1442633,0.96871638) q[0];
                        u3(-1.0819089,0.96263516,-0.65452409) q[1];
                        cu3(2.6056113,-1.862028,-1.8736396) q[0],q[1];
                        cu3(-1.8737527,2.8256829,1.0469393) q[1],q[0];
                        u3(3.0229998,-2.5926819,-3.1160707) q[0];
                        u3(-2.4578683,-2.1133151,1.2724712) q[1];
                        cu3(1.1249285,2.6104259,-1.6223981) q[0],q[1];
                        cu3(-2.1416609,1.6668605,-1.2698458) q[1],q[0];
                        u3(1.9067074,-0.74550194,1.7971354) q[0];
                        u3(-2.440917,-1.585404,0.95779765) q[1];
                        cu3(0.66415638,-0.80097657,1.8726075) q[0],q[1];
                        cu3(2.1356838,-2.2781994,-1.6771964) q[1],q[0];
                        u3(2.876637,-1.0600755,-1.1137462) q[0];
                        u3(-3.0397882,-1.7990966,0.7847814) q[1];
                        cu3(-0.4146688,-2.2804382,0.073691376) q[0],q[1];
                        cu3(-2.1459639,-2.6653168,-1.7299577) q[1],q[0];
                        u3(-2.7495599,-2.0003717,3.1403639) q[0];
                        u3(0.59336823,0.96811229,-2.9301143) q[1];
                        cu3(-2.0633159,-1.0456975,0.49125436) q[0],q[1];
                        cu3(-2.7643545,-1.3536276,-1.8807728) q[1],q[0];
                        u3(0.0087061655,-1.1689968,-0.21769907) q[0];
                        u3(-2.1288366,-2.156374,-1.8328109) q[1];
                        cu3(-1.0753591,-2.4795992,2.6341307) q[0],q[1];
                        cu3(-0.62349319,2.703016,0.97886401) q[1],q[0];
                        u3(-2.6602912,2.1740928,-0.86439294) q[0];
                        u3(-1.2042544,-2.6077435,-3.1232479) q[1];
                        cu3(0.89884311,-0.68626165,1.2230947) q[0],q[1];
                        cu3(-2.5781903,2.3324101,-2.306098) q[1],q[0];
                        barrier q[0],q[1];
                    """
    
    if (qnn_type == "long"):
        qnn_circuit = qnn_circuit_long
    elif (qnn_type == "medium"):
        qnn_circuit = qnn_circuit_medium
    else:
        qnn_circuit = qnn_circuit_short
    
    if is_mal:
        victim_circ = QuantumCircuit.from_qasm_str(qnn_circuit)
        malicious_circ = malicious_circuit_gen(mal_type, copies)
        circuit = QuantumCircuit(malicious_circ.num_qubits + victim_circ.num_qubits)
        circuit.append(victim_circ, list(range(victim_circ.num_qubits)))
        circuit.append(malicious_circ, list(range(victim_circ.num_qubits, victim_circ.num_qubits + malicious_circ.num_qubits)))
        circuit = circuit.decompose()
    else:
        circuit = QuantumCircuit.from_qasm_str(qnn_circuit)

    return circuit


def qnn_pattern_matching(qnn_type, mal_type = None, copies = None, is_mal = False):
    qc = qnn_circ(qnn_type, mal_type, copies, is_mal)
    pt = malicious_circuit_gen(mal_type, 1)
    
    print("Malicious Circuit Type: " + mal_type + ". Pattern Count: " + str(pattern_counter(qc, pt)) + ". Bar graph: " + str(bar_graph(qc, pt)))
