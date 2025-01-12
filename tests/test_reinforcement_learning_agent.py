import unittest
from agents.reinforcement_learning_agent import ReinforcementLearningAgent

class TestReinforcementLearningAgent(unittest.TestCase):

    def test_choose_action(self):
        agent = ReinforcementLearningAgent()
        action = agent.choose_action('state1')
        self.assertIn(action, [0, 1])

    def test_update_q_value(self):
        agent = ReinforcementLearningAgent()
        agent.update_q_value('state1', 0, 1, 'state2')
        self.assertTrue('state1' in agent.q_table)

if __name__ == '__main__':
    unittest.main() 