import argparse
from qiskit import QuantumCircuit
from malicious_circuit_gen import malicious_circuit_gen

import sys
sys.path.append('../')
from pattern_matching import pattern_counter, bar_graph



def bv_algorithm(s, n):
    # We need a circuit with n qubits, plus one auxiliary qubit
    # Also need n classical bits to write the output to
    bv_circuit = QuantumCircuit(n+1, n)

    # put auxiliary in state |->
    bv_circuit.h(n)
    bv_circuit.z(n)

    # Apply Hadamard gates before querying the oracle
    for i in range(n):
        bv_circuit.h(i)

    # Apply barrier 
    bv_circuit.barrier()

    # Apply the inner-product oracle
    s = s[::-1] # reverse s to fit qiskit's qubit ordering
    for q in range(n):
        if s[q] == '0':
            bv_circuit.i(q)
        else:
            bv_circuit.cx(q, n)

    # Apply barrier 
    bv_circuit.barrier()

    #Apply Hadamard gates after querying the oracle
    for i in range(n):
        bv_circuit.h(i)
    

    # Measurement
    for i in range(n):
        bv_circuit.measure(i, i)
    
    return bv_circuit



def bv_mal(copies, mal_type):
    s = '01'
    n = 2
    # We need a circuit with n qubits, plus one auxiliary qubit
    # Also need n classical bits to write the output to
#     bv_circuit = QuantumCircuit(n+1, n)
#     bv_circuit = QuantumCircuit(5, 4)
#     bv_circuit = QuantumCircuit(7, 6)
    
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
    
    bv_circuit = QuantumCircuit(qr, cr)
    
    bv_circuit.barrier()
    # put auxiliary in state |->
    bv_circuit.h(n)
    bv_circuit.z(n)
    
    # Apply Hadamard gates before querying the oracle
    for i in range(n):
        bv_circuit.h(i)

    # Apply barrier 
#     bv_circuit.barrier()

    # Apply the inner-product oracle
    s = s[::-1] # reverse s to fit qiskit's qubit ordering
    for q in range(n):
        if s[q] == '0':
            bv_circuit.i(q)
        else:
            bv_circuit.cx(q, n)

    # Apply barrier 
#     bv_circuit.barrier()

    #Apply Hadamard gates after querying the oracle
    for i in range(n):
        bv_circuit.h(i)
    
#     for i in range(copies):
#         bv_circuit.z(3)
#         bv_circuit.cx(3,4)
#         bv_circuit.cx(4,5)
#         bv_circuit.delay(0, qarg = 3)
#         bv_circuit.cx(4,5)
        
#         bv_circuit.h(3)
#         bv_circuit.delay(0, qarg = 3)
#         bv_circuit.h(3)
#         bv_circuit.delay(0, qarg = 3)
#         bv_circuit.cx(4,3)
#         bv_circuit.delay(0, qarg = 3)
 
#         if i%2==1:
#             bv_circuit.cx(4,3)
#             bv_circuit.cx(5,4)
#             bv_circuit.cx(6,5)
#             bv_circuit.delay(0, qarg = 6)
#         else:
#             bv_circuit.cx(6,5)
#             bv_circuit.cx(5,4)
#             bv_circuit.cx(4,3)
#             bv_circuit.delay(0, qarg = 3)

############ MALICIOUS CIRCUIT #####################
    if (mal_type == 'M12'):
        bv_circuit.barrier()
        bv_circuit.delay(5*10**copies, unit = 'dt')
    
    else:
        for i in range(copies):
            if (mal_type == 'M1'):
                bv_circuit.cx(3,4)

            if (mal_type == 'M2'):
                bv_circuit.cx(3,4)
                bv_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M3'):
                bv_circuit.cx(3,4)
                bv_circuit.delay(0, qarg=3, unit = 'dt')
                bv_circuit.cx(4,3)
                bv_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M4'):
                bv_circuit.cx(3,4)
                bv_circuit.h(3)
                bv_circuit.delay(0, qarg=3, unit = 'dt')
                bv_circuit.h(3)

            if (mal_type == 'M5'):
                bv_circuit.x(3)
                bv_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M6'):
                bv_circuit.y(3)
                bv_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M7'):
                bv_circuit.z(3)
                bv_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M8'):
                bv_circuit.h(3)
                bv_circuit.delay(0, qarg=3, unit = 'dt')

            if (mal_type == 'M9'):
                bv_circuit.cx(3,4)
                bv_circuit.cx(4,5)

            if (mal_type == 'M10'):
                if i%2==1:
                    bv_circuit.cx(4,3)
                    bv_circuit.cx(5,4)
                    bv_circuit.cx(6,5)
                    bv_circuit.delay(0, qarg = 6)
                else:
                    bv_circuit.cx(6,5)
                    bv_circuit.cx(5,4)
                    bv_circuit.cx(4,3)
                    bv_circuit.delay(0, qarg = 3)

            if (mal_type == 'M11'):
                bv_circuit.cx(5,6)
                bv_circuit.delay(0, qarg=4, unit = 'dt')


            
####################################################
    bv_circuit.barrier()
    # Measurement
#     for i in range(n):
#         bv_circuit.measure(i, i)
    bv_circuit.measure(0, 0)
    bv_circuit.measure(1, 1)
    
    if (mal_type == 'M9'):
        bv_circuit.measure(3, 2)
        bv_circuit.measure(4, 3)
        bv_circuit.measure(5, 4) 
    
    elif (mal_type == 'M10'):
        bv_circuit.measure(3, 2)
        bv_circuit.measure(4, 3)
        bv_circuit.measure(5, 4)
        bv_circuit.measure(6, 5)
        
    elif (mal_type == 'M0' or mal_type == 'M12'):
        pass
    
    else:
        bv_circuit.measure(3, 2)
        bv_circuit.measure(4, 3)
#     bv_circuit.measure(5, 4)
#     bv_circuit.measure(6, 5)
    
    
    return bv_circuit    



def bv(s, n, mal_type, copies, is_mal):
    #for our application s = "01", n = 2
    n = int(n)
    if is_mal:
        qc = bv_mal(copies, mal_type)
    else:
        qc = bv_algorithm(s, n)
    pt = malicious_circuit_gen(mal_type, 1)

    print("Malicious Circuit Type: " + mal_type + ". Pattern Count: " + str(pattern_counter(qc, pt)) + ". Bar graph: " + str(bar_graph(qc, pt)))

    # print("--------------------------------------------------------")
    # print("Bernstein-Vazarani Circuit", "\n Search String = ", s, "\n Number of Qubits =", n) 
    # print(qc)
    
    # print("Search Pattern:") 
    # print(pt)
    
    # print("--------------------------------------------------------")
    # print("2. Pattern counter\n")
    # print("The pattern count in the quantum circuit is: " + str(pattern_counter(qc, pt)))    
    
    # print("--------------------------------------------------------")
    # print("3. Pattern bar graph\n")
    # print("The pattern bar graph in the quantum circuit is: " + str(bar_graph(qc, pt)))

    return 



# parser = argparse.ArgumentParser()
# parser.add_argument('-s','--string', type=str, required=True, help='Hidden binary String')
# parser.add_argument('-w','--width', type=int, required=True, help='Width of binary string')
# parser.add_argument('-m','--mal_type', type=str, required=True, help='Malicious Circuit type options M1 - M10')
# parser.add_argument('-k','--copies', type=int, required=True, help='Defines depth of the malicious circuit')

# args = parser.parse_args()
# bv(args.string, args.width, args.mal_type, args.copies)    
