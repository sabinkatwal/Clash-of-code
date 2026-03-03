import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context

# ------------------ Add app path ------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ------------------ Import your models ------------------
from app.database.base import Base
from app.database.models import user, match, submission, rating  # import all models

# ------------------ Alembic config ------------------
config = context.config

# Set up logging from .ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for 'autogenerate' migrations
target_metadata = Base.metadata

# ------------------ Offline mode ------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# ------------------ Online mode (SYNC engine) ------------------
def run_migrations_online() -> None:
    """Run migrations in 'online' mode using a synchronous engine."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# ------------------ Run migrations ------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()