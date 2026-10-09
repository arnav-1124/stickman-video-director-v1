import os
import sys
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
branding_dir = root_dir / "assets/branding/stone_age_tales"
branding_dir.mkdir(parents=True, exist_ok=True)

ep2_slides = root_dir / "projects/long/ep02_how_humans_invented_the_first_lie/slides"
s15_path = ep2_slides / "slide_15.jpg"  # 5 tribe stickmen walking in savanna
s16_path = ep2_slides / "slide_16.jpg"  # Leopard + Monkey in Acacia tree
ref_hero = root_dir / "ref_01_ink_explainer_savanna_day.jpg"  # Hero stickman standing

# 1. Base Canvas: 2048 x 1152 from slide_15
base_s15 = Image.open(s15_path).convert("RGB")
banner = base_s15.resize((2048, 1152), Image.Resampling.LANCZOS)

# 2. Extract Leopard from slide_16 (Native 1920x1080: X ~ 1140 to 1720, Y ~ 560 to 760)
s16_img = Image.open(s16_path).convert("RGBA")
# Crop leopard region
leopard_crop = s16_img.crop((1140, 560, 1720, 755))
# Create soft feathered alpha mask based on savanna background color
leopard_np = np.array(leopard_crop)
# Savanna color in slide_16 is around RGB (235, 185, 95)
# Let's create an alpha mask that keeps the leopard (yellow/black spots, black outline)
diff = np.abs(leopard_np[:, :, :3] - np.array([235, 186, 96]))
dist = np.mean(diff, axis=2)
# Pixels that differ significantly from background are part of the leopard
alpha = np.clip((dist - 8) * 12, 0, 255).astype(np.uint8)

# Feather the mask slightly
leopard_mask = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.5))
leopard_crop.putalpha(leopard_mask)

# Resize leopard for banner right flank
leopard_resized = leopard_crop.resize((int(leopard_crop.width * 1.05), int(leopard_crop.height * 1.05)), Image.Resampling.LANCZOS)
# Paste on the right side of savanna in banner (X: 1420, Y: 680)
banner_rgba = banner.convert("RGBA")
banner_rgba.paste(leopard_resized, (1420, 680), leopard_resized)

# 3. Extract Monkey on Acacia Tree branch from slide_16 (X ~ 120 to 600, Y ~ 100 to 480)
tree_monkey_crop = s16_img.crop((20, 80, 850, 600))
# Create mask for tree and monkey (sky is around RGB (110, 195, 235))
tree_np = np.array(tree_monkey_crop)
sky_color = np.array([120, 198, 238])
diff_sky = np.abs(tree_np[:, :, :3] - sky_color)
dist_sky = np.mean(diff_sky, axis=2)
alpha_tree = np.clip((dist_sky - 12) * 10, 0, 255).astype(np.uint8)
tree_mask = Image.fromarray(alpha_tree).filter(ImageFilter.GaussianBlur(1.2))
tree_monkey_crop.putalpha(tree_mask)

# Resize tree & monkey to frame the left/top corner naturally
tree_resized = tree_monkey_crop.resize((int(tree_monkey_crop.width * 0.75), int(tree_monkey_crop.height * 0.75)), Image.Resampling.LANCZOS)
# Paste in upper-left corner of banner (X: -40, Y: -20)
banner_rgba.paste(tree_resized, (-40, -10), tree_resized)

# 4. Add the Hero stickman on the far left in foreground
hero_img = Image.open(ref_hero).convert("RGBA")
# Hero is from X: 220 to 480, Y: 130 to 700 in 1280x720
hero_crop = hero_img.crop((230, 140, 480, 660))
hero_np = np.array(hero_crop)
# Sky is blue, ground is yellow
# Non-white, non-sky, non-ground
# Let's extract hero
diff_h_sky = np.mean(np.abs(hero_np[:, :, :3] - np.array([115, 196, 236])), axis=2)
diff_h_ground = np.mean(np.abs(hero_np[:, :, :3] - np.array([218, 175, 96])), axis=2)
hero_alpha = np.clip((np.minimum(diff_h_sky, diff_h_ground) - 8) * 12, 0, 255).astype(np.uint8)
hero_mask = Image.fromarray(hero_alpha).filter(ImageFilter.GaussianBlur(1.2))
hero_crop.putalpha(hero_mask)

hero_scale = 0.95
hero_resized = hero_crop.resize((int(hero_crop.width * hero_scale), int(hero_crop.height * hero_scale)), Image.Resampling.LANCZOS)
# Paste on foreground left (X: 140, Y: 560)
banner_rgba.paste(hero_resized, (140, 560), hero_resized)

# 5. Clean up bottom-right corner watermark
draw = ImageDraw.Draw(banner_rgba)
savanna_sample = banner_rgba.crop((1650, 1000, 1850, 1152))
banner_rgba.paste(savanna_sample, (1840, 1000))

# 6. Center Branding Typography (YouTube Safe Area: X ~ 600 to 1500, Y ~ 380 to 520 in Open Sky)
font_bold = "C:/Windows/Fonts/ARLRDBD.TTF"
if not os.path.exists(font_bold):
    font_bold = "C:/Windows/Fonts/arialbd.ttf"

title_font = ImageFont.truetype(font_bold, 92)
sub_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 32)

title_text = "STONE AGE TALES"
sub_text = "HOW ANCIENT HUMANS SURVIVED, THOUGHT & EVOLVED"

t_box = draw.textbbox((0, 0), title_text, font=title_font)
t_w = t_box[2] - t_box[0]
s_box = draw.textbbox((0, 0), sub_text, font=sub_font)
s_w = s_box[2] - s_box[0]

# Center in banner
tx = (2048 - t_w) // 2
ty = 390

sx = (2048 - s_w) // 2
sy = ty + 115

# Soft subtle white backing glow behind title to separate from clouds/sky
glow = Image.new("RGBA", (2048, 1152), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow)
g_draw.rectangle([min(tx, sx) - 35, ty - 20, max(tx + t_w, sx + s_w) + 35, sy + 45], fill=(255, 255, 255, 140))
glow = glow.filter(ImageFilter.GaussianBlur(18))
banner_rgba = Image.alpha_composite(banner_rgba, glow)

draw = ImageDraw.Draw(banner_rgba)

# Draw Title (Drop Shadow + Bold Dark Outline + Vibrant Canary Gold #FFE500)
for dx in [-5, -4, 0, 4, 5]:
    for dy in [-5, -4, 0, 4, 5]:
        draw.text((tx + dx, ty + dy), title_text, font=title_font, fill=(15, 20, 30))

draw.text((tx + 6, ty + 6), title_text, font=title_font, fill=(0, 0, 0, 160))
draw.text((tx, ty), title_text, font=title_font, fill=(255, 229, 0))

# Subtitle (Charcoal Navy with Crisp White Outline)
for dx in [-2, 0, 2]:
    for dy in [-2, 0, 2]:
        draw.text((sx + dx, sy + dy), sub_text, font=sub_font, fill=(255, 255, 255))
draw.text((sx, sy), sub_text, font=sub_font, fill=(20, 25, 40))

final_banner = banner_rgba.convert("RGB")
out_banner = branding_dir / "banner_mini_world_2048x1152.jpg"
final_banner.save(out_banner, "JPEG", quality=95)

# Also update the primary banner file
out_master = branding_dir / "banner_2048x1152.jpg"
final_banner.save(out_master, "JPEG", quality=95)

print(f"[SUCCESS] Mini-World Banner created at: {out_master}")
