import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
W_9x16, H_9x16 = 1080, 1920
W_16x9, H_16x9 = 1920, 1080

COLOR_WB_BG = (247, 249, 252, 255)
COLOR_WB_CARD = (255, 255, 255, 255)
COLOR_WB_BORDER = (220, 226, 236, 255)
COLOR_INK_BLACK = (18, 24, 38, 255)
COLOR_INK_MUTED = (95, 110, 132, 255)

COLOR_EMERALD = (16, 185, 129, 255)
COLOR_EMERALD_BG = (236, 253, 245, 255)
COLOR_CRIMSON = (239, 68, 68, 255)
COLOR_CRIMSON_BG = (254, 242, 242, 255)
COLOR_COBALT = (37, 99, 235, 255)
COLOR_COBALT_BG = (239, 246, 255, 255)
COLOR_AMBER = (217, 119, 6, 255)
COLOR_AMBER_BG = (254, 243, 199, 255)

def get_font(size):
    for f in ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_centered_text(draw, cx, y, text, font, fill):
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, y), text, fill=fill, font=font)
    return w

def draw_pill(draw, cx, y, text, font, text_color, bg_color, border_color, pad_x=28, height=54, radius=14):
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    box_w = w + pad_x * 2
    x1 = cx - box_w // 2
    x2 = x1 + box_w
    draw.rounded_rectangle([(x1, y), (x2, y + height)], radius=radius, fill=bg_color, outline=border_color, width=2)
    draw_centered_text(draw, cx, y + (height - (bbox[3] - bbox[1])) // 2 - 2, text, font, text_color)
    return box_w

def generate_9x16_thumbnail(output_path):
    img = Image.new("RGBA", (W_9x16, H_9x16), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(35, 35), (W_9x16 - 35, H_9x16 - 35)], radius=24, outline=COLOR_WB_BORDER, width=4)
    
    # Category Pill
    draw_pill(draw, W_9x16 // 2, 140, "FINANCIAL MENTAL MODEL", get_font(28), COLOR_COBALT, COLOR_COBALT_BG, (190, 215, 250, 255), pad_x=32, height=56)
    
    # Hero Title
    draw_centered_text(draw, W_9x16 // 2, 230, "THE 1% COMPOUND TRAP", get_font(62), COLOR_INK_BLACK)
    
    # Subtitle Pill
    draw_pill(draw, W_9x16 // 2, 325, "Why 99% Quit Right Before Compounding Explodes", get_font(28), (180, 83, 9, 255), COLOR_AMBER_BG, (253, 230, 138, 255), pad_x=28, height=50)
    
    # 3-Stat KPI Strip
    card_w = 950
    card_h = 120
    card_x = W_9x16 // 2 - card_w // 2
    card_y = 405
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=18, fill=COLOR_WB_CARD, outline=COLOR_WB_BORDER, width=2)
    draw.line([(card_x + 316, card_y + 18), (card_x + 316, card_y + card_h - 18)], fill=COLOR_WB_BORDER, width=2)
    draw.line([(card_x + 633, card_y + 18), (card_x + 633, card_y + card_h - 18)], fill=COLOR_WB_BORDER, width=2)
    
    # Col 1
    draw.text((card_x + 35, card_y + 18), "INITIAL PRINCIPAL", fill=COLOR_INK_MUTED, font=get_font(18))
    draw.text((card_x + 35, card_y + 44), "$10,000", fill=COLOR_COBALT, font=get_font(40))
    draw.text((card_x + 35, card_y + 88), "Day 0 Base (1.00x)", fill=COLOR_INK_MUTED, font=get_font(20))
    
    # Col 2
    draw.text((card_x + 350, card_y + 18), "EXPECTED BY MO. 6", fill=COLOR_INK_MUTED, font=get_font(18))
    draw.text((card_x + 350, card_y + 44), "$185,000", fill=COLOR_CRIMSON, font=get_font(40))
    draw.text((card_x + 350, card_y + 88), "Mental Illusion Target", fill=COLOR_CRIMSON, font=get_font(20))
    
    # Col 3
    draw.text((card_x + 670, card_y + 18), "ACTUAL DAY 365", fill=COLOR_INK_MUTED, font=get_font(18))
    draw.text((card_x + 670, card_y + 44), "$377,834", fill=COLOR_EMERALD, font=get_font(40))
    draw.text((card_x + 670, card_y + 88), "+3,778% ROI (37.78x)", fill=COLOR_EMERALD, font=get_font(20))
    
    # Chart Grid & Axes
    origin_x, origin_y = 150, 1420
    max_x, min_y = W_9x16 - 100, 620
    
    for gy in [origin_y, origin_y - 200, origin_y - 400, min_y + 30]:
        draw.line([(origin_x, gy), (max_x, gy)], fill=(230, 236, 245, 255), width=2)
    for gx in range(origin_x, max_x + 1, 160):
        draw.line([(gx, min_y), (gx, origin_y)], fill=(230, 236, 245, 255), width=2)
        
    draw.line([(origin_x, min_y), (origin_x, origin_y), (max_x, origin_y)], fill=COLOR_INK_BLACK, width=7)
    
    # Linear Illusion Line (Blue)
    draw.line([(origin_x, origin_y - 20), (max_x - 100, min_y + 60)], fill=COLOR_COBALT, width=5)
    
    # Stratosphere Compounding Curve (Emerald Green)
    pts = []
    for step in range(30):
        ratio = step / 29.0
        x = origin_x + int(ratio * (max_x - origin_x - 50))
        growth = (math.exp(2.8 * ratio) - 1.0) / (math.exp(2.8) - 1.0)
        y = int((origin_y - 20) - growth * (origin_y - 20 - min_y - 30))
        pts.append((x, y))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=COLOR_EMERALD, width=14)
        
    # Peak Badge (Positioned cleanly below peak without touching valley card)
    peak_x, peak_y = pts[-1][0], pts[-1][1]
    draw_pill(draw, peak_x - 190, peak_y + 90, "+37.8x ($378K)", get_font(34), (255, 255, 255, 255), COLOR_EMERALD, (5, 140, 95, 255), pad_x=22, height=56)
    
    # Shaded Valley of Disappointment Card (Compact and cleanly positioned on left)
    draw.rounded_rectangle([(170, 580), (610, 725)], radius=18, fill=COLOR_WB_CARD, outline=COLOR_CRIMSON, width=3)
    draw_pill(draw, 390, 595, "THE VALLEY OF DISAPPOINTMENT", get_font(18), COLOR_CRIMSON, COLOR_CRIMSON_BG, (254, 202, 202, 255), pad_x=16, height=34)
    draw_centered_text(draw, 390, 638, "99% Quit In Negative Spread", get_font(26), COLOR_INK_BLACK)
    draw_centered_text(draw, 390, 678, "Mental: $185K Target  vs  Reality: $60K", get_font(20), COLOR_CRIMSON)
    draw.polygon([(390, 741), (378, 725), (402, 725)], fill=COLOR_CRIMSON)
    
    # Bottom Callout Banner
    draw_pill(draw, W_9x16 // 2, 1530, "SURVIVE THE FLATLINE TO EARN THE MULTIPLIER", get_font(30), (255, 255, 255, 255), (18, 24, 38, 255), COLOR_AMBER, pad_x=32, height=64)
    draw_centered_text(draw, W_9x16 // 2, 1618, "Initial $10,000 Grows into $377,834 with 1% Daily Improvements", get_font(26), COLOR_INK_MUTED)
    
    img.convert("RGB").save(output_path, quality=95)
    print(f"[Thumbnail 9x16] Saved: {output_path}")

def generate_16x9_thumbnail(output_path):
    img = Image.new("RGBA", (W_16x9, H_16x9), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(30, 30), (W_16x9 - 30, H_16x9 - 30)], radius=24, outline=COLOR_WB_BORDER, width=4)
    
    # Left Column: High-Impact Typography & Narrative
    draw_pill(draw, 450, 100, "FINANCIAL LAWS", get_font(26), COLOR_COBALT, COLOR_COBALT_BG, (190, 215, 250, 255), pad_x=28, height=50)
    
    draw.text((120, 180), "THE 1% COMPOUND TRAP", fill=COLOR_INK_BLACK, font=get_font(60))
    draw_pill(draw, 480, 275, "Why 99% Quit Right Before Compounding Explodes", get_font(26), (180, 83, 9, 255), COLOR_AMBER_BG, (253, 230, 138, 255), pad_x=24, height=48)
    
    # 4-Stage Comparison Mini-Table on Left
    table_y = 350
    table_x = 120
    table_w = 680
    card_h = 105
    stages = [
        ("STAGE 1: DAY 90", "$24,486", "+$14.5K Gain (2.45x)", COLOR_INK_MUTED, (246, 248, 252, 255)),
        ("STAGE 2: DAY 180", "$59,958", "+$50.0K Gain (6.00x)", COLOR_COBALT, COLOR_COBALT_BG),
        ("STAGE 3: DAY 270", "$146,815", "+$136.8K (14.68x)", COLOR_AMBER, COLOR_AMBER_BG),
        ("STAGE 4: DAY 365", "$377,834", "+$367.8K (37.78x)", COLOR_EMERALD, COLOR_EMERALD_BG),
    ]
    for idx, (title, bal, gain, accent, bg) in enumerate(stages):
        cy = table_y + idx * (card_h + 14)
        draw.rounded_rectangle([(table_x, cy), (table_x + table_w, cy + card_h)], radius=14, fill=bg, outline=accent, width=2)
        draw.text((table_x + 25, cy + 18), title, fill=accent, font=get_font(20))
        draw.text((table_x + 25, cy + 46), bal, fill=COLOR_INK_BLACK, font=get_font(38))
        draw.text((table_x + 360, cy + 50), gain, fill=accent, font=get_font(26))
        
    draw_pill(draw, 460, 860, "CRITICAL MASS INFLECTION: DAY 270 ($146.8K)", get_font(24), COLOR_EMERALD, COLOR_EMERALD_BG, (167, 243, 208, 255), pad_x=24, height=50)
    draw_centered_text(draw, 460, 930, "\"Survive the flatline to earn the multiplier.\"", get_font(26), COLOR_INK_MUTED)
    
    # Right Column: Big Dramatic Graph
    origin_x, origin_y = 920, 880
    max_x, min_y = W_16x9 - 100, 220
    
    for gy in [origin_y, origin_y - 200, origin_y - 400, min_y + 20]:
        draw.line([(origin_x, gy), (max_x, gy)], fill=(230, 236, 245, 255), width=2)
    for gx in range(origin_x, max_x + 1, 180):
        draw.line([(gx, min_y), (gx, origin_y)], fill=(230, 236, 245, 255), width=2)
        
    draw.line([(origin_x, min_y), (origin_x, origin_y), (max_x, origin_y)], fill=COLOR_INK_BLACK, width=7)
    
    # Linear Illusion Line (Blue)
    draw.line([(origin_x, origin_y - 20), (max_x - 120, min_y + 80)], fill=COLOR_COBALT, width=5)
    draw.text((origin_x + 60, min_y + 110), "Linear Expectation ($185K)", fill=COLOR_COBALT, font=get_font(22))
    
    # Compounding Curve (Emerald)
    pts = []
    for step in range(30):
        ratio = step / 29.0
        x = origin_x + int(ratio * (max_x - origin_x - 40))
        growth = (math.exp(2.8 * ratio) - 1.0) / (math.exp(2.8) - 1.0)
        y = int((origin_y - 20) - growth * (origin_y - 20 - min_y - 20))
        pts.append((x, y))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=COLOR_EMERALD, width=14)
        
    # Massive Peak Callout Pill
    peak_x, peak_y = pts[-1][0], pts[-1][1]
    draw_pill(draw, peak_x - 220, peak_y + 30, "+37.8x ($377,834)", get_font(36), (255, 255, 255, 255), COLOR_EMERALD, (5, 140, 95, 255), pad_x=28, height=62)
    
    # Valley of Disappointment Card on Right
    draw.rounded_rectangle([(origin_x + 40, 420), (origin_x + 480, 560)], radius=16, fill=COLOR_WB_CARD, outline=COLOR_CRIMSON, width=3)
    draw_pill(draw, origin_x + 260, 436, "VALLEY OF DISAPPOINTMENT", get_font(18), COLOR_CRIMSON, COLOR_CRIMSON_BG, (254, 202, 202, 255), pad_x=16, height=32)
    draw_centered_text(draw, origin_x + 260, 480, "99% Quit In Negative Spread", get_font(26), COLOR_INK_BLACK)
    draw_centered_text(draw, origin_x + 260, 518, "-$125,000 Frustration Gap", get_font(20), COLOR_CRIMSON)
    
    img.convert("RGB").save(output_path, quality=95)
    print(f"[Thumbnail 16x9] Saved: {output_path}")

if __name__ == "__main__":
    out_dir = Path("productions/shorts/the-1-compound-trap")
    out_dir.mkdir(parents=True, exist_ok=True)
    generate_9x16_thumbnail(out_dir / "thumbnail_9x16.jpg")
    generate_16x9_thumbnail(out_dir / "thumbnail_16x9.jpg")
