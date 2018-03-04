import asyncio
import aiohttp





async def main():
    async with aiohttp.ClientSession as session:
        url="https://discordapp.com/api/v7/users/@me"
        r = await session.request(method, url, **kwargs)
        print(r)

loop=asyncio.get_event_loop()
loop.run_until_complete(main())