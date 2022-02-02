# List of files

1. ``benchmarks_results/``: uses pattern matching algorithm to find 10 malicious patterns we defined in the paper in 5 benchmarks: Grover, Deutch-Jozsa, Bernstein-Vazarani, VQE, QNN.
2. ``previous_antivirus/``: contains previously implemented pattern matching algorithm. This is based on instruction list, which can work but may have order issue when there are independent gates.
3. ``circuit_to_dagnc.py``: converts the ``QuantumCircuit`` object to DAGNC. This file is modified based on ``circuit_to_dagdependency.py`` in Qiskit.
4. ``dagnc.py``: defines DAGNC. This file is modified based on ``dagdependency.py`` in Qiskit.
5. ``example.py``: examples of the functionality of this directory.
6. ``pattern_matching.py``: defines functions related to pattern matching, such as match(), pattern_counter() and bar_graph().
7. ``utils.py``: defines some helper functions.

# Usage

Please find ``example.py `` to see how to use.
You can directly with

    python example.py