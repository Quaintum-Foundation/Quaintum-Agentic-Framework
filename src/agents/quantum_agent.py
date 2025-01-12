from quantum.circuits import QuantumCircuitBuilder
from ml.quantum_ml import QuantumMLModel
from agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class QuantumAgent(BaseAgent):
    def __init__(self, circuit_size: int, backend: str = "qiskit"):
        self.circuit_builder = QuantumCircuitBuilder(circuit_size, backend)
        self.model = QuantumMLModel()

    def make_decision(self, input_data: list) -> float:
        circuit = self.circuit_builder.build(input_data)
        result = self.model.run(circuit)
        logger.info("Quantum decision made: %s", result)
        return result