import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

print(os.getenv('DATABASE_URL'))

engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()