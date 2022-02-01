import argparse
from qiskit import QuantumCircuit
from malicious_circuit_gen import malicious_circuit_gen
import numpy as np

import sys
sys.path.append('../')
from pattern_matching import pattern_counter, match, bar_graph



def dj_oracle(case, n):
    # We need to make a QuantumCircuit object to return
    # This circuit has n+1 qubits: the size of the input,
    # plus one output qubit
    oracle_qc = QuantumCircuit(n+1)
    
    # First, let's deal with the case in which oracle is balanced
    if case == "balanced":
        # First generate a random number that tells us which CNOTs to
        # wrap in X-gates:
        b = np.random.randint(1,2**n)
        # Next, format 'b' as a binary string of length 'n', padded with zeros:
        b_str = format(b, '0'+str(n)+'b')
        # Next, we place the first X-gates. Each digit in our binary string 
        # corresponds to a qubit, if the digit is 0, we do nothing, if it's 1
        # we apply an X-gate to that qubit:
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
        # Do the controlled-NOT gates for each qubit, using the output qubit 
        # as the target:
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
        # Next, place the final X-gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)

    # Case in which oracle is constant
    if case == "constant":
        # First decide what the fixed output of the oracle will be
        # (either always 0 or always 1)
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)
    
    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle" # To show when we display the circuit
    return oracle_gate


def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n+1, n)
    # Set up the output qubit:
    dj_circuit.x(n)
    dj_circuit.h(n)
    # And set up the input register:
    for qubit in range(n):
        dj_circuit.h(qubit)
    # Let's append the oracle gate to our circuit:
    dj_circuit.append(oracle, range(n+1))
    # Finally, perform the H-gates again and measure:
    for qubit in range(n):
        dj_circuit.h(qubit)
    
    
    for i in range(n):
        dj_circuit.measure(i, i)
    
    return dj_circuit

def dj_mal(n, copies, mal_type):
    oracle = dj_oracle("balanced",2)
#     oracle = dj_oracle("constant",2)
#     dj_circuit = QuantumCircuit(7, 6)
#     dj_circuit = QuantumCircuit(5, 4)
    
    if (mal_type == 'M10' or mal_type == 'M11'):
        qr = n+5
        cr = qr-1
    
    elif (mal_type == 'M9'):
        qr = n+4
        cr = qr - 1
        
    elif (mal_type == 'M12' or mal_type == 'M0'):
        qr = n + 1 
        cr = qr-1
    else:
        qr = n+3 
        cr = qr-1
    
    dj_circuit = QuantumCircuit(qr, cr)
    
    dj_circuit.barrier()
    # Set up the output qubit:
    dj_circuit.x(2)
    dj_circuit.h(2)
    # And set up the input register:
    for qubit in range(2):
        dj_circuit.h(qubit)
    # Let's append the oracle gate to our circuit:
    
#     dj_circuit.append(oracle, range(2+1))
    dj_circuit.append(oracle, [0,1,2])
    # Finally, perform the H-gates again and measure:
    for qubit in range(2):
        dj_circuit.h(qubit)
    
#     for i in range(copies):
# #         dj_circuit.z(3)
#         dj_circuit.cx(3,4)
# #         dj_circuit.h(3)
# #         dj_circuit.delay(0, qarg = 3)
# #         dj_circuit.h(3)
# #         dj_circuit.delay(0, qarg = 3)
#         dj_circuit.cx(4,3)
# #         dj_circuit.delay(0, qarg = 3)

# #         if i%2==1:
# #             dj_circuit.cx(4,3)
# #             dj_circuit.cx(5,4)
# #             dj_circuit.cx(6,5)
# #             dj_circuit.delay(0, qarg = 6)
# #         else:
# #             dj_circuit.cx(6,5)
# #             dj_circuit.cx(5,4)
# #             dj_circuit.cx(4,3)
# #             dj_circuit.delay(0, qarg = 3)

