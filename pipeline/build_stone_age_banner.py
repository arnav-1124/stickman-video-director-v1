import os
import sys
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path("f:/Arnav - YT/stickman-video-director")
branding_dir = root_dir / "assets/branding/stone_age_tales"
branding_dir.mkdir(parents=True, exist_ok=True)
cutouts_dir = root_dir / "temp/cutouts"

# 1. Base Canvas: 2048 x 1152 from env_01_savanna_day_empty.jpg
env_path = root_dir / "projects/long/ep02_how_humans_invented_the_first_lie/master_assets/environments/env_01_savanna_day_empty.jpg"
env_raw = Image.open(env_path).convert("RGB")
canvas = env_raw.resize((2048, 1152), Image.Resampling.LANCZOS).convert("RGBA")

# 2. Place Soaring Hawk in sky (Upper right)
hawk = Image.open(cutouts_dir / "cutout_hawk.png").convert("RGBA")
hawk_w = 230
hawk_h = int(hawk.height * (hawk_w / hawk.width))
hawk_resized = hawk.resize((hawk_w, hawk_h), Image.Resampling.LANCZOS)
canvas.paste(hawk_resized, (1580, 340), hawk_resized)

# 3. Place Monkey on the Acacia Branch (Left)
monkey = Image.open(cutouts_dir / "clean_monkey.png").convert("RGBA")
m_w = 175
m_h = int(monkey.height * (m_w / monkey.width))
m_resized = monkey.resize((m_w, m_h), Image.Resampling.LANCZOS)
canvas.paste(m_resized, (365, 430), m_resized)

# 4. Place Stalking Leopard in Savanna Grass (Right Flank)
leopard = Image.open(cutouts_dir / "clean_leopard.png").convert("RGBA")
leo_w = 400
leo_h = int(leopard.height * (leo_w / leopard.width))
leo_resized = leopard.resize((leo_w, leo_h), Image.Resampling.LANCZOS)
canvas.paste(leo_resized, (1450, 610), leo_resized)

# 5. Place Prehistoric People (Grog, Hunter, Elder)
elder = Image.open(cutouts_dir / "cutout_elder.png").convert("RGBA")
elder_h = 240
elder_w = int(elder.width * (elder_h / elder.height))
elder_resized = elder.resize((elder_w, elder_h), Image.Resampling.LANCZOS)
canvas.paste(elder_resized, (620, 535), elder_resized)

hunter = Image.open(cutouts_dir / "cutout_hunter.png").convert("RGBA")
hunter_h = 265
hunter_w = int(hunter.width * (hunter_h / hunter.height))
hunter_resized = hunter.resize((hunter_w, hunter_h), Image.Resampling.LANCZOS)
canvas.paste(hunter_resized, (745, 510), hunter_resized)

grog = Image.open(cutouts_dir / "cutout_grog.png").convert("RGBA")
grog_h = 260
grog_w = int(grog.width * (grog_h / grog.height))
grog_resized = grog.resize((grog_w, grog_h), Image.Resampling.LANCZOS)
canvas.paste(grog_resized, (920, 515), grog_resized)

# 6. Typography: Channel Name + "SUBSCRIBE & LIKE"
draw = ImageDraw.Draw(canvas)
font_bold = "C:/Windows/Fonts/ARLRDBD.TTF"
if not os.path.exists(font_bold):
    font_bold = "C:/Windows/Fonts/arialbd.ttf"

title_font = ImageFont.truetype(font_bold, 86)
sub_font = ImageFont.truetype(font_bold, 28)

title_text = "STONE AGE TALES"
sub_text = "• SUBSCRIBE & LIKE •"

t_box = draw.textbbox((0, 0), title_text, font=title_font)
t_w = t_box[2] - t_box[0]
s_box = draw.textbbox((0, 0), sub_text, font=sub_font)
s_w = s_box[2] - s_box[0]

cx = 1040
tx = cx - (t_w // 2)
ty = 370

sx = cx - (s_w // 2)
sy = ty + 95

# Draw Title
for dx in [-4, -3, 0, 3, 4]:
    for dy in [-4, -3, 0, 3, 4]:
        draw.text((tx + dx, ty + dy), title_text, font=title_font, fill=(15, 20, 30))

draw.text((tx + 5, ty + 5), title_text, font=title_font, fill=(0, 0, 0, 190))
draw.text((tx, ty), title_text, font=title_font, fill=(255, 229, 0))

# Draw Subtitle ("• SUBSCRIBE & LIKE •")
for dx in [-2, -1, 1, 2]:
    for dy in [-2, -1, 1, 2]:
        draw.text((sx + dx, sy + dy), sub_text, font=sub_font, fill=(255, 255, 255))
draw.text((sx, sy), sub_text, font=sub_font, fill=(20, 25, 35))

# Save output banner
final_banner = canvas.convert("RGB")
out_master = branding_dir / "banner_2048x1152.jpg"
final_banner.save(out_master, "JPEG", quality=95)

# Also update pipeline/build_stone_age_banner.py with this final code
print(f"[SUCCESS] Final Banner saved at: {out_master}")
