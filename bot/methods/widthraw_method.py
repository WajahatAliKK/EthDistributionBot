import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from web3 import Web3
from database.models import Wallets

async def withdraw_eth(user_id, amount, wallet_address, target_wallet_address, private_key, db):
    async with db() as session:
        # Retrieve the user's wallet
        user_wallet = await session.execute(
            db.query(Wallets).filter(
                Wallets.user_id == user_id,
                Wallets.wallet_address == wallet_address
            ).first()
        )
        if user_wallet:
            user_wallet = user_wallet.scalar()
            
            # Perform the Ethereum transfer using Web3
            # Initialize a Web3 instance
            w3 = Web3(Web3.HTTPProvider('your_ethereum_node_url_here'))
            
            # Unlock the sender's account using the private key
            sender_account = w3.eth.account.from_key(private_key)
            
            # Calculate the gas price and estimate the gas limit
            gas_price = w3.eth.gas_price
            gas_limit = w3.eth.estimate_gas({
                'to': target_wallet_address,
                'value': w3.toWei(amount, 'ether')
            })
            
            # Build the transaction
            transaction = {
                'to': target_wallet_address,
                'value': w3.toWei(amount, 'ether'),
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': w3.eth.getTransactionCount(sender_account.address),
            }
            
            # Sign the transaction
            signed_tx = sender_account.signTransaction(transaction)
            
            # Send the transaction
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            
            # Update the wallet's transaction state and balance
            user_wallet.wallet_balance -= amount
            user_wallet.tx_state = 'pending'
            
            # Commit the changes to the database
            await session.commit()
            await session.refresh(user_wallet)
            
            return user_wallet
        return None
