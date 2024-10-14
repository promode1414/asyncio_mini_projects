import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("http://127.0.0.1:8080/ws") as ws:
            print("Connected to server!!")
            async for msg in ws:
                print(f"{msg.data}", end="")
    print("Disconnected")


asyncio.run(main())
