from sqlalchemy.orm import Session
from database.models import Users as User, Wallets as Wallet    
from database.user_functions import get_user_by_chat_id
from typing import Optional
from aiogram import types
from bot.db_client import db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from typing import List

async def user_has_wallet(user_data: types.User, db, network=None) -> Optional[bool]:
    with db.Session() as session:
        return User.has_wallet(user_data.id, session, network)

async def add_wallet(user_data: types.User, wallet_data, db) -> Optional[Wallet]:
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(User).where(User.chat_id == user_data)
        )
        user = result.scalar_one_or_none()
        
        if user:
            wallet = Wallet(
                user_id = user.id,
                wallet_address=wallet_data['address'],
                wallet_encrypted_seed=wallet_data['encrypted_seed'],
                network_id = 1
            )
            
            
            session.add(wallet)
            await session.commit()

        return wallet
    

async def get_active_wallets(user_data: types.User, db) -> Optional[Wallet]:
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(User).where(User.chat_id == user_data.id)
        )
        user = result.scalar_one_or_none()
        result = await session.execute(
            select(Wallet).where(
                (Wallet.user_id == user.id)
                )
        )
        wallets = result.scalar_one_or_none()
        return wallets
    



async def get_active_network_wallet(user_data: types.User, network, db) -> Optional[Wallet]:
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(Wallet).where(
                (Wallet.user_id == user_data.id) & (Wallet.active == True) & (Wallet.network == network)
                )
        )
        wallets = result.scalars().first()
        return wallets
    

async def get_wallet_by_id(wallet_id: int, db) -> Optional[Wallet]:
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(Wallet).where(
                (Wallet.id == wallet_id)
                )
        )
        wallet = result.scalar_one_or_none()
        return wallet
    



async def change_active_wallet(user_data: types.User, network: str, db) -> Optional[str]:
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(User).where(User.chat_id == user_data.id)
        )
        user = result.scalar_one_or_none()
        result = await session.execute(
            select(Wallet).where(
                (Wallet.user_id == user.id) & (Wallet.network == network.lower())
            )
        )
        wallets = result.scalars().all()
        
        if not wallets or len(wallets) != 2:
            return None

        # Toggle the active status of both wallets
        for wallet in wallets:
            wallet.active = not wallet.active

        # Commit the changes to the database
        await session.commit()

        return network
    
async def view_wallets(user_data: types.User, network: str, db) -> List[Wallet]:
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(User).where(User.chat_id == user_data.id)
        )
        user = result.scalar_one_or_none()
        result = await session.execute(
            select(Wallet).where(
                (Wallet.user_id == user.id) & (Wallet.network == network.lower())
            )
        )
        wallets = result.scalars().all()
        
        return wallets
    


async def delete_wallet_by_name(user_data: types.User, db):
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(User).where(User.chat_id == user_data.id)
        )
        user = result.scalar_one_or_none()
        result = await session.execute(
            select(Wallet).where(
                (Wallet.user_id == user.id)
            )
        )
        
        target_wallet = result.scalar_one_or_none()
        
        await session.delete(target_wallet)
        await session.commit()
        return True
