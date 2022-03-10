import random
from qiskit import QuantumCircuit, transpile, schedule



def malicious_circuit_gen(copies, mal_type): # copies- decides the depth of the malicious circuit and d is the delay value
    
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
        if (mal_type == 'M0'):
            mal_circuit.cx(0,1)
            mal_circuit.cx(1,0)
            mal_circuit.cx(0,1)

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

    return mal_circuit



def append_random_malicious_circuit(vic_circ, mal_list, mal_duration, vic_qubits, mal_qubits, backend, random_seed = 0, **transpiler_args):
    """Randomly generate the malicious circuits with an approximate duration and append them to the victim circuit.

    Args:
        vic_circ: The victim circuit.
        mal_list: A list containing the malicious patterns.
        mal_duration: The upper bound of the duration of malicious circuit to be appended.
            The total duration of malicious circuit is less or equal to `mal_duration`, and
            adding any malicious pattern will make the total duration larger than 
            `mal_duration`.
        vic_qubits: Qubit indices to append the victim circuit.
        mal_qubits: Qubit indices to append the malicious circuit.
        backend: The backend used to compute the duration and tranpile the circuit.
        random_Seed: Random seed.
        transpiler_args: arguments for tranpile().

    Returns:
        The victim circuit appended with randomly generated malicious circuit.

    Examples:

        .. jupyter-execute::

            circ = QuantumCircuit(2)
            for i in range(10):
                circ.cx(0,1)
            mal_list = [malicious_circuit_gen(1, "M"+str(i)) for i in range(1, 5)]
            append_random_malicious_circuit(circ, mal_list, 10000, list(range(2)), [3, 4], backend)
    
    Note:
        1. Don't input transpiled vic_circ otherwise it would include ancilla qubits
    """
    random.seed(random_seed)

    # store the duration of each malicious type on the backend in unit 'dt'
    mal_durations = []
    for mal_circ in mal_list:
        mal_sche = schedule(transpile(mal_circ, backend, **transpiler_args), backend)
        mal_durations.append(mal_sche.duration)
    
    # sort the list based on durations
    # `mal_ids_sorted` stores the indices of the malicious patterns in `mal_list``
    # `mal_durations_sorted` stores the durations ascendingly
    mal_ids_durations = zip(list(range(len(mal_list))), mal_durations)
    sorted_zipped = sorted(mal_ids_durations, key = lambda x: x[1])
    mal_ids_sorted, mal_durations_sorted = [list(x) for x in zip(*sorted_zipped)]

    # randomly generate circuits
    # the total duration is less or equal to `mal_duration`, and adding any malicious
    # pattern in `mal_list` will make the total duration larger than `mal_duration`
    mal_circ = QuantumCircuit(2)
    mal_duration_init = mal_duration
    while True:
        for i in range(len(mal_list)):
            if mal_durations_sorted[i] > mal_duration:
                break
        if i == 0:
            break
        idx = mal_ids_sorted[random.randint(0, i-1)]
        mal_circ.append(mal_list[idx].to_instruction(), [0, 1])
        mal_circ = mal_circ.decompose()
        mal_duration -= mal_durations_sorted[idx]
    mal_duration = mal_duration_init - mal_duration
    
    # combine the victim circuit and malicious circuit
    circ = QuantumCircuit(backend.configuration().n_qubits)
    circ.append(vic_circ, vic_qubits)
    circ.append(mal_circ, mal_qubits)
    circ = transpile(circ, backend, **transpiler_args)

    return circ, mal_duration

