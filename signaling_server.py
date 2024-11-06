import asyncio
import websockets
import json

connected_clients = set()

async def signaling_server(websocket, path):
    # Register the client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # Broadcast the message to all connected clients except the sender
            for client in connected_clients:
                if client != websocket:
                    try:
                        await client.send(json.dumps(data))
                    except websockets.ConnectionClosed:
                        # Remove client if connection closed unexpectedly
                        connected_clients.remove(client)
    except websockets.ConnectionClosed:
        print("Connection closed with a client.")
    finally:
        # Unregister the client
        connected_clients.remove(websocket)
        print("Client disconnected.")

# Start the WebSocket server
start_server = websockets.serve(signaling_server, "localhost", 8765)

# Run the server until manually stopped
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
