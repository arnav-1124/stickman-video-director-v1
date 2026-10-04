import cv2
import numpy as np
from PIL import Image
from pathlib import Path

assets_dir = Path("projects/shorts/ep05_how_to_handle_disrespect/master_assets")

def full_forensic(path):
    img = Image.open(path).convert("RGB")
    arr = np.array(img)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape

    # 1. Background Purity (corners & outer 50px border)
    borders = np.vstack([
        arr[:50, :].reshape(-1,3),
        arr[-50:, :].reshape(-1,3),
        arr[:, :50].reshape(-1,3),
        arr[:, -50:].reshape(-1,3)
    ])
    bg_rgb = np.mean(borders, axis=0)
    bg_hex = f"#{int(round(bg_rgb[0])):02X}{int(round(bg_rgb[1])):02X}{int(round(bg_rgb[2])):02X}"

    # 2. Ink Line Stroke Width
    edges = cv2.Canny(gray, 40, 120)
    edges_dilated = cv2.dilate(edges, np.ones((5,5), np.uint8))
    pure_ink = (gray < 75) & (edges_dilated > 0)
    dist = cv2.distanceTransform(pure_ink.astype(np.uint8), cv2.DIST_L2, 5)
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(dist, kernel)
    ridge = (dist == dilated) & (dist >= 1.5) & (dist <= 15)
    sw = dist[ridge] * 2.0
    med_sw = np.median(sw) if len(sw) > 0 else 0
    mean_sw = np.mean(sw) if len(sw) > 0 else 0

    # 3. Head / Face White Purity
    head_region = arr[int(h*0.08):int(h*0.5), int(w*0.2):int(w*0.8)]
    head_gray = cv2.cvtColor(head_region, cv2.COLOR_RGB2GRAY)
    white_face_px = head_region[(head_gray > 248) & (head_region[:,:,0] > 250)]
    face_rgb = np.mean(white_face_px, axis=0) if len(white_face_px) > 0 else [255, 255, 255]
    face_hex = f"#{int(round(face_rgb[0])):02X}{int(round(face_rgb[1])):02X}{int(round(face_rgb[2])):02X}"

    # 4. Text / Label / Artifact Detection in outer margins
    margin_ink = np.sum(pure_ink[:100, :]) + np.sum(pure_ink[-100:, :]) + np.sum(pure_ink[:, :100]) + np.sum(pure_ink[:, -100:])
    margin_status = "CLEAN (0 text)" if margin_ink < 50 else f"NOTE ({margin_ink}px)"

    # 5. Flatness gradient score
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    interior_mask = (edges_dilated == 0) & (gray < 240)
    flatness_mean = np.mean(grad_mag[interior_mask]) if np.sum(interior_mask) > 100 else 0

    return {
        "name": path.name,
        "dim": f"{w}x{h}",
        "bg_hex": bg_hex,
        "stroke_med": f"{med_sw:.1f}px",
        "stroke_mean": f"{mean_sw:.1f}px",
        "face_hex": face_hex,
        "flatness": f"{flatness_mean:.2f}",
        "margin": margin_status
    }

print("| Asset Name                | Dimensions | Canvas  | Stroke (Med/Mean) | Face Fill | Flatness | Margins / Text |")
print("|---------------------------|------------|---------|-------------------|-----------|----------|----------------|")
for p in sorted(assets_dir.glob("*.jpg")):
    r = full_forensic(p)
    print(f"| {r['name']:<25} | {r['dim']:<10} | {r['bg_hex']:<7} | {r['stroke_med']:<4} / {r['stroke_mean']:<6} | {r['face_hex']:<9} | {r['flatness']:<8} | {r['margin']:<14} |")
