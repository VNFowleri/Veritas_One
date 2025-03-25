import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text  # Import `text` for SQL execution

# Load database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://neondb_owner:npg_n6q9MyOcXUDi@ep-dawn-heart-a5xge8c0-pooler.us-east-2.aws.neon.tech/neondb"
)

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async def test_connection():
    """Attempts to connect to the database and run a test query."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))  # Fix: Use `text()`
            print(f"✅ DEBUG: Database is connected. Result: {result.scalar()}")
    except Exception as e:
        print(f"❌ DEBUG: Database connection failed: {e}")

# Run the connection test
if __name__ == "__main__":
    asyncio.run(test_connection())