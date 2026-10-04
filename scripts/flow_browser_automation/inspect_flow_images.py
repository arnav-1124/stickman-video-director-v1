import json
import urllib.request
import asyncio
import websockets
import os
import base64

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

async def inspect_canvas_images():
    tab = find_flow_tab()
    if not tab:
        return []
    ws_url = tab.get("webSocketDebuggerUrl")
    async with websockets.connect(ws_url) as ws:
        js = """
        (() => {
            const imgs = Array.from(document.querySelectorAll('img[src*="flow.google.com/asb/"], img[src*="flow-content.google"]'));
            return imgs.map((img, idx) => ({
                index: idx,
                src: img.src,
                naturalWidth: img.naturalWidth,
                naturalHeight: img.naturalHeight,
                alt: img.alt,
                className: img.className
            }));
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        data = json.loads(resp)
        imgs = data.get("result", {}).get("result", {}).get("value", [])
        return imgs

if __name__ == "__main__":
    imgs = asyncio.run(inspect_canvas_images())
    print(f"Total canvas images found: {len(imgs)}")
    for img in imgs[-6:]:
        print(f"[{img['index']}] {img['naturalWidth']}x{img['naturalHeight']} | {img['src'][:70]}")
