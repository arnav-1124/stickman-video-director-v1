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

async def inspect_editor_and_references():
    tab = get_flow_tab()
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        js = """
        (() => {
            // Find prompt box container and surrounding controls
            const promptBox = document.querySelector('.prompt-box-container') || document.querySelector('flow-prompt-box') || document.querySelector('.ProseMirror').parentElement;
            
            // Check for buttons near editor (attachment, reference, model picker, aspect ratio)
            const controls = Array.from(document.querySelectorAll('button, [role="button"]')).map(el => ({
                text: el.innerText.trim(),
                aria: el.getAttribute('aria-label'),
                title: el.getAttribute('title'),
                cls: el.className
            })).filter(e => (e.aria || e.title || e.text) && (
                (e.aria && (e.aria.includes('reference') || e.aria.includes('attach') || e.aria.includes('image') || e.aria.includes('add') || e.aria.includes('model') || e.aria.includes('ratio'))) ||
                (e.text && (e.text.includes('Reference') || e.text.includes('Nano') || e.text.includes('16:9')))
            ));

            // Check any tiles/cards on the canvas with text/titles
            const tiles = Array.from(document.querySelectorAll('[class*="tile"], [class*="node"], [class*="card"]')).map(el => ({
                text: el.innerText ? el.innerText.substring(0, 100).replace(/\\n/g, ' ') : '',
                cls: el.className
            })).filter(t => t.text.length > 5);

            return {
                controls: controls.slice(0, 20),
                tilesSample: tiles.slice(-5)
            };
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        data = json.loads(resp)
        result = data.get("result", {}).get("result", {}).get("value", {})
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(inspect_editor_and_references())
