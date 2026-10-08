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

async def test_trigger_autocomplete():
    tab = get_flow_tab()
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        # Focus and dispatch typing of '@'
        js = """
        (() => {
            const editor = document.querySelector('.ProseMirror');
            editor.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            
            // Dispatch input event for '@'
            document.execCommand('insertText', false, '@');
            
            // Check after small delay if any popup/menu/overlay appeared
            return { length: editor.innerText.length };
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        await ws.recv()
        
        await asyncio.sleep(0.5)
        
        # Check for any overlays/menus
        js_check = """
        (() => {
            const overlays = Array.from(document.querySelectorAll('.cdk-overlay-pane, [role="menu"], [role="listbox"], .mention-menu, .autocomplete-panel, .mat-mdc-menu-panel')).map(p => ({
                html: p.outerHTML.substring(0, 300),
                text: p.innerText
            }));
            return overlays;
        })()
        """
        msg2 = {"id": 2, "method": "Runtime.evaluate", "params": {"expression": js_check, "returnByValue": True}}
        await ws.send(json.dumps(msg2))
        resp2 = await ws.recv()
        print("OVERLAYS:", json.loads(resp2)['result']['result']['value'])
        
        # Clean up editor
        js_clean = """
        (() => {
            const editor = document.querySelector('.ProseMirror');
            editor.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
        })()
        """
        msg3 = {"id": 3, "method": "Runtime.evaluate", "params": {"expression": js_clean, "returnByValue": True}}
        await ws.send(json.dumps(msg3))
        await ws.recv()

if __name__ == "__main__":
    asyncio.run(test_trigger_autocomplete())
