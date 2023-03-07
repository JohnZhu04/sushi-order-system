from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

host: str = 'db'
port: int = 3306
db_name: str = 'fastapi'
user = 'fastapi'
password = 'passw0rd'

uri = f'mysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8'
engine = create_engine(uri, echo=True)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)
)

base = declarative_base()
base.query = session.query_property()