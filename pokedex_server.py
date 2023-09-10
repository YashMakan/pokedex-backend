import asyncio
import io
import json
from pokedex_basic import recognize_pokemon
import websockets

async def websocket_handler(websocket, path):
    try:
        async for message in websocket:
            response = recognize(message)
            await websocket.send(json.dumps(response))
    except Exception as e:
        print(f"WebSocket Error: {str(e)}")


def recognize(message):
    try:
        pokemon = recognize_pokemon(message)
        if pokemon:
            return {"status": True, "message": "Pokemon found!", "data": {"name": pokemon}}
        else:
            return {"status": False, "message": "No pokemon found!", "data": {}}

    except Exception as e:
        return {"status": False, "message": str(e)}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        websockets.serve(websocket_handler, "0.0.0.0", 8765)
    )
    loop.run_forever()
