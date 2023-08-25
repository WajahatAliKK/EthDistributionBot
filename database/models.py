from sqlalchemy import Column, BigInteger, String, Float, DateTime, ForeignKey, Boolean, Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(100), nullable=True)
    chat_id = Column(BigInteger, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    joined_channel = Column(Boolean, nullable=False, default=False)
    holds_token = Column(Boolean, nullable=False, default=False)

    wallets = relationship('Wallets', back_populates='user')
  


class Swaps(Base):
    __tablename__ = 'swaps'

    id = Column(BigInteger, primary_key=True)
    coinA_id = Column(BigInteger, ForeignKey('coins.id'), nullable=True)
    coinB_id = Column(BigInteger, ForeignKey('coins.id'), nullable=True)
    eth = Column(BigInteger)
    coinAqty = Column(BigInteger)
    coinBqty = Column(BigInteger)
    timestamp = Column(DateTime)
    transaction_id = Column(BigInteger, ForeignKey('transactions.id'), nullable=True)

    coinA = relationship('Coins', foreign_keys=[coinA_id])
    coinB = relationship('Coins', foreign_keys=[coinB_id])
    transaction = relationship('Transactions', foreign_keys=[transaction_id])


class Claims(Base):
    __tablename__ = 'claims'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    claimed = Column(Boolean, nullable=False, default=False)
    hodlings = Column(BigInteger)
    qty = Column(BigInteger)
    coin_id = Column(BigInteger, ForeignKey('coins.id'), nullable=True)
    transaction_id = Column(BigInteger, ForeignKey('transactions.id'), nullable=True)
    swap_id = Column(BigInteger, ForeignKey('swaps.id'), nullable=True)

    user = relationship('Users', foreign_keys=[user_id])
    coin = relationship('Coins', foreign_keys=[coin_id])
    transaction = relationship('Transactions', foreign_keys=[transaction_id])
    swap = relationship('Swaps', foreign_keys=[swap_id])


class Wallets(Base):
    __tablename__ = 'wallets'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    wallet_address = Column(String(100))
    wallet_encrypted_seed = Column(String(500))
    network_id = Column(BigInteger, ForeignKey('networks.id'), nullable=True)

    user = relationship('Users', foreign_keys=[user_id])
    network = relationship('Networks', foreign_keys=[network_id])


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    wallet_id = Column(BigInteger, ForeignKey('wallets.id'), nullable=True)
    tx_hash = Column(String(500, collation='utf8mb3_general_ci'))
    fee = Column(Float, nullable=True)
    tx_type = Column(String(30))
    time_stamp = Column(DateTime)
    tx_state = Column(String(50))

    user = relationship('Users', foreign_keys=[user_id], backref='transactions')
    wallet = relationship('Wallets', foreign_keys=[wallet_id], backref='transactions')


class Coins(Base):
    __tablename__ = 'coins'

    id = Column(BigInteger, primary_key=True)
    contract_address = Column(String(64), unique=True)
    name = Column(String(200))
    symbol = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    lp_address = Column(String(64), nullable=True, default='0x000000000...')
    network_id = Column(BigInteger, ForeignKey('networks.id'))
    quote_symbol = Column(String(500), default='0x000000000...')
    quote_address = Column(String(500), default='0x000000000...')
    liquidity = Column(Float, default=0.0)
    price = Column(Float, default=0.0)
    price_usd = Column(Float, default=0.0)
    max_buy_amount = Column(Float, default=0.0)
    max_sell_amount = Column(Float, default=0.0)
    max_wallet_amount = Column(Float, default=0.0)
    is_honeypot = Column(Boolean, default=False)
    is_blacklisted = Column(Boolean, default=False)
    is_anti_whale = Column(Boolean, default=False)
    cant_sell_all = Column(Boolean, default=False)
    decimals = Column(Integer, default=18)
    totalsupply = Column(BigInteger, default=18, name='totalSupply')
    buy_tax = Column(Float, default=0.0)
    sell_tax = Column(Float, default=0.0)
    is_dexscreener = Column(Boolean, default=False)
    pair_created_at = Column(DateTime, default=datetime.utcnow)

    network = relationship('Networks')


class Networks(Base):
    __tablename__ = 'networks'

    id = Column(BigInteger, primary_key=True)
    network = Column(String(20))
    dex = Column(String(50))

    wallets = relationship('Wallets', back_populates='network')  # Change 'network' to 'networks'
