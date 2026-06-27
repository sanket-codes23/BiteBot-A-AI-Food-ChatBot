from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Create the connection URL safely
connection_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

# Create SQLAlchemy engine
engine = create_engine(connection_url, echo=True)

# Create Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()