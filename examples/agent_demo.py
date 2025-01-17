from agents.quantum_agent import QuantumAgent
from agents.classical_agent import ClassicalAgent
from agents.hybrid_agent import HybridAgent
from agents.reinforcement_learning_agent import ReinforcementLearningAgent
from agents.solana_agent import SolanaAgent

# Create instances of each agent
quantum_agent = QuantumAgent(circuit_size=3)
classical_agent = ClassicalAgent()
hybrid_agent = HybridAgent(circuit_size=3, rpc_url="https://api.mainnet-beta.solana.com")
rl_agent = ReinforcementLearningAgent()
solana_agent = SolanaAgent(rpc_url="https://api.mainnet-beta.solana.com")

# Define some example input data
input_data = [0.5, 1.0, 0.25]

# Make decisions using each agent
quantum_decision = quantum_agent.make_decision(input_data)
print(f"Quantum Agent Decision: {quantum_decision}")

classical_decision = classical_agent.make_decision(input_data)
print(f"Classical Agent Decision: {classical_decision}")

hybrid_decision = hybrid_agent.make_decision(input_data)
print(f"Hybrid Agent Decision: {hybrid_decision}")

# Reinforcement Learning Agent Example
state = 'state1'
action = rl_agent.choose_action(state)
print(f"Chosen action for {state}: {action}")

# Update Q-value based on the action taken
reward = 1  # Example reward
next_state = 'state2'
rl_agent.update_q_value(state, action, reward, next_state)
print(f"Updated Q-value for {state}: {rl_agent.q_table[state]}")

# Solana Agent Example: Check balance of a Solana account
public_key = "YourPublicKeyHere"  # Replace with an actual public key
balance = solana_agent.get_balance(public_key)
print(f"Balance of {public_key}: {balance} SOL")

# Example of transferring SOL using the Hybrid Agent
from_key = "YourFromPublicKeyHere"  # Replace with an actual public key
to_key = "YourToPublicKeyHere"      # Replace with an actual public key
amount = 0.01
transfer_response = hybrid_agent.transfer_sol(from_key, to_key, amount)
print(f"Transfer response: {transfer_response}")
