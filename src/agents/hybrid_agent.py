import numpy as np
from sklearn.neural_network import MLPClassifier
from agents.solana_agent import SolanaAgent

class HybridAgent:
    def __init__(self, circuit_size: int, rpc_url: str, hidden_layer_sizes=(10,), max_iter=1000):
        """
        Initializes a HybridAgent with quantum and Solana capabilities.
        :param circuit_size: Size of the quantum circuit.
        :param rpc_url: The RPC URL for the Solana cluster.
        """
        self.model = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter)
        self.solana_agent = SolanaAgent(rpc_url)

    def make_decision(self, input_data: list) -> float:
        """
        Makes a decision based on classical machine learning.
        :param input_data: Input data for the classical model.
        :return: The decision made by the hybrid agent.
        """
        return self.model.predict([input_data])[0]

    def get_balance(self, public_key: str) -> float:
        """
        Gets the balance of a given Solana account.
        :param public_key: The public key of the Solana account.
        :return: The balance in SOL.
        """
        return self.solana_agent.get_balance(public_key)

    def transfer_sol(self, from_key: str, to_key: str, amount: float):
        """
        Transfers SOL from one account to another.
        :param from_key: The public key of the sender's account.
        :param to_key: The public key of the recipient's account.
        :param amount: The amount of SOL to transfer.
        """
        return self.solana_agent.transfer_sol(from_key, to_key, amount)
