from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.rpc.types import TxOpts
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolanaAgent:
    def __init__(self, rpc_url: str):
        self.client = Client(rpc_url)
        logger.info("SolanaAgent initialized with RPC URL: %s", rpc_url)

    def get_balance(self, public_key: str) -> float:
        try:
            balance = self.client.get_balance(PublicKey(public_key))
            logger.info("Balance retrieved for %s: %s", public_key, balance)
            return balance['result']['value'] / 1_000_000_000  # Convert lamports to SOL
        except Exception as e:
            logger.error("Error retrieving balance for %s: %s", public_key, e)
            raise RuntimeError(f"Failed to retrieve balance for {public_key}: {str(e)}")

    def transfer_sol(self, from_key: str, to_key: str, amount: float):
        try:
            transaction = Transaction()
            transaction.add(transfer(TransferParams(from_pubkey=PublicKey(from_key), to_pubkey=PublicKey(to_key), lamports=int(amount * 1_000_000_000))))
            response = self.client.send_transaction(transaction, from_key)
            logger.info("Transferred %s SOL from %s to %s", amount, from_key, to_key)
            return response
        except Exception as e:
            logger.error("Error transferring SOL from %s to %s: %s", from_key, to_key, e)
            raise RuntimeError(f"Failed to transfer SOL from {from_key} to {to_key}: {str(e)}")

    def interact_with_contract(self, program_id: str, data: bytes, accounts: list, from_key: str):
        try:
            transaction = Transaction()
            transaction.add(
                self.client.transaction_instruction(
                    program_id=PublicKey(program_id),
                    data=data,
                    accounts=accounts
                )
            )
            response = self.client.send_transaction(transaction, from_key, opts=TxOpts(skip_preflight=True))
            logger.info("Interacted with contract %s", program_id)
            return response
        except Exception as e:
            logger.error("Error interacting with contract %s: %s", program_id, e)
            return None

class QuantumAgent:
    def __init__(self, circuit_size: int, backend: str = "qiskit"):
        self.circuit_builder = QuantumCircuitBuilder(circuit_size, backend)
        self.model = QuantumMLModel()
        logger.info("QuantumAgent initialized with circuit size: %d and backend: %s", circuit_size, backend)

    def make_decision(self, input_data: list) -> float:
        circuit = self.circuit_builder.build(input_data)
        result = self.model.run(circuit)
        logger.info("Quantum decision made: %s", result)
        return result