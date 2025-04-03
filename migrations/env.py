import asyncio
import ssl
import certifi  # Provides Mozilla's trusted CA bundle
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context

# Import Base from your db.py to capture all your model metadata.
from app.database.db import Base
from app import models

target_metadata = Base.metadata

# Alembic configuration: load settings from alembic.ini.
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Create an SSL context using certifi's CA bundle.
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Load the database connection URL from alembic.ini (ensure it does not include '?sslmode=require').
DATABASE_URL = config.get_main_option("sqlalchemy.url")

# Create the asynchronous engine with proper SSL handling.
connectable = create_async_engine(
    DATABASE_URL,
    poolclass=pool.NullPool,
    connect_args={"ssl": ssl_context},
)


def do_run_migrations(connection):
    """
    Synchronously run migrations using the given connection.
    This function configures the Alembic context with the target metadata
    and then runs the migrations within a transaction.
    """
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations asynchronously using the async engine.

    This function acquires an asynchronous connection from the engine and then
    calls the synchronous migration runner (do_run_migrations) via run_sync.
    """
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    # Offline mode: generate SQL scripts without a live connection.
    context.configure(url=DATABASE_URL, literal_binds=True, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
else:
    # Online mode: run migrations asynchronously.
    asyncio.run(run_migrations_online())

    # Debug Assist:
    print(f"Running migration against: {config.get_main_option('sqlalchemy.url')}")