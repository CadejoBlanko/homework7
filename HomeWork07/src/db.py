from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

url = 'postgresql://postgres:71797384@localhost/cadejo07dbhw'
Base = declarative_base()
engine = create_engine(url, echo=False, pool_size=5)

DBSession = sessionmaker(bind=engine)
session = DBSession()