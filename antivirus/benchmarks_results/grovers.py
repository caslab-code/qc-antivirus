from qiskit import QuantumCircuit
from malicious_circuit_gen import malicious_circuit_gen

import sys
sys.path.append('../')
from pattern_matching import pattern_counter, bar_graph



def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc



def ga_algorithm():
    n = 2
    grover_circuit = QuantumCircuit(n)
    grover_circuit = initialize_s(grover_circuit, [0,1])
    
    grover_circuit.cz(0,1) # Oracle

    # Diffusion operator (U_s)
    grover_circuit.h([0,1])
    grover_circuit.z([0,1])
    grover_circuit.cz(0,1)
    grover_circuit.h([0,1])
    return grover_circuit



def ga_mal(mal_type = None, copies = None): # k- decides the depth of the malicious circuit and d is the delay value
    
    if (mal_type == 'M10' or mal_type == 'M11'):
        n = 6
    
    elif (mal_type == 'M9'):
        n = 5
    elif (mal_type == 'M12'):
        n = 2
    else:
        n = 4     
    
    #grover_circuit = QuantumCircuit(n)
    grover_circuit = QuantumCircuit(n)
    
    
    grover_circuit.barrier()
    grover_circuit.x(2)
    ############## VICTIM's CIRCUIT ######################    
    grover_circuit = initialize_s(grover_circuit, [0,1])
    
    grover_circuit.cz(0,1) # Oracle

    # Diffusion operator (U_s)
    grover_circuit.h([0,1])
    grover_circuit.z([0,1])
    grover_circuit.cz(0,1)
    grover_circuit.h([0,1])

    ############ MALICIOUS CIRCUIT #####################
    if (mal_type == 'M12'):
        grover_circuit.barrier()
        grover_circuit.delay(10**copies, unit = 'dt')
    
    else:
        for i in range(copies):
            if (mal_type == 'M1'):
                grover_circuit.cx(2,3)

            if (mal_type == 'M2'):
                grover_circuit.cx(2,3)
                grover_circuit.delay(0, qarg=2, unit = 'dt')

            if (mal_type == 'M3'):
                grover_circuit.cx(2,3)
                grover_circuit.delay(0, qarg=2, unit = 'dt')
                grover_circuit.cx(3,2)
                grover_circuit.delay(0, qarg=2, unit = 'dt')

            if (mal_type == 'M4'):
                grover_circuit.cx(2,3)
                grover_circuit.h(2)
                grover_circuit.delay(0, qarg=2, unit = 'dt')
                grover_circuit.h(2)

            if (mal_type == 'M5'):
                grover_circuit.x(2)
                grover_circuit.delay(0, qarg=2, unit = 'dt')

            if (mal_type == 'M6'):
                grover_circuit.y(2)
                grover_circuit.delay(0, qarg=2, unit = 'dt')

            if (mal_type == 'M7'):
                grover_circuit.z(2)
                grover_circuit.delay(0, qarg=2, unit = 'dt')

            if (mal_type == 'M8'):
                grover_circuit.h(2)
                grover_circuit.delay(0, qarg=2, unit = 'dt')

            if (mal_type == 'M9'):
                grover_circuit.cx(2,3)
                grover_circuit.cx(3,4)

            if (mal_type == 'M10'):
                if i%2==1:
                    grover_circuit.cx(3,2)
                    grover_circuit.cx(4,3)
                    grover_circuit.cx(5,4)
                    grover_circuit.delay(0, qarg = 5)
                else:
                    grover_circuit.cx(5,4)
                    grover_circuit.cx(4,3)
                    grover_circuit.cx(3,2)
                    grover_circuit.delay(0, qarg = 2)

            if (mal_type == 'M11'):
                grover_circuit.cx(4,5)
                grover_circuit.delay(0, qarg=4, unit = 'dt')


            
####################################################

    grover_circuit.barrier()
    grover_circuit.measure_all()
#     grover_circuit.measure(0,0)
#     grover_circuit.measure(1,1)
    
    return grover_circuit



def ga(mal_type, copies, is_mal):
    pt = malicious_circuit_gen(mal_type, 1)
    
    if is_mal:
        qc = ga_mal(mal_type, copies)
    else:
        qc = ga_algorithm()

    print("Malicious Circuit Type: " + mal_type + ". Pattern Count: " + str(pattern_counter(qc, pt)) + ". Bar graph: " + str(bar_graph(qc, pt)))
    
    return 
