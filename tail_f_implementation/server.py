import asyncio
import os
import aiofiles
import aiohttp
import aiohttp.web
from aiohttp.web import WebSocketResponse

LOG_FILE_PATH = (
    "/Users/pramodchoudhari/personal_projects/tail_f_implementation/your_log_file.log"
)


async def tail_file(ws: WebSocketResponse, total_lines=20, buffer_size=4098):
    """
    Sends the last 'total_lines' lines from the log file to the WebSocket client,
    then continuously watches for new lines and sends them as well.
    """
    async with aiofiles.open(LOG_FILE_PATH, "rb") as log_file:
        print("Starting tail process")

        lines_found = []
        block_counter = -1
        while len(lines_found) <= total_lines:
            try:
                await log_file.seek(block_counter * buffer_size, os.SEEK_END)
            except IOError:
                await log_file.seek(0)
                lines_found = await log_file.readlines()
                break

            lines_found = await log_file.readlines()
            block_counter -= 1

        last_lines = [line.decode("utf-8") for line in lines_found[-total_lines:]]
        last_lines_str = "".join(last_lines)

        print("Sending initial lines")
        await ws.send_str(last_lines_str)

        print("Watching for new changes")
        last_position = await log_file.tell()

        while True:
            new_line = await log_file.readline()
            new_position = await log_file.tell()

            if new_position != last_position:
                await ws.send_str(new_line.decode("utf-8"))
                last_position = new_position

            await asyncio.sleep(3)

            if ws.closed:
                print("WebSocket is closed, stopping tail process.")
                break


async def handle_client_disconnection(ws):
    """
    Handles WebSocket client disconnection or error.
    """
    try:
        async for msg in ws:
            if msg.type in {aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.ERROR}:
                print("WebSocket Closed or Error Detected.")
                break
    finally:
        await ws.close()
        print("Client Disconnected")


async def websocket_handler(request):
    """
    Handles incoming WebSocket connection requests.
    """
    ws = WebSocketResponse()
    await ws.prepare(request)
    print("New client connected")

    tail_task = asyncio.create_task(tail_file(ws))
    disconnection_task = asyncio.create_task(handle_client_disconnection(ws))

    await asyncio.gather(tail_task, disconnection_task)
    return ws


if __name__ == "__main__":
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.get("/ws", websocket_handler)])
    aiohttp.web.run_app(app, host="127.0.0.1", port=8080)
