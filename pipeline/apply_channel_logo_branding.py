import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import glob
import cv2
from PIL import Image
import numpy as np

def apply_channel_branding(
    slides_dir="projects/shorts/ep05_how_to_handle_disrespect/slides",
    logo_path="assets/branding/channel_logo.png",
    sparkle_center=(1423, 2635),
    logo_size=(150, 150)
):
    """
    Replaces the Google Gemini watermark in the bottom-right corner
    of all slides with the creator's official channel logo badge.
    """
    slides = sorted(glob.glob(os.path.join(slides_dir, "*.jpg")))
    if not slides:
        print(f"[Error] No slides found in {slides_dir}")
        return

    if not os.path.exists(logo_path):
        print(f"[Error] Logo not found at {logo_path}")
        return

    raw_logo = Image.open(logo_path).convert("RGBA")
    logo = raw_logo.resize(logo_size, Image.Resampling.LANCZOS)
    lw, lh = logo_size

    cx, cy = sparkle_center
    top_left = (cx - lw // 2, cy - lh // 2)

    print(f"[Branding] Processing {len(slides)} slides in {slides_dir}...")
    for slide_p in slides:
        # Step 1: Inpaint the Gemini watermark sparkle to erase it cleanly
        cv_img = cv2.imread(slide_p)
        mask = np.zeros(cv_img.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (cx, cy), 28, 255, -1)
        inpainted = cv2.inpaint(cv_img, mask, inpaintRadius=4, flags=cv2.INPAINT_TELEA)

        # Step 2: Convert to PIL and composite official channel logo badge
        pil_img = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
        pil_img.paste(logo, top_left, mask=logo)

        # Step 3: Overwrite slide with high quality JPEG
        pil_img.save(slide_p, format="JPEG", quality=98, subsampling=0)
        print(f"  ✓ {os.path.basename(slide_p)}: Watermark replaced with channel logo at {top_left}")

    print("[Branding] All slides successfully updated with official channel badge!")

if __name__ == "__main__":
    apply_channel_branding()
