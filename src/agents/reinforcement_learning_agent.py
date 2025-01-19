import numpy as np
import random

class ReinforcementLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, action_space=2, epsilon=0.1):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.action_space = action_space
        self.epsilon = epsilon  # Exploration rate

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_space)
        
        # Epsilon-greedy action selection
        if random.random() < self.epsilon:
            return random.randint(0, self.action_space - 1)  # Explore
        return np.argmax(self.q_table[state])  # Exploit

    def update_q_value(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_space)
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        self.q_table[state][action] += self.learning_rate * (td_target - self.q_table[state][action])