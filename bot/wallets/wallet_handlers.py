from bot.wallet_manager import WalletManager
from dotenv import load_dotenv
import os

load_dotenv()


eth_wm = WalletManager(network_url=os.getenv('PROVIDER'), encryption_key=os.getenv('ENCRYPTION_KEY'))