import websockets
import requests
import json
import asyncio




access_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM1YjU0NDBkLTk5NDUtNDk2Ny1iNDEzLTFjZWQ2MDZkOTg0MiIsIm5iZiI6MTc2MzQ0MDU3NiwiZXhwIjoxNzY0MDQ1Mzc2LCJpYXQiOjE3NjM0NDA1NzZ9.GXTs_XevfcriEmxIL22FgWmWIunM3PEWRn8xqHHzhJs"

negotiate_url = (
    "https://us01governor.futuredge.com/api/myhub/negotiate"
    "?Machine=WebClient&Key=random&negotiateVersion=1"
)

EXT = "\x1e"

def negotiate_connection():
    headers = {
        "Authorization": access_token,
        "Accept": "*/*",
        "Content-Type": "text/plain;charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "x-signalr-user-agent": "Microsoft SignalR/5.0 (5.0.17; Python)",
        "cache-control": "max-age=0"
    }
    r = requests.post(negotiate_url, headers=headers, data="")
    r.raise_for_status()
    
connection_token = negotiate_connection()

websocket_url = (
    "wss://us01governor.futuredge.com/api/myhub"
    f"?Machine=WebClient&Key=random&id={connection_token}"
    f"&access_token={access_token.replace('Bearer ', '')}"
)

ws= websockets.connect(websocket_url)
async def rerun_bot():
    
    await ws.send(json.dumps({"protocol": "json", "version": 1}) + EXT)
    await asyncio.sleep(0.1)
    return "run"

