import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Claims, Transactions

async def get_transaction_state(transaction_id, db):
    async with db() as session:
        transaction = await session.execute(
            db.query(Transactions).filter(Transactions.id == transaction_id).first()
        )
        if transaction:
            return transaction.scalar().tx_state
        return None

async def add_transaction(user_id, wallet_id, tx_data, db):
    async with db() as session:
        transaction = Transactions(
            user_id=user_id,
            wallet_id=wallet_id,
            tx_hash=tx_data['tx_hash'],
            fee=tx_data['fee'],
            tx_type=tx_data['tx_type'],
            time_stamp=tx_data['time_stamp'],
            tx_state=tx_data['tx_state']
        )
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction

async def change_transaction_state(transaction_id, new_state, db):
    async with db() as session:
        transaction = await session.execute(
            db.query(Transactions).filter(Transactions.id == transaction_id).first()
        )
        if transaction:
            transaction = transaction.scalar()
            transaction.tx_state = new_state
            await session.commit()
            await session.refresh(transaction)
            return transaction
        return None
