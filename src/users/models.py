from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

User = Table(
    'users',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(20), unique=True),
    Column('password', String(87))
)
