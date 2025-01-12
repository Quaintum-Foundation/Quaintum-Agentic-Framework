import unittest
from agents.quantum_agent import QuantumAgent
from agents.classical_agent import ClassicalAgent
from agents.hybrid_agent import HybridAgent

class TestAgents(unittest.TestCase):

    def test_quantum_agent(self):
        agent = QuantumAgent(circuit_size=3)
        decision = agent.make_decision([0.5, 1.0, 0.25])
        self.assertIsInstance(decision, float)

    def test_classical_agent(self):
        agent = ClassicalAgent()
        decision = agent.make_decision([0.5, 1.0, 0.25])
        self.assertIsInstance(decision, float)

    def test_hybrid_agent(self):
        agent = HybridAgent(circuit_size=3)
        decision = agent.make_decision([0.5, 1.0, 0.25])
        self.assertIsInstance(decision, float)

if __name__ == '__main__':
    unittest.main()
