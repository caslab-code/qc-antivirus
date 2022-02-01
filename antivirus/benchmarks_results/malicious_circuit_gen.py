from qiskit import QuantumCircuit

def malicious_circuit_gen(mal_type, copies): # copies- decides the depth of the malicious circuit and d is the delay value
    
    if (mal_type == 'M5' or mal_type == 'M6' or mal_type == 'M7' or mal_type == 'M8'  ):
        n = 1
    elif (mal_type == 'M9'):
        n = 3
    elif (mal_type == 'M10'):
        n = 4     
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
            mal_circuit.delay(0, qarg=0, unit = 'dt')
            mal_circuit.cx(1,0)
            mal_circuit.delay(0, qarg=0, unit = 'dt')
        
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

    # mal_circuit.barrier()
    # mal_circuit.measure_all()

    return mal_circuit

