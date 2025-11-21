import asyncio
from enka import HSRClient
from pprint import pprint

async def inspect_character(uid: int):
    async with HSRClient() as client:
        data = await client.fetch_showcase(uid)
        for char in data.characters:
            pprint(char.__dict__)  # Shows all fields for this character

asyncio.run(inspect_character(700712292))