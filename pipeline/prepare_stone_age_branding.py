import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
branding_dir = root_dir / "assets/branding/stone_age_tales"
branding_dir.mkdir(parents=True, exist_ok=True)

brain_dir = Path(r"C:\Users\Arnav112\.gemini\antigravity-ide\brain\386cece7-fe2b-4bc2-9f4b-4a39fdc8808f")
raw_pfp = brain_dir / "stone_age_pfp_1791515882364.jpg"
raw_banner = brain_dir / "stone_age_banner_1791515905512.jpg"

# 1. Prepare Profile Picture (800x800 high res PNG & JPG)
pfp_img = Image.open(raw_pfp).convert("RGB")
pfp_img = pfp_img.resize((800, 800), Image.Resampling.LANCZOS)

out_pfp_png = branding_dir / "profile_picture_800x800.png"
out_pfp_jpg = branding_dir / "profile_picture_800x800.jpg"
pfp_img.save(out_pfp_png, "PNG", quality=95)
pfp_img.save(out_pfp_jpg, "JPEG", quality=95)
print(f"[PFP] Saved profile picture to: {out_pfp_png}")

# 2. Prepare 2048x1152 Banner with Typography
banner_img = Image.open(raw_banner).convert("RGB")
banner_img = banner_img.resize((2048, 1152), Image.Resampling.LANCZOS)

# Create an overlay for typography in the safe area (safe area Y is approx 407 to 745)
# Safe center: Y = 576, X = 1024
draw = ImageDraw.Draw(banner_img)

font_path = "C:/Windows/Fonts/ARLRDBD.TTF"
if not os.path.exists(font_path):
    font_path = "C:/Windows/Fonts/arialbd.ttf"

title_font = ImageFont.truetype(font_path, 88)
sub_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 32)

title_text = "STONE AGE TALES"
sub_text = "HOW ANCIENT HUMANS SURVIVED, THOUGHT & EVOLVED"

# Calculate bounding boxes
t_bbox = draw.textbbox((0, 0), title_text, font=title_font)
t_w = t_bbox[2] - t_bbox[0]
t_h = t_bbox[3] - t_bbox[1]
t_x = (2048 - t_w) // 2
t_y = 450  # Inside safe band

s_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
s_w = s_bbox[2] - s_bbox[0]
s_h = s_bbox[3] - s_bbox[1]
s_x = (2048 - s_w) // 2
s_y = t_y + t_h + 25

# Draw subtle dark glow backdrop behind text for 100% legibility
glow_overlay = Image.new("RGBA", (2048, 1152), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow_overlay)
g_draw.rectangle([t_x - 40, t_y - 20, t_x + t_w + 40, s_y + s_h + 25], fill=(10, 15, 25, 170))
glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(15))

banner_rgba = banner_img.convert("RGBA")
banner_rgba = Image.alpha_composite(banner_rgba, glow_overlay)
draw = ImageDraw.Draw(banner_rgba)

# Draw Title with stroke and shadow
# Shadow
draw.text((t_x + 6, t_y + 6), title_text, font=title_font, fill=(0, 0, 0, 220))
# Stroke
for dx in [-4, 0, 4]:
    for dy in [-4, 0, 4]:
        draw.text((t_x + dx, t_y + dy), title_text, font=title_font, fill=(5, 8, 15, 255))
# Main Text Canary Yellow
draw.text((t_x, t_y), title_text, font=title_font, fill=(255, 229, 0, 255))

# Draw Subtitle with crisp white
draw.text((s_x + 3, s_y + 3), sub_text, font=sub_font, fill=(0, 0, 0, 220))
draw.text((s_x, s_y), sub_text, font=sub_font, fill=(240, 245, 255, 255))

final_banner = banner_rgba.convert("RGB")
out_banner = branding_dir / "banner_2048x1152.jpg"
final_banner.save(out_banner, "JPEG", quality=95)
print(f"[BANNER] Saved 2048x1152 banner to: {out_banner}")
print("[SUCCESS] All branding assets ready for YouTube Studio!")
