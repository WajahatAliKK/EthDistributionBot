import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from web3 import Web3
from database.models import Wallets, Users as User
from dotenv import load_dotenv 
from bot.wallets.wallet_handlers import eth_wm
from sqlalchemy import select
import os

load_dotenv()
PROVIDER = os.getenv('PROVIDER')

async def withdraw_eth(user_id, target_wallet_address, db):
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
        if user_wallet:
            private_key = eth_wm.decrypt_seed(user_wallet.wallet_encrypted_seed)
            # Perform the Ethereum transfer using Web3
            # Initialize a Web3 instance
            w3 = eth_wm.web3
            # Unlock the sender's account using the private key
            sender_account = w3.eth.account.from_key(private_key)
            balance = w3.eth.get_balance(sender_account.address)
            
            # Calculate the gas price and estimate the gas limit
            gas_price = w3.eth.gas_price
            gas_limit = w3.eth.estimate_gas({
                'to': target_wallet_address,
                'value': balance
            })
            amount = balance - (gas_limit * 1.5)
            # Build the transaction
            transaction = {
                'to': target_wallet_address,
                'value': w3.to_wei(amount, 'ether'),
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': w3.eth.get_transaction(sender_account.address),
            }
            
            # Sign the transaction
            signed_tx = sender_account.sign_transaction(transaction)
            
            # Send the transaction
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Update the wallet's transaction state
            user_wallet.wallet_balance -= amount
            user_wallet.tx_state = 'pending'
            print(tx_hash)
            # Commit the changes to the database
            await session.commit()
            await session.refresh(user_wallet)
            
            return tx_hash
        return None
