from os import environ

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from databases import Database

from .settings import DB_USER, DB_PASSWORD, DB_PORT, DB_NAME


DATABASE_CONNECTION_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@mariadb:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_CONNECTION_URI)
database = Database(DATABASE_CONNECTION_URI)

metadata = MetaData()
