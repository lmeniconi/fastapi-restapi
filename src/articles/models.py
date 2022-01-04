from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

Article = Table(
    'articles',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100)),
    Column('description', String(500))
)
