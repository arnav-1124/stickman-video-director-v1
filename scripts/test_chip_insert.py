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

async def test_chip_insertion():
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
        await asyncio.sleep(0.6)

        # Step 2: Click char_01_grog_liar.jpg item and click "Add to prompt"
        js2 = """
        (() => {
            const buttons = Array.from(document.querySelectorAll('button.asset-item'));
            const targetBtn = buttons.find(b => b.innerText.includes('char_01_grog_liar'));
            if (!targetBtn) return { error: 'Target asset button not found' };
            targetBtn.click();
            
            // Check for 'Add to prompt' button
            const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().includes('Add to prompt'));
            if (addBtn) {
                addBtn.click();
                return { action: 'clicked target and Add to prompt' };
            }
            return { action: 'clicked target, no Add to prompt button' };
        })()
        """
        msg2 = {"id": 2, "method": "Runtime.evaluate", "params": {"expression": js2, "returnByValue": True}}
        await ws.send(json.dumps(msg2))
        resp2 = await ws.recv()
        print("CLICK RESULT:", json.loads(resp2)['result']['result']['value'])
        await asyncio.sleep(0.6)

        # Step 3: Check editor HTML
        js3 = """
        (() => {
            const editor = document.querySelector('.ProseMirror');
            return {
                text: editor.innerText,
                html: editor.innerHTML
            };
        })()
        """
        msg3 = {"id": 3, "method": "Runtime.evaluate", "params": {"expression": js3, "returnByValue": True}}
        await ws.send(json.dumps(msg3))
        resp3 = await ws.recv()
        print("EDITOR STATE AFTER CHIP:", json.loads(resp3)['result']['result']['value'])

        # Clean editor
        js4 = """
        (() => {
            const editor = document.querySelector('.ProseMirror');
            editor.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
        })()
        """
        msg4 = {"id": 4, "method": "Runtime.evaluate", "params": {"expression": js4, "returnByValue": True}}
        await ws.send(json.dumps(msg4))
        await ws.recv()

if __name__ == "__main__":
    asyncio.run(test_chip_insertion())
