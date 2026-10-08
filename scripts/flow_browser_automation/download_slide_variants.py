import sys
import json
import base64
import os
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

async def download_variants_for_slide(slide_num, output_dir=None):
    tab = find_flow_tab()
    if not tab:
        print("ERROR: Flow project tab not found in Brave!")
        return False
    
    ws_url = tab.get("webSocketDebuggerUrl")
    print(f"Connecting to Flow tab: {ws_url}")
    
    if output_dir is None:
        output_dir = "projects/long/ep02_how_humans_invented_the_first_lie/slides/slide_temp"
    os.makedirs(output_dir, exist_ok=True)
    
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        # JavaScript to extract the 4 most recent generated images on the canvas
        js = """
        (async () => {
            // Find all tiles or images on the canvas
            // In Google Flow, generated tiles have img elements
            const allImgs = Array.from(document.querySelectorAll('img[src*="flow.google.com/asb/"], img[src*="flow-content.google"]'));
            
            // We want the most recent batch of 4 images
            // In Flow, the latest generation appears either at the top-left or top
            // Let's get unique src URLs
            const uniqueImgs = [];
            const seen = new Set();
            for (const img of allImgs) {
                if (!seen.has(img.src) && (img.naturalWidth > 100 || img.width > 100)) {
                    seen.add(img.src);
                    uniqueImgs.push(img);
                }
            }
            
            // Take the first 4 unique images from the canvas (top row)
            const targets = uniqueImgs.slice(0, 4);
            const results = [];
            
            for (let i = 0; i < targets.length; i++) {
                const img = targets[i];
                try {
                    // Try fetch first
                    const res = await fetch(img.src);
                    const blob = await res.blob();
                    const b64 = await new Promise((resolve) => {
                        const reader = new FileReader();
                        reader.onloadend = () => resolve(reader.result);
                        reader.readAsDataURL(blob);
                    });
                    results.push({
                        idx: i,
                        src: img.src,
                        w: img.naturalWidth || img.width,
                        h: img.naturalHeight || img.height,
                        data: b64
                    });
                } catch (e) {
                    // Fallback to canvas drawImage
                    const canvas = document.createElement('canvas');
                    canvas.width = img.naturalWidth || img.width || 1280;
                    canvas.height = img.naturalHeight || img.height || 720;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);
                    results.push({
                        idx: i,
                        src: img.src,
                        w: canvas.width,
                        h: canvas.height,
                        data: canvas.toDataURL('image/jpeg', 0.95),
                        error: e.toString()
                    });
                }
            }
            return results;
        })()
        """
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js,
                "awaitPromise": True,
                "returnByValue": True
            }
        }
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        data = json.loads(resp)
        results = data.get("result", {}).get("result", {}).get("value", [])
        
        print(f"Retrieved {len(results)} variant images from browser!")
        labels = ["A", "B", "C", "D"]
        saved_paths = []
        for i, item in enumerate(results):
            label = labels[i] if i < len(labels) else f"var_{i}"
            b64_data = item.get("data", "")
            if "," in b64_data:
                b64_data = b64_data.split(",", 1)[1]
            img_bytes = base64.b64decode(b64_data)
            
            filename = f"slide_{slide_num:03d}_{label}.jpg"
            dest_path = os.path.join(output_dir, filename)
            with open(dest_path, "wb") as f:
                f.write(img_bytes)
            print(f"Saved Variant {label} ({item.get('w')}x{item.get('h')}) -> {dest_path}")
            saved_paths.append(dest_path)
        
        return saved_paths

if __name__ == "__main__":
    slide = int(sys.argv[1]) if len(sys.argv) > 1 else 106
    asyncio.run(download_variants_for_slide(slide))
