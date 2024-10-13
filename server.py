from aiohttp import web

clients = {}

async def handle_client(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    client_id = len(clients) + 1
    clients[client_id]=ws

    print(f'Connected to server: Client -> {client_id}')
    try:
        async for msg in ws:
            data = msg.json()
            message_type = data["message_type"]
            message = data["message"]
            if message_type == "pc":
                target_client_id = data["target_client_id"]
                if target_client_id not in clients:
                    await ws.send_str(f"Client with Id: {target_client_id} not found")
                else:
                    await clients[target_client_id].send_str(f"Private: Client: {client_id} says: {message}")
            else:
                for cid, client_ws in clients.items():
                    if cid != client_id:
                        await client_ws.send_str(f"Client: {client_id} Says: {message} ")
    finally:
        del clients[client_id]
        await ws.close()
        print(f"DisConnected from server: Client -> {client_id}")

 
if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.get('/ws', handle_client)])
    web.run_app(app, host='127.0.0.1', port=8080)
