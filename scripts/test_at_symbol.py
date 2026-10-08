import asyncio
import json
import urllib.request
import websockets

def get_flow_tab():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    for t in tabs:
        if "flow.google.com" in t.get("url", ""):
            return t
    return None

async def test_at_symbol():
    tab = get_flow_tab()
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        # Check current HTML of editor and see if there are any chips currently in it
        js = """
        (() => {
            const editor = document.querySelector('.ProseMirror');
            return {
                html: editor ? editor.innerHTML : null,
                parentHtml: editor ? editor.parentElement.outerHTML.substring(0, 500) : null
            };
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        print(json.loads(resp)['result']['result']['value'])

if __name__ == "__main__":
    asyncio.run(test_at_symbol())
