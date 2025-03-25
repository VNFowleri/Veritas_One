import asyncio
from app.routers.ifax import init_db

asyncio.run(init_db())