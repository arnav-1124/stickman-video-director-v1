import math
from PIL import Image
import numpy as np
from pathlib import Path

ASSETS_DIR = Path("projects/shorts/ep05_how_to_handle_disrespect/master_assets")

files = [
    "Character_Protagonist.jpg",
    "Character_Jester.jpg",
    "Character_Friends.jpg",
    "Character_Senior.jpg",
    "Environment_LivingRoom.jpg"
]

print(f"{'Filename':<28} | {'Resolution':<12} | {'Aspect':<8} | {'Avg BG Color (Hex)':<18} | {'Color Match'}")
print("-" * 85)

for f in files:
    img_path = ASSETS_DIR / f
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    gcd_val = math.gcd(w, h)
    aspect = f"{w//gcd_val}:{h//gcd_val}" if w != h else "1:1"
    if aspect == "9:16" or aspect == "1:1":
        pass
    else:
        # Check standard aspect ratios
        ratio = w / h
        if abs(ratio - 9/16) < 0.02:
            aspect = "9:16"
        elif abs(ratio - 1.0) < 0.02:
            aspect = "1:1"
    
    # Sample 4 corners for background color
    arr = np.array(img)
    corners = np.concatenate([
        arr[0:20, 0:20],
        arr[0:20, -20:],
        arr[-20:, 0:20],
        arr[-20:, -20:]
    ])
    avg_rgb = np.mean(corners, axis=(0, 1)).astype(int)
    hex_color = f"#{avg_rgb[0]:02X}{avg_rgb[1]:02X}{avg_rgb[2]:02X}"
    
    is_match = "PASS (Studio Paper)" if avg_rgb[0] > 240 and avg_rgb[1] > 240 and avg_rgb[2] > 235 else "CHECK"
    print(f"{f:<28} | {f'{w}x{h}':<12} | {aspect:<8} | {hex_color:<18} | {is_match}")
