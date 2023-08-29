from database.models import Coins
from typing import Optional
from bot.db_client import db
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

async def add_coin(coin_data: dict) -> Coins:
    async with db.Session() as session:
        try:
            coin = Coins(
                contract_address=coin_data['contract_address'],
                name=coin_data['name'],
                symbol=coin_data['symbol'],
                created_at=coin_data.get('created_at', datetime.utcnow()),
                lp_address=coin_data['lp_address'],
                network_id=coin_data['network_id'],
                quote_symbol=coin_data['quote_symbol'],
                quote_address=coin_data['quote_address'],
                liquidity=coin_data.get('liquidity', 0.0),
                price=coin_data.get('price', 0.0),
                price_usd=coin_data.get('price_usd', 0.0),
                max_buy_amount=coin_data.get('max_buy_amount', 0.0),
                max_sell_amount=coin_data.get('max_sell_amount', 0.0),
                max_wallet_amount=coin_data.get('max_wallet_amount', 0.0),
                is_honeypot=coin_data.get('is_honeypot', False),
                is_blacklisted=coin_data.get('is_blacklisted', False),
                is_anti_whale=coin_data.get('is_anti_whale', False),
                cant_sell_all=coin_data.get('cant_sell_all', False),
                decimals=coin_data.get('decimals', 18),
                totalsupply=coin_data.get('totalsupply', 18),
                buy_tax=coin_data.get('buy_tax', 0.0),
                sell_tax=coin_data.get('sell_tax', 0.0),
                is_dexscreener=coin_data.get('is_dexscreener', False),
                pair_created_at=coin_data.get('pair_created_at', datetime.utcnow())
            )
            
            session.add(coin)
            await session.commit()

            return coin
        except SQLAlchemyError as e:
            print("An error occurred:", str(e))
            await session.rollback()


async def get_coin_by_contract_address(contract_address: str) -> Coins:
    async with db.AsyncSession() as session:
        coin = await session.execute(select(Coins).filter_by(contract_address=contract_address)).scalar_one_or_none()
    return coin


async def delete_coin_by_contract_address( contract_address: str) -> bool:
    async with db.AsyncSession() as session:
        try:
            coin = await session.execute(select(Coins).where(Coins.contract_address == contract_address))
            coin = coin.scalar_one_or_none()

            if coin:
                session.delete(coin)
                await session.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            print(f"Error deleting coin: {e}")
            await session.rollback()
            return False