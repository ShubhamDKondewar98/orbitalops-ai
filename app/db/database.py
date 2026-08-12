
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langgraph.checkpoint.postgres import PostgresSaver
from contextlib import contextmanager
from psycopg_pool import ConnectionPool

engine = create_engine(os.getenv('DATABASE_URL'))

SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    return SessionLocal()

@contextmanager
def get_checkpointer():
    conn_string = os.getenv("DATABASE_URL")
    pool = ConnectionPool(
        conninfo=conn_string,
        max_size=5,
        kwargs={
            "autocommit": True,
            "prepare_threshold": None,
        },
    )
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()
    try:
        yield checkpointer
    finally:
        pool.close()



