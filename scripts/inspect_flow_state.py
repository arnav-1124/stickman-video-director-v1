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

async def inspect():
    tab = get_flow_tab()
    if not tab:
        print("No flow tab found!")
        return
    ws_url = tab["webSocketDebuggerUrl"]
    print("Connecting to:", ws_url)
    async with websockets.connect(ws_url) as ws:
        js = """
        (() => {
            const editor = document.querySelector('.ProseMirror');
            const editorHtml = editor ? editor.innerHTML : '';
            const editorText = editor ? editor.innerText : '';
            
            // Check images or assets on canvas/sidebar
            const images = Array.from(document.querySelectorAll('img')).map(img => ({
                src: img.src ? img.src.substring(0, 80) : '',
                alt: img.alt,
                w: img.naturalWidth || img.width,
                h: img.naturalHeight || img.height,
                cls: img.className
            })).filter(i => i.w > 50);

            // Check generation buttons
            const genBtns = Array.from(document.querySelectorAll('button')).map(b => ({
                label: b.getAttribute('aria-label') || b.innerText.trim(),
                cls: b.className,
                disabled: b.disabled || b.classList.contains('mat-mdc-button-disabled')
            })).filter(b => b.label && (b.label.toLowerCase().includes('generat') || b.label.toLowerCase().includes('start') || b.label.toLowerCase().includes('run')));

            return {
                url: window.location.href,
                hasEditor: !!editor,
                editorText: editorText,
                editorHtml: editorHtml.substring(0, 300),
                genButtons: genBtns,
                imagesCount: images.length,
                recentImages: images.slice(-8)
            };
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        data = json.loads(resp)
        result = data.get("result", {}).get("result", {}).get("value", {})
        print("FLOW STATE:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(inspect())
