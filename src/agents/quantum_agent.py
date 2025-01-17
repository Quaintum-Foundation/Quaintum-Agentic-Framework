from quantum.circuits import QuantumCircuitBuilder
from ml.quantum_ml import QuantumMLModel
from agents.base_agent import BaseAgent
from quantum.optimization import QuantumOptimizer
from quantum.optimization import QAOA, VQE
import logging
from typing import List

logger = logging.getLogger(__name__)

class QuantumAgent(BaseAgent):
    def __init__(self, circuit_size: int, backend: str = "qiskit"):
        """
        Initializes a QuantumAgent with a given circuit size and backend.

        :param circuit_size: The size of the quantum circuit.
        :param backend: The backend to use for quantum computation (e.g., "qiskit").
        """
        self.circuit_builder = QuantumCircuitBuilder(circuit_size, backend)
        self.model = QuantumMLModel()
        self.optimizer = QuantumOptimizer(backend=backend)

    def make_decision(self, input_data: List[float]) -> float:
        """
        Makes a decision based on quantum computations.

        :param input_data: Input data to process using the quantum model.
        :return: The decision made by the quantum agent.
        """
        circuit = self.circuit_builder.build(input_data)
        result = self.model.run(circuit)
        logger.info("Quantum decision made: %s", result)
        return result
    
    def optimize_qaoa(self, problem: dict):
        qaoa = QAOA()
        return qaoa.solve(problem)

    def optimize_vqe(self, hamiltonian):
        vqe = VQE()
        return vqe.solve(hamiltonian)
    
    def optimize(self, problem: dict):
        """
        Uses quantum optimization (QAOA or VQE) to solve the given problem.
        :param problem: A dictionary defining the optimization problem.
        :return: Optimization results.
        """
        return self.optimizer.optimize_qaoa(problem)
