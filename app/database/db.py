from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
import os
import ssl
import certifi  # Ensure you've installed certifi: pip install certifi
from datetime import datetime

# Load database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://neondb_owner:npg_n6q9MyOcXUDi@ep-dawn-heart-a5xge8c0-pooler.us-east-2.aws.neon.tech/neondb"
)

# Create an SSL context using certifi's CA bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Create async engine with SSL enabled via connect_args
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"ssl": ssl_context}
)

# Create AsyncSession
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base class for ORM models
Base = declarative_base()

# 🔥 Import models so Alembic can pick them up
from app.models.fax_file import FaxFile

# ✅ Provide get_db dependency for FastAPI
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()