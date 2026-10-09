import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
branding_dir = root_dir / "assets/branding/stone_age_tales"
branding_dir.mkdir(parents=True, exist_ok=True)

ref_day = root_dir / "ref_01_ink_explainer_savanna_day.jpg"

base_img = Image.open(ref_day).convert("RGB")
banner = base_img.resize((2048, 1152), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(banner)

# 1. Clean bottom-right watermark (sample nearby savanna color)
# The watermark is in bottom right approx X: 1850-2048, Y: 1000-1152
# Let's clone / patch with clean savanna background
savanna_patch = banner.crop((1600, 1000, 1800, 1152))
banner.paste(savanna_patch, (1840, 1000))

# 2. Typography in Open Sky / Upper-Safe Zone
# Safe area: Y is 407 to 745. Let's place it at Y ~ 430 to 580 in the bright open sky!
draw = ImageDraw.Draw(banner)

font_bold = "C:/Windows/Fonts/ARLRDBD.TTF"
if not os.path.exists(font_bold):
    font_bold = "C:/Windows/Fonts/arialbd.ttf"

title_font = ImageFont.truetype(font_bold, 96)
sub_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)

title_text = "STONE AGE TALES"
sub_text = "HOW ANCIENT HUMANS SURVIVED, THOUGHT & EVOLVED"

# Text coordinates: Center-right aligned to character
tx = 740
ty = 430

sx = 745
sy = ty + 120

# Draw Title with bold, punchy black comic outline
for dx in [-5, -4, 0, 4, 5]:
    for dy in [-5, -4, 0, 4, 5]:
        draw.text((tx + dx, ty + dy), title_text, font=title_font, fill=(15, 20, 30))

# Deep soft shadow
draw.text((tx + 7, ty + 7), title_text, font=title_font, fill=(0, 0, 0, 160))

# Main Title Fill: Brilliant Canary Gold (#FFE500)
draw.text((tx, ty), title_text, font=title_font, fill=(255, 229, 0))

# Subtitle: Deep charcoal navy with crisp white outline for 100% legibility
for dx in [-2, 0, 2]:
    for dy in [-2, 0, 2]:
        draw.text((sx + dx, sy + dy), sub_text, font=sub_font, fill=(255, 255, 255))
draw.text((sx, sy), sub_text, font=sub_font, fill=(20, 25, 40))

out_banner = branding_dir / "banner_2048x1152.jpg"
banner.save(out_banner, "JPEG", quality=95)
print(f"[SUCCESS] Clean, light, premium banner saved to: {out_banner}")
