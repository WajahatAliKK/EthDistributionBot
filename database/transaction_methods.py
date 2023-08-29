from database.models import Transactions
from typing import Optional
from bot.db_client import db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

async def add_transaction(user_id: int, wallet_id: int, tx_data: dict) -> Optional[Transactions]:
    async with db.Session() as session:
        try:
            transaction = Transactions(
                user_id=user_id,
                wallet_id=wallet_id,
                tx_hash=tx_data['tx_hash'],
                fee=tx_data.get('fee'),
                tx_type=tx_data['tx_type'],
                time_stamp=tx_data['time_stamp'],
                tx_state=tx_data['tx_state']
            )

            session.add(transaction)
            await session.commit()

            return transaction
        except SQLAlchemyError as e:
            print(f"Error adding transaction: {e}")
            await session.rollback()
            return None


async def get_transaction_by_tx_hash(tx_hash: str) -> Optional[Transactions]:
    async with db.Session() as session:
        try:
            transaction = await session.execute(select(Transactions).where(Transactions.tx_hash == tx_hash))
            return transaction.scalar_one_or_none()
        except SQLAlchemyError as e:
            print(f"Error retrieving transaction: {e}")
            return None


async def delete_transaction_by_tx_hash(tx_hash: str) -> bool:
    async with db.Session() as session:
        try:
            transaction = await get_transaction_by_tx_hash(session, tx_hash)
            if transaction:
                session.delete(transaction)
                await session.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            print(f"Error deleting transaction: {e}")
            await session.rollback()
            return False


async def change_transaction_state(tx_hash: str, new_state: str) -> bool:
    async with db.Session() as session:
        try:
            transaction = await get_transaction_by_tx_hash(tx_hash)
            if transaction:
                transaction.tx_state = new_state
                await session.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            print(f"Error changing transaction state: {e}")
            await session.rollback()
            return False