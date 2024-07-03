import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy import insert
from sqlalchemy.dialects import sqlite, postgresql
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("username", String(50), unique=True, nullable=False),  # VARCHAR(50)
    Column("fullname", String),
)


address = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)
metadata.drop_all(engine)
metadata.create_all(engine)


with engine.connect() as connection:
    stmt = insert(user_table).values(username="test", fullname="test")
    postgres_stmt = stmt.compile(bind=engine, dialect=postgresql.dialect())
    sqlite_stmt = stmt.compile(bind=engine, dialect=sqlite.dialect())
    print(postgres_stmt)
    print(sqlite_stmt)
    print(postgres_stmt.params)
    print(sqlite_stmt.params)
    result = connection.execute(statement=postgres_stmt)
    print(result.inserted_primary_key)
    connection.commit()


with engine.begin() as connection:
    stmt = insert(user_table).values(username="test2", fullname="test2")
    result = connection.execute(stmt)
    print(result.inserted_primary_key)
    stmt_no_values = insert(user_table)
    result = connection.execute(
        stmt_no_values,
        parameters=[
            {"username": "test3", "fullname": "test3"},
            {"username": "test4", "fullname": "test4"},
            {"username": "test5", "fullname": "test5"},
        ]
    )


print(user_table.c.keys())
# with engine.connect() as connection:
#     result = connection.execute(text("select 'Hello, world!'"))
#     print(result.scalars().all())
