from sqlalchemy import (Table, Column, Integer, String,
                        MetaData, ForeignKey, DateTime, func)

from ..users.models import User

metadata = MetaData()

Article = Table(
    'articles',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100)),
    Column('description', String(500)),
    Column('user_id', Integer, ForeignKey(
        User.c.id, ondelete='CASCADE', onupdate='CASCADE')),

    # Probably the best approach is using a SQLAlchemy with his ORM system
    Column('create_date', DateTime, default=func.now()),
    Column('last_modified', DateTime, onupdate=func.utc_timestamp()),
)
