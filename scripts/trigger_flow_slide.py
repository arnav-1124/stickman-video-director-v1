import sys
import json
import re
import urllib.request
import asyncio
import websockets

def get_prompt_for_slide(slide_num):
    file_path = "projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_04_the_magnetism_of_the_unoccupied_mind/quick_batch_copypaste.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = rf"--- SLIDE {slide_num:03d} .*? ---\s*\[Voiceover:[^\n]*\]\s*\n(.*?)(?=\n--- SLIDE|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

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

async def trigger_slide(slide_num):
    prompt = get_prompt_for_slide(slide_num)
    if not prompt:
        print(f"ERROR: Could not find prompt for Slide {slide_num}")
        return False
    
    print(f"Submitting Slide {slide_num}...")
    tab = find_flow_tab()
    if not tab:
        print("ERROR: Flow project tab not found in Brave!")
        return False
    
    ws_url = tab.get("webSocketDebuggerUrl")
    async with websockets.connect(ws_url) as ws:
        # Step 1: Insert text into ProseMirror
        js_insert = f"""
        (() => {{
            const editor = document.querySelector('.ProseMirror');
            if (!editor) return {{ error: 'ProseMirror editor not found' }};
            
            editor.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            document.execCommand('insertText', false, {json.dumps(prompt)});
            return {{ text_len: editor.innerText.length }};
        }})()
        """
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": js_insert, "returnByValue": True}
        }
        await ws.send(json.dumps(msg))
        await ws.recv()
        await asyncio.sleep(0.3)
        
        # Step 2: Trigger Enter key or click Generate button
        js_trigger = """
        (() => {
            const btn = document.querySelector('button.generate-icon-button, button[aria-label*="Start generation" i]');
            if (btn && !btn.disabled && !btn.classList.contains('mat-mdc-button-disabled')) {
                btn.click();
                return { action: 'button_clicked' };
            }
            const editor = document.querySelector('.ProseMirror');
            if (editor) {
                const enterEvent = new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true,
                    cancelable: true
                });
                editor.dispatchEvent(enterEvent);
                return { action: 'enter_dispatched' };
            }
            return { error: 'neither button nor editor triggered' };
        })()
        """
        msg2 = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": js_trigger, "returnByValue": True}
        }
        await ws.send(json.dumps(msg2))
        resp2 = await ws.recv()
        data2 = json.loads(resp2)
        print("TRIGGER RESULT:", data2.get("result", {}).get("result", {}).get("value", {}))
        return True

async def inspect_canvas():
    tab = find_flow_tab()
    if not tab:
        return
    ws_url = tab.get("webSocketDebuggerUrl")
    async with websockets.connect(ws_url) as ws:
        js = """
        (() => {
            const tiles = Array.from(document.querySelectorAll('.tile, [class*="tile"], [class*="card"]'));
            const editor = document.querySelector('.ProseMirror');
            const images = Array.from(document.querySelectorAll('img')).map(i => ({
                src: i.src.substring(0, 70),
                alt: i.alt
            }));
            return {
                editor_text: editor ? editor.innerText.substring(0, 80) : '',
                total_tiles: tiles.length,
                total_images: images.length,
                last_3_images: images.slice(-3)
            };
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        data = json.loads(resp)
        print(json.dumps(data.get("result", {}).get("result", {}).get("value", {}), indent=2))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "inspect":
        asyncio.run(inspect_canvas())
    else:
        slide = int(sys.argv[1]) if len(sys.argv) > 1 else 106
        asyncio.run(trigger_slide(slide))
