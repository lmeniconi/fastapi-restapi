from sqlalchemy import (Table, Column, Integer, String,
                        MetaData, DateTime, func)


metadata = MetaData()

User = Table(
    'users',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(20), unique=True),
    Column('password', String(87)),

    # Probably the best approach is using a SQLAlchemy with his ORM system
    Column('create_date', DateTime, default=func.now()),
    Column('last_modified', DateTime, onupdate=func.utc_timestamp()),
)
