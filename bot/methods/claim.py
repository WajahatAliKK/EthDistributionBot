from web3 import Web3
from database.models import Wallets, Users as User
from bot.wallets.wallet_handlers import eth_wm
from sqlalchemy import select
import os

# Replace these values with your actual values
contract_address = os.environ.get("CONTRACT_ADDRESS ")

# Initialize a Web3 instance
w3 = eth_wm.web3

# Load the contract ABI
contract_abi = os.environ.get("CONTRACT_ABI")

# Load the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

async def claim(user_id, db):
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(User).where(User.chat_id == user_id)
        )
        user = result.scalar_one_or_none()
        # Retrieve the user's wallet
        user_wallet = await session.execute(
            select(Wallets).where(
                Wallets.user_id == user.id,
            )
        )

        user_wallet = user_wallet.scalar_one_or_none()
        private_key = eth_wm.decrypt_seed(user_wallet.wallet_encrypted_seed)
        account = w3.eth.account.from_key(private_key)

        # Call the claim function
        transaction_data = contract.functions.claim().build_transaction({
            'chainId': 1,  # Replace with the appropriate chain ID
            'gas': 200000,  # Replace with the appropriate gas value
            'gasPrice': w3.to_wei('5', 'gwei'),  # Replace with the desired gas price
            'nonce': w3.eth.get_transaction_count(account.address),
        })

        # Sign the transaction
        signed_transaction = w3.eth.account.sign_transaction(transaction_data, private_key)

        # Send the transaction
        transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # Wait for the transaction to be mined
        w3.eth.wait_for_transaction_receipt(transaction_hash)

        # Check if the transaction was successful
        receipt = w3.eth.get_transaction_receipt(transaction_hash)
        if receipt['status'] == 1:
            print("Claim successful")
        else:
            print("Claim failed")
        return transaction_hash