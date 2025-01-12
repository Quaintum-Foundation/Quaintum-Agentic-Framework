import os

class Config:
    RPC_URL = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")