############ MALICIOUS CIRCUIT #####################
    if (mal_type == 'M12'):
        dj_circuit.barrier()
        dj_circuit.delay(5*10**copies, unit = 'dt')
    
    else:
        for i in range(copies):
            if (mal_type == 'M1'):
                dj_circuit.cx(3,4)

            if (mal_type == 'M2'):
                dj_circuit.cx(3,4)
                dj_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M3'):
                dj_circuit.cx(3,4)
                dj_circuit.delay(0, qarg=3, unit = 'dt')
                dj_circuit.cx(4,3)
                dj_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M4'):
                dj_circuit.cx(3,4)
                dj_circuit.h(3)
                dj_circuit.delay(0, qarg=3, unit = 'dt')
                dj_circuit.h(3)

            if (mal_type == 'M5'):
                dj_circuit.x(3)
                dj_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M6'):
                dj_circuit.y(3)
                dj_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M7'):
                dj_circuit.z(3)
                dj_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M8'):
                dj_circuit.h(3)
                dj_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M9'):
                dj_circuit.cx(3,4)
                dj_circuit.cx(4,5)

            if (mal_type == 'M10'):
                if i%2==1:
                    dj_circuit.cx(4,3)
                    dj_circuit.cx(5,4)
                    dj_circuit.cx(6,5)
                    dj_circuit.delay(0, qarg = 6)
                else:
                    dj_circuit.cx(6,5)
                    dj_circuit.cx(5,4)
                    dj_circuit.cx(4,3)
                    dj_circuit.delay(0, qarg = 3)

            if (mal_type == 'M11'):
                dj_circuit.cx(5,6)
                dj_circuit.delay(0, qarg=4, unit = 'dt')


            
####################################################

    dj_circuit.barrier()
    # Measurement
#     for i in range(n):
#         bv_circuit.measure(i, i)
    dj_circuit.measure(0, 0)
    dj_circuit.measure(1, 1)
    
    if (mal_type == 'M9'):
        dj_circuit.measure(3, 2)
        dj_circuit.measure(4, 3)
        dj_circuit.measure(5, 4) 
    
    elif (mal_type == 'M10'):
        dj_circuit.measure(3, 2)
        dj_circuit.measure(4, 3)
        dj_circuit.measure(5, 4)
        dj_circuit.measure(6, 5)
        
    elif (mal_type == 'M0' or mal_type == 'M12'):
        pass
    
    else:
        dj_circuit.measure(3, 2)
        dj_circuit.measure(4, 3)
#     bv_circuit.measure(5, 4)
#     bv_circuit.measure(6, 5)
    
    return dj_circuit



def dj(case, n, mal_type, copies, is_mal):
    #for our application case = "balanced", n = 2
    n = int(n)
    oracle = dj_oracle(case,n)
    if is_mal:
        qc = dj_mal(n, copies, mal_type)
    else:
        qc = dj_algorithm(oracle,n)
    pt = malicious_circuit_gen(mal_type, 1)
    
    # print("--------------------------------------------------------")
    # print("Deutsch-Josza Circuit", "\n Case = ", case, "\n Number of Qubits =", n) 
    # print(qc)
    
    # print("Search Pattern:") 
    # print(pt)
    
    # for matching in match(qc, pt):
    #     print(matching)

    # # 2. Pattern counter:
    # #       Count how many patterns in the quantum circuit.
    # print("--------------------------------------------------------")
    # print("2. Pattern counter\n")
    # print("The pattern count in the quantum circuit is: " + str(pattern_counter(qc, pt)))

    # print("--------------------------------------------------------")
    # print("3. Pattern bar graph\n")
    # print("The pattern bar graph in the quantum circuit is: " + str(bar_graph(qc, pt)))

    print("Malicious Circuit Type: " + mal_type + ". Pattern Count: " + str(pattern_counter(qc, pt)) + ". Bar graph: " + str(bar_graph(qc, pt)))

    return 



# parser = argparse.ArgumentParser()
# parser.add_argument('-c','--case', type=str, required=True, help='Select one from two options: 1. "balanced" 2. "constant" ')
# parser.add_argument('-w','--width', type=int, required=True, help='Width of input string')
# parser.add_argument('-m','--mal_type', type=str, required=True, help='Malicious Circuit type options M1 - M10')
# parser.add_argument('-k','--copies', type=int, required=True, help='Defines depth of the malicious circuit')

# args = parser.parse_args()
# dj(args.case, args.width, args.mal_type, args.copies)
