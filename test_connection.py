import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import text

# Your database URL from the logs
DATABASE_URL = "postgresql+asyncpg://clash_user:sabindon@localhost:5432/clash_of_code"

# 1. Create the asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# 2. Create a session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def test():
    try:
        async with AsyncSessionLocal() as session:
            # 3. Use text() for raw SQL queries
            result = await session.execute(text("SELECT 1"))
            
            # FIX: result.fetchall() returns a list, it is NOT a coroutine.
            # Do NOT use 'await' here.
            data = result.fetchall()
            
            print("\n--- Connection Successful! ---")
            print(f"Result from database: {data}")
            print("------------------------------\n")
            
    except Exception as e:
        print(f"\n--- Connection Failed! ---")
        print(f"Error: {e}")
        print("--------------------------\n")
    finally:
        # Close the engine connections cleanly
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test())