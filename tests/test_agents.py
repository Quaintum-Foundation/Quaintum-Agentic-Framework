import unittest
from agents.quantum_agent import QuantumAgent
from agents.classical_agent import ClassicalAgent
from agents.hybrid_agent import HybridAgent
from agents.reinforcement_learning_agent import ReinforcementLearningAgent

class TestAgents(unittest.TestCase):

    def test_quantum_agent(self):
        agent = QuantumAgent(circuit_size=3)
        decision = agent.make_decision([0.5, 1.0, 0.25])
        self.assertIsInstance(decision, float)
        self.assertGreaterEqual(decision, 0.0)

    def test_classical_agent(self):
        agent = ClassicalAgent()
        decision = agent.make_decision([0.5, 1.0, 0.25])
        self.assertIsInstance(decision, float)
        self.assertGreaterEqual(decision, 0.0)

    def test_hybrid_agent(self):
        agent = HybridAgent(circuit_size=3, rpc_url="https://api.mainnet-beta.solana.com")
        decision = agent.make_decision([0.5, 1.0, 0.25])
        self.assertIsInstance(decision, float)
        self.assertGreaterEqual(decision, 0.0)

    def test_reinforcement_learning_agent(self):
        agent = ReinforcementLearningAgent()
        action = agent.choose_action('state1')
        self.assertIn(action, [0, 1])
        agent.update_q_value('state1', action, 1, 'state2')
        self.assertTrue('state1' in agent.q_table)
if __name__ == '__main__':
    unittest.main()