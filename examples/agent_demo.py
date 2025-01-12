from agents.quantum_agent import QuantumAgent
from agents.classical_agent import ClassicalAgent
from agents.hybrid_agent import HybridAgent

# Create instances of each agent
quantum_agent = QuantumAgent(circuit_size=3)
classical_agent = ClassicalAgent()
hybrid_agent = HybridAgent(circuit_size=3)

# Define some example input data
input_data = [0.5, 1.0, 0.25]

# Make decisions using each agent
quantum_decision = quantum_agent.make_decision(input_data)
print(f"Quantum Agent Decision: {quantum_decision}")

classical_decision = classical_agent.make_decision(input_data)
print(f"Classical Agent Decision: {classical_decision}")

hybrid_decision = hybrid_agent.make_decision(input_data)
print(f"Hybrid Agent Decision: {hybrid_decision}")
