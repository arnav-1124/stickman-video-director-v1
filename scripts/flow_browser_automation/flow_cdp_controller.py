import json
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

async def submit_prompt(prompt_text):
    tab = find_flow_tab()
    if not tab:
        print("ERROR: Flow project tab not found!")
        return False
    
    ws_url = tab.get("webSocketDebuggerUrl")
    async with websockets.connect(ws_url) as ws:
        # Step 1: Insert prompt text
        js_insert = f"""
        (() => {{
            const editor = document.querySelector('.ProseMirror');
            if (!editor) return {{ error: 'ProseMirror editor not found' }};
            editor.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            document.execCommand('insertText', false, {json.dumps(prompt_text)});
            
            const btn = document.querySelector('button.generate-icon-button, button[aria-label*="Start generation" i]');
            return {{
                inserted: editor.innerText.length > 0,
                btn_disabled: btn ? (btn.disabled || btn.classList.contains('mat-mdc-button-disabled')) : true
            }};
        }})()
        """
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": js_insert, "returnByValue": True}
        }
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        data = json.loads(resp)
        res = data.get("result", {}).get("result", {}).get("value", {})
        print("INSERT RESULT:", res)
        
        if res.get("btn_disabled"):
            print("Generate button is disabled! Waiting 500ms...")
            await asyncio.sleep(0.5)
        
        # Step 2: Click Generate button
        js_click = """
        (() => {
            const btn = document.querySelector('button.generate-icon-button, button[aria-label*="Start generation" i]');
            if (!btn) return { error: 'Generate button not found' };
            btn.click();
            return { clicked: true };
        })()
        """
        msg2 = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": js_click, "returnByValue": True}
        }
        await ws.send(json.dumps(msg2))
        resp2 = await ws.recv()
        data2 = json.loads(resp2)
        res2 = data2.get("result", {}).get("result", {}).get("value", {})
        print("CLICK RESULT:", res2)
        return True

if __name__ == "__main__":
    # Test with a harmless check
    tab = find_flow_tab()
    print("Flow tab ready:", tab.get("title") if tab else "None")
