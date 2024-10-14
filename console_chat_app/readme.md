# WebSocket Server and Client in Python using aiohttp and aioconsole

This project demonstrates how to implement a WebSocket server and client in Python using `aiohttp` for WebSocket communication and `aioconsole` for non-blocking console input. The server allows clients to send and receive messages in both **broadcast** and **private** modes.

## Features

- **Broadcast Messaging**: A message sent by one client is broadcasted to all other connected clients.
- **Private Messaging**: A message can be sent to a specific client, ensuring that only the intended recipient receives it.
- **Non-blocking Input**: The client can send messages at any time while continuing to receive messages in parallel, using `aioconsole` for non-blocking user input.

## Requirements

- Python 3.7+
- `aiohttp`: For handling WebSocket communication.
- `aioconsole`: For non-blocking user input.

## Reference
For more information on how to handle WebSocket clients in asyncio, you can refer to this detailed guide: SuperFastPython: Asyncio WebSocket Clients.[https://superfastpython.com/asyncio-websocket-clients/]
