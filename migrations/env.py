from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
import asyncio
import os

# Alembic Config object for reading values from .ini file
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load database URL from Alembic config
DATABASE_URL = config.get_main_option("sqlalchemy.url")

# Ensure that metadata is correctly set for migrations
target_metadata = None  # Update if using models

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and does not create an Engine. Calls to `context.execute()`
    here emit the SQL directly to the output.

    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    This will create an async database engine and execute migrations.
    """
    # Create an async engine with SSL enabled
    connectable = create_async_engine(
        DATABASE_URL,
        connect_args={"ssl": "require"}  # Explicitly require SSL for NeonDB
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn, target_metadata=target_metadata
            )
        )
        await connection.run_sync(context.run_migrations)

# Determine whether to run in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    # Use existing event loop to run async migrations
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_migrations_online())