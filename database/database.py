from sqlalchemy import create_engine
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from contextlib import asynccontextmanager
from database.clinet import Client 
from dotenv import load_dotenv
# from bot.utils.config import DBUSER, DBPASS, DBHOST, DBNAME
load_dotenv()
Base = declarative_base()


# Replace the following values with your MySQL configuration
# user = 'root'
# password = 'testDB77!!'
# host = 'localhost'
# db_name = 'SniperDB' 
def get_db():

    print("DB_USER:", os.getenv('DB_USER'))
    print("DB_PASS:", os.getenv('DB_PASS'))
    print("DB_HOST:", os.getenv('DB_HOST'))
    print("DB:", os.getenv('DB'))

    db = Client(username= os.getenv('DB_USER'),
            password= os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            name=os.getenv('DB'))
    return db

