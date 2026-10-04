import sys
import json
import re
import urllib.request
import asyncio
import websockets

def find_flow_tab():
    url = "http://127.0.0.1:9222/json"
    req = urllib.request.urlopen(url)
    tabs = json.loads(req.read().decode())
    for t in tabs:
        if "flow.google.com/project/3c9ecff9-f48e-4786-b6dc-95e76ba22dbd" in t.get("url", ""):
            return t
    for t in tabs:
        if "flow.google.com/project" in t.get("url", ""):
            return t
    return None

async def send_hardware_enter():
    tab = find_flow_tab()
    ws_url = tab.get("webSocketDebuggerUrl")
    async with websockets.connect(ws_url) as ws:
        # Step 1: Focus editor
        msg_focus = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": "document.querySelector('.ProseMirror').focus();"}
        }
        await ws.send(json.dumps(msg_focus))
        await ws.recv()
        
        # Step 2: Send raw keyDown for Enter
        msg_kd = {
            "id": 2,
            "method": "Input.dispatchKeyEvent",
            "params": {
                "type": "keyDown",
                "windowsVirtualKeyCode": 13,
                "nativeVirtualKeyCode": 13,
                "macCharCode": 13,
                "unmodifiedText": "\r",
                "text": "\r",
                "key": "Enter",
                "code": "Enter"
            }
        }
        await ws.send(json.dumps(msg_kd))
        await ws.recv()
        
        # Step 3: Send raw keyUp for Enter
        msg_ku = {
            "id": 3,
            "method": "Input.dispatchKeyEvent",
            "params": {
                "type": "keyUp",
                "windowsVirtualKeyCode": 13,
                "nativeVirtualKeyCode": 13,
                "macCharCode": 13,
                "unmodifiedText": "\r",
                "text": "\r",
                "key": "Enter",
                "code": "Enter"
            }
        }
        await ws.send(json.dumps(msg_ku))
        await ws.recv()
        print("Hardware ENTER dispatched!")

if __name__ == "__main__":
    asyncio.run(send_hardware_enter())
