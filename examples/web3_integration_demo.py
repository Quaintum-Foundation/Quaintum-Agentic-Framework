from agents.solana_agent import SolanaAgent
from agents.hybrid_agent import HybridAgent

# Initialize the Solana agent
rpc_url = "https://api.mainnet-beta.solana.com"
solana_agent = SolanaAgent(rpc_url)

# Check balance of a Solana account
public_key = "YourPublicKeyHere"
balance = solana_agent.get_balance(public_key)
print(f"Balance of {public_key}: {balance} SOL")

# Initialize the Hybrid agent
hybrid_agent = HybridAgent(circuit_size=3, rpc_url=rpc_url)

# Example of transferring SOL
from_key = "YourFromPublicKeyHere"
to_key = "YourToPublicKeyHere"
amount = 0.01
transfer_response = hybrid_agent.transfer_sol(from_key, to_key, amount)
print(f"Transfer response: {transfer_response}") 