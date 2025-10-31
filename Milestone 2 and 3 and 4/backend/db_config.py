# db_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Update DATABASE_URL with your MySQL credentials and DB name
DATABASE_URL = "mysql+pymysql://root:meka@localhost/mydb"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()