
import asyncio
import json
import aiohttp
from aioconsole import ainput

async def send_message(ws):
    while True:
        message_type = str(await ainput("Enter Message Type bc/pc: "))
        message =  str(await ainput("Enter message: "))
        if message_type == "pc":
            target_client_id = int(await ainput("Enter target client_id: "))
            json_data = {
                "target_client_id": target_client_id,
                "message": message,
                "message_type": message_type
            }
            await ws.send_str(json.dumps(json_data))
        else:
            json_data = {
                "message": message,
                "message_type": message_type
            }
            await ws.send_str(json.dumps(json_data))


async def receive_message(ws):
    async for msg in ws:
        print(f"Received message: {msg.data}")


async def connect_server():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://127.0.0.1:8080/ws') as ws:
            print('Connected to server')
            send_task = asyncio.create_task(send_message(ws))
            receive_task = asyncio.create_task(receive_message(ws))

            await asyncio.gather(send_task, receive_task)


 
asyncio.run(connect_server())
