import asyncio
import json
import aiohttp
from aioconsole import ainput

async def send_message(ws):
    """Handles sending messages to the server."""
    while True:
        message_type = await ainput("Enter Message Type (bc for broadcast / pc for private): ")
        message = await ainput("Enter your message: ")

        if message_type == "pc":
            try:
                target_client_id = int(await ainput("Enter target client ID: "))
            except ValueError:
                print("Invalid client ID. Please enter a valid number.")
                continue

            json_data = {
                "target_client_id": target_client_id,
                "message": message,
                "message_type": message_type
            }
        else:
            json_data = {
                "message": message,
                "message_type": message_type
            }

        # Send the message as JSON data
        await ws.send_str(json.dumps(json_data))


async def receive_message(ws):
    """Handles receiving messages from the server."""
    async for msg in ws:
        print(f"Received message: {msg.data}")


async def connect_server():
    """Connects to the WebSocket server and manages send/receive tasks."""
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://127.0.0.1:8080/ws') as ws:
            print('Connected to server')

            # Create tasks for sending and receiving messages concurrently
            send_task = asyncio.create_task(send_message(ws))
            receive_task = asyncio.create_task(receive_message(ws))

            # Wait for both tasks to complete
            await asyncio.gather(send_task, receive_task)


if __name__ == "__main__":
    asyncio.run(connect_server())
