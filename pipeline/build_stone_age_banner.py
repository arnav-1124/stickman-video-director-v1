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
avatar_file = brain_dir / "stone_age_avatar_v2_1791515966152.jpg"
landscape_banner = brain_dir / "stone_age_banner_1791515905512.jpg"

# 1. Export Master Profile Picture (800x800)
pfp = Image.open(avatar_file).convert("RGB")
pfp = pfp.resize((800, 800), Image.Resampling.LANCZOS)
pfp_path_png = branding_dir / "profile_picture_800x800.png"
pfp_path_jpg = branding_dir / "profile_picture_800x800.jpg"
pfp.save(pfp_path_png, "PNG", quality=95)
pfp.save(pfp_path_jpg, "JPEG", quality=95)
print(f"[PFP] Successfully saved Profile Picture to: {pfp_path_png}")

# 2. Build 2048x1152 Banner with Character & Typography
banner = Image.open(landscape_banner).convert("RGB")
banner = banner.resize((2048, 1152), Image.Resampling.LANCZOS)

# Crop the character from avatar (transparent circular cutout)
char_img = Image.open(avatar_file).convert("RGBA")
# Resize character for banner left flank (height ~480px)
char_scale = 480
char_resized = char_img.resize((char_scale, char_scale), Image.Resampling.LANCZOS)

# Create circular mask with soft edge
mask = Image.new("L", (char_scale, char_scale), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse((10, 10, char_scale - 10, char_scale - 10), fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(3))

# Composite character on the left side of safe band (X ~ 180, Y ~ 430)
banner_rgba = banner.convert("RGBA")
banner_rgba.paste(char_resized, (180, 410), mask)

# Typography in the Safe Area (X ~ 720 to 1900, Y ~ 480 to 720)
font_bold = "C:/Windows/Fonts/ARLRDBD.TTF"
if not os.path.exists(font_bold):
    font_bold = "C:/Windows/Fonts/arialbd.ttf"

title_font = ImageFont.truetype(font_bold, 86)
sub_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)

title_text = "STONE AGE TALES"
sub_text = "HOW ANCIENT HUMANS SURVIVED, THOUGHT & EVOLVED"

draw = ImageDraw.Draw(banner_rgba)

# Text positioning to the right of character
tx = 690
ty = 480

sx = 695
sy = ty + 105

# Glow box behind text
glow = Image.new("RGBA", (2048, 1152), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow)
t_box = draw.textbbox((tx, ty), title_text, font=title_font)
s_box = draw.textbbox((sx, sy), sub_text, font=sub_font)
max_right = max(t_box[2], s_box[2])
g_draw.rectangle([tx - 30, ty - 20, max_right + 30, sy + 45], fill=(5, 10, 20, 190))
glow = glow.filter(ImageFilter.GaussianBlur(15))
banner_rgba = Image.alpha_composite(banner_rgba, glow)

draw = ImageDraw.Draw(banner_rgba)

# Draw Title (Drop Shadow + Outline + Canary Yellow)
# Shadow
draw.text((tx + 6, ty + 6), title_text, font=title_font, fill=(0, 0, 0, 230))
# Outline
for dx in [-4, 0, 4]:
    for dy in [-4, 0, 4]:
        draw.text((tx + dx, ty + dy), title_text, font=title_font, fill=(5, 5, 10, 255))
# Main Text Canary Yellow
draw.text((tx, ty), title_text, font=title_font, fill=(255, 229, 0, 255))

# Draw Subtitle (Crisp White + Subtitle Shadow)
draw.text((sx + 3, sy + 3), sub_text, font=sub_font, fill=(0, 0, 0, 220))
draw.text((sx, sy), sub_text, font=sub_font, fill=(240, 245, 255, 255))

final_banner = banner_rgba.convert("RGB")
out_banner_jpg = branding_dir / "banner_2048x1152.jpg"
final_banner.save(out_banner_jpg, "JPEG", quality=95)
print(f"[BANNER] Successfully saved Banner to: {out_banner_jpg}")
print("=================================================================")
print("  BRANDING ASSETS COMPLETED AT YOUTUBE SPECIFICATIONS!")
print("=================================================================")
