#initialization
import matplotlib.pyplot as plt
import numpy as np
import argparse

# importing Qiskit
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy

# import basic plot tools
from qiskit.visualization import plot_histogram

#importing from Search Pattern
import sys
sys.path.append('../antivirus/previous_antivirus')
import search_pattern

sys.path.append('../antivirus')
from pattern_matching import match, pattern_counter, bar_graph
from utils import get_bits_mapping

def malicious_circuit_gen(copies, mal_type): # copies- decides the depth of the malicious circuit and mal_type decides which malicious circuit
    
    if (mal_type == 'M10'):
        n = 4
    
    elif (mal_type == 'M9'):
        n = 3
    
    elif (mal_type == 'M5' or mal_type == 'M6' or mal_type == 'M7' or mal_type == 'M8'  ):
        n = 1     
    
    else:
        n = 2
    mal_circuit = QuantumCircuit(n)
    
############ MALICIOUS CIRCUIT #####################
    for i in range(copies):
        if (mal_type == 'M1'):
            mal_circuit.cx(0,1)
        
        if (mal_type == 'M2'):
            mal_circuit.cx(0,1)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M3'):
            mal_circuit.cx(0,1)
            mal_circuit.cx(1,0)
        
        if (mal_type == 'M4'):
            mal_circuit.cx(0,1)
            mal_circuit.h(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
            mal_circuit.h(0)
        
        if (mal_type == 'M5'):
            mal_circuit.x(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M6'):
            mal_circuit.y(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M7'):
            mal_circuit.z(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M8'):
            mal_circuit.h(0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
        if (mal_type == 'M9'):
            mal_circuit.cx(0,1)
            mal_circuit.cx(1,2)
        
        if (mal_type == 'M10'):
            if i%2==1:
                mal_circuit.cx(1,0)
                mal_circuit.cx(2,1)
                mal_circuit.cx(3,2)
                mal_circuit.delay(0, qarg = 3)
            else:
                mal_circuit.cx(3,2)
                mal_circuit.cx(2,1)
                mal_circuit.cx(1,0)
                mal_circuit.delay(0, qarg = 0)
####################################################

#     mal_circuit.barrier()
    return mal_circuit

 
    
def vqe_types(vqe_type):
    # n = 4
    vqe_circuit_short = """OPENQASM 2.0;
                        include "qelib1.inc";
                        qreg q[2];
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
                        """
      
    vqe_circuit_medium = """OPENQASM 2.0;
                            include "qelib1.inc";
                            qreg q[2];
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
                        """
                    
    vqe_circuit_long =   """OPENQASM 2.0;
                            include "qelib1.inc";
                            qreg q[2];
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
                         """
    
    if (vqe_type == "long"):
        vqe_circuit = vqe_circuit_long
    elif (vqe_type == "medium"):
        vqe_circuit = vqe_circuit_medium
    else:
        vqe_circuit = vqe_circuit_short
    
    
    vqe_circ = QuantumCircuit.from_qasm_str(vqe_circuit)
    
    return vqe_circ


def vqe(vqe_type, mal_type ="M1", copies =1):
    qc = vqe_types(vqe_type)
    pt = malicious_circuit_gen(copies,mal_type)
    print(qc)
    print(pt)
    
    # print("--------------------------------------------------------")
    # print("Grover's 2-Qubit Circuit \n") 
    # print(qc)
    
    # print("Search Pattern:") 
    # print(pt)
    
    # for matching in match(qc, pt):
        # print(matching)

    # 2. Pattern counter:
          # Count how many patterns in the quantum circuit.
    # print("--------------------------------------------------------")
    # print("2. Pattern counter\n")
    # print("The pattern count in the quantum circuit is: " + str(pattern_counter(qc, pt)))

    print("--------------------------------------------------------------------------------------------------")
    print("\n1. Output details of all matching\n")
    for i, matching in enumerate(match(qc, pt)):
        print("Matching " + str(i+1) + ":\n")
        print("(a) Node mapping ({node in the quantum circuit: node in the pattern}):")
        print(matching)
        print("\n(b) Qubit and clbit index mapping:")
        mapping = get_bits_mapping(matching)
        print("Qubit index mapping is ({index in the quantum circuit: index in the pattern}): ")
        print(mapping[0])
        print("Clbit index mapping is ({index in the quantum circuit: index in the pattern}): ")
        print(mapping[1])
        print()
        print()
        print()

    # 2. Pattern counter:
    #       Count how many patterns in the quantum circuit.
    
    # print("--------------------------------------------------------------------------------------------------")
    # print("\n2. Pattern counter\n")
    # print("The appearances of the pattern in the quantum circuit is: " + str(pattern_counter(qc, pt, matcher="networkx")))
    # print()

    # 3. Pattern histogram:
    #       Histogram of the pattern in the circuit.
    #       The return value is a dict, whose keys are how many times the pattern appears in series
    #       and values are the counts for them.
    # print("--------------------------------------------------------------------------------------------------")
    # print("\n3. Pattern histogram\n")
    # print("{Number of the pattern in a continuous appearance: count for this appearance}")
    # print(bar_graph(qc, pt, matcher="networkx"))
    
    return 

    
parser = argparse.ArgumentParser()
parser.add_argument('-v','--vqe_type', type=str, required=True, help='VQE type type options short, medium, long')
parser.add_argument('-m','--mal_type', type=str, required=True, help='Malicious Circuit type options M1 - M10')
parser.add_argument('-k','--copies', type=int, required=True, help='Defines depth of the malicious circuit')


args = parser.parse_args()
vqe(args.vqe_type, args.mal_type, args.copies)

# grover_2qbit()    
