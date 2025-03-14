from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
import os
from datetime import datetime

# Load database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://neondb_owner:npg_n6q9MyOcXUDi@ep-dawn-heart-a5xge8c0-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")

# Create async engine for PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create AsyncSession
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()

class FaxFile(Base):
    __tablename__ = "fax_files"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, nullable=False)  # iFax job ID
    transaction_id = Column(String, unique=True, nullable=False)  # iFax transaction ID
    sender = Column(String, nullable=True)  # Sender's fax number
    receiver = Column(String, nullable=True)  # Receiver's fax number
    received_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    file_path = Column(String, nullable=False)  # Path to the stored PDF
    raw_text = Column(Text, nullable=True)  # OCR extracted text

# Function to initialize the database (used with Alembic)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)