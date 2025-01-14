from qiskit import Aer, execute
from qiskit.circuit.library import TwoLocal
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms import QAOA, VQE
from qiskit.opflow import I, Z, X, PauliSumOp

class QuantumOptimizer:
    def __init__(self, backend: str = "qasm_simulator"):
        self.backend = Aer.get_backend(backend)

    def optimize_qaoa(self, problem: dict, p: int = 2):
        """
        Solves a combinatorial optimization problem using QAOA.
        :param problem: A dictionary defining the problem Hamiltonian.
        :param p: The depth of the QAOA circuit.
        :return: Optimal parameters and results.
        """
        hamiltonian = PauliSumOp.from_list(problem['hamiltonian'])
        qaoa = QAOA(optimizer=COBYLA(maxiter=200), reps=p)
        result = qaoa.compute_minimum_eigenvalue(operator=hamiltonian)
        return result

    def optimize_vqe(self, hamiltonian, ansatz: str = "TwoLocal"):
        """
        Solves a quantum chemistry or optimization problem using VQE.
        :param hamiltonian: The problem Hamiltonian.
        :param ansatz: Ansatz circuit type, default is "TwoLocal".
        :return: Ground state energy and parameters.
        """
        ansatz_circuit = TwoLocal(rotation_blocks=['ry', 'rz'], entanglement_blocks='cz') if ansatz == "TwoLocal" else None
        vqe = VQE(ansatz=ansatz_circuit, optimizer=COBYLA(maxiter=200), quantum_instance=self.backend)
        result = vqe.compute_minimum_eigenvalue(operator=hamiltonian)
        return result
