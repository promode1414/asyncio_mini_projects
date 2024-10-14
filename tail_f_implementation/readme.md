# Tail Client-Server Implementation

This folder contains a client-server implementation where the server continuously reads the last few lines of a log file and streams updates to a connected client via WebSocket. It uses Python's `aiohttp` for WebSocket handling and asynchronous file I/O using `aiofiles` to avoid blocking the event loop.

## Features

- **Tail a Log File**: The server reads the last N lines of a specified log file and sends them to the WebSocket client.
- **Real-Time Updates**: The server monitors the log file for changes and sends any new lines to the client in real-time.
- **Asynchronous Implementation**: The implementation is fully asynchronous, ensuring non-blocking I/O operations.
