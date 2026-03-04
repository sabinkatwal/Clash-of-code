"""
Initialize the database by creating all tables.
Run this script once to set up the database schema.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.base import Base
from app.database.models.user import User
from app.database.models.match import Match
from app.database.models.submission import Submission
from app.database.models.rating import Rating

# Load environment variables (prefer backend/app/.env when present)
env_path = os.path.join(os.path.dirname(__file__), "app", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

# Determine a default database URL relative to project root (sibling to backend folder)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
default_db_path = os.path.join(project_root, "clash.db")
default_db_url = f"sqlite:///{default_db_path}"

# Get database URL from env or use default
raw_db_url = os.getenv("DATABASE_URL", default_db_url)

# Normalize asyncpg URL to a sync-compatible URL for this script
if isinstance(raw_db_url, str) and raw_db_url.startswith("postgresql+asyncpg://"):
    DATABASE_URL = raw_db_url.replace("+asyncpg", "")
else:
    DATABASE_URL = raw_db_url

print(f"Using database: {DATABASE_URL}")

try:
    # Create engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Create all tables (this will add missing columns where possible)
    Base.metadata.create_all(bind=engine)

    print("\n✓ Database tables created/updated successfully!")
    print("✓ Ready to use admin_gui.py")

except Exception as e:
    print(f"\n✗ Error creating tables: {e}")
    sys.exit(1)
