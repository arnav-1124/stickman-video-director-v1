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

async def inspect_asset_selection():
    tab = get_flow_tab()
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        # Step 1: Trigger @ menu
        js = """
        (() => {
            const editor = document.querySelector('.ProseMirror');
            editor.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            document.execCommand('insertText', false, '@');
            return true;
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        await ws.recv()
        await asyncio.sleep(0.5)

        # Step 2: Inspect items in the asset list
        js2 = """
        (() => {
            const items = Array.from(document.querySelectorAll('.asset-list-viewport [role="option"], .asset-list-viewport [class*="item"], .add-menu-popover-container [class*="item"]')).map(el => ({
                text: el.innerText.trim().replace(/\\n/g, ' - '),
                tag: el.tagName,
                cls: el.className
            }));
            return items;
        })()
        """
        msg2 = {"id": 2, "method": "Runtime.evaluate", "params": {"expression": js2, "returnByValue": True}}
        await ws.send(json.dumps(msg2))
        resp2 = await ws.recv()
        print("MENU ITEMS:", json.loads(resp2)['result']['result']['value'])

        # Clean editor
        js3 = """
        (() => {
            const editor = document.querySelector('.ProseMirror');
            editor.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
        })()
        """
        msg3 = {"id": 3, "method": "Runtime.evaluate", "params": {"expression": js3, "returnByValue": True}}
        await ws.send(json.dumps(msg3))
        await ws.recv()

if __name__ == "__main__":
    asyncio.run(inspect_asset_selection())
