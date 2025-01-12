from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer

class SolanaAgent:
    def __init__(self, rpc_url: str):
        """
        Initializes a SolanaAgent with a given RPC URL.
        :param rpc_url: The RPC URL for the Solana cluster.
        """
        self.client = Client(rpc_url)

    def get_balance(self, public_key: str) -> float:
        """
        Gets the balance of a given Solana account.
        :param public_key: The public key of the Solana account.
        :return: The balance in SOL.
        """
        balance = self.client.get_balance(PublicKey(public_key))
        return balance['result']['value'] / 1_000_000_000  # Convert lamports to SOL

    def transfer_sol(self, from_key: str, to_key: str, amount: float):
        """
        Transfers SOL from one account to another.
        :param from_key: The public key of the sender's account.
        :param to_key: The public key of the recipient's account.
        :param amount: The amount of SOL to transfer.
        """
        transaction = Transaction()
        transaction.add(transfer(TransferParams(from_pubkey=PublicKey(from_key), to_pubkey=PublicKey(to_key), lamports=int(amount * 1_000_000_000))))
        response = self.client.send_transaction(transaction, from_key)
        return response