import math
import random
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1080
HEIGHT = 1920
FPS = 30
FLOOR_Y = 1450

# Whiteboard Color Palette (Clean, high-contrast, modern studio explainer)
COLOR_WB_BG = (246, 248, 250, 255)       # Premium off-white vellum
COLOR_WB_CARD = (255, 255, 255, 240)     # Pure white layered card
COLOR_INK_BLACK = (24, 27, 34, 255)      # Rich charcoal dry-erase marker
COLOR_INK_MUTED = (115, 125, 145, 255)   # Pencil/sketch gray
COLOR_EMERALD = (16, 185, 129, 255)      # Finance growth green
COLOR_EMERALD_BG = (236, 253, 245, 255)  # Light mint card fill
COLOR_CRIMSON = (239, 68, 68, 255)       # Debt / Trap red
COLOR_CRIMSON_BG = (254, 242, 242, 255)  # Light red card fill
COLOR_COBALT = (37, 99, 235, 255)        # Frame / Logic blue
COLOR_AMBER = (245, 158, 11, 255)        # Golden wealth / attention
COLOR_AMBER_BG = (254, 243, 199, 255)    # Light gold card fill
COLOR_CROWD = (140, 148, 165, 200)       # Gray crowd tone

def get_font(size):
    for font_name in ["segoeuib.ttf", "arialbd.ttf", "consola.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return ImageFont.load_default()

FONT_BADGE = get_font(28)
FONT_SUB = get_font(32)
FONT_BODY = get_font(30)
FONT_CAPTION = get_font(28)
FONT_TITLE = get_font(64)
FONT_LARGE = get_font(80)

def draw_centered_text(draw, cx, y, text, font, fill):
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, y), text, fill=fill, font=font)
    return w

def draw_pill_badge(draw, cx, y, text, font, text_color, fill_color, outline_color, padding_x=28, height=52, radius=14, width_override=None):
    bbox = font.getbbox(text)
    w = (bbox[2] - bbox[0]) if width_override is None else width_override
    box_w = w + padding_x * 2 if width_override is None else width_override
    x1 = cx - box_w // 2
    x2 = x1 + box_w
    y1 = y
    y2 = y + height
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=radius, fill=fill_color, outline=outline_color, width=2)
    draw_centered_text(draw, cx, y + (height - (bbox[3] - bbox[1])) // 2 - 2, text, font, text_color)
    return box_w

def draw_hand_drawn_line(draw, points, color, width=6, jitter=1.2, seed=42):
    """Draws a polyline with organic micro-jitter for authentic marker ink."""
    if len(points) < 2:
        return
    rng = random.Random(seed)
    jittered = []
    for i, (x, y) in enumerate(points):
        if i == 0 or i == len(points) - 1:
            jittered.append((x, y))
        else:
            jx = x + rng.uniform(-jitter, jitter)
            jy = y + rng.uniform(-jitter, jitter)
            jittered.append((jx, jy))
            
    for i in range(len(jittered) - 1):
        p1 = jittered[i]
        p2 = jittered[i + 1]
        draw.line([p1, p2], fill=color, width=width)
        draw.ellipse([(p1[0] - width // 2, p1[1] - width // 2), (p1[0] + width // 2, p1[1] + width // 2)], fill=color)
        draw.ellipse([(p2[0] - width // 2, p2[1] - width // 2), (p2[0] + width // 2, p2[1] + width // 2)], fill=color)

def draw_marker_pen(draw, tip_x, tip_y, angle_deg=-45, color=COLOR_EMERALD):
    """Draws a stylized dry-erase chisel marker whose nib touches (tip_x, tip_y)."""
    rad = math.radians(angle_deg)
    pen_len = 160
    pen_w = 26
    
    dx = math.cos(rad)
    dy = math.sin(rad)
    nx = -dy
    ny = dx
    
    nib_len = 22
    nib_base_x = tip_x - dx * nib_len
    nib_base_y = tip_y - dy * nib_len
    draw.polygon([
        (tip_x, tip_y),
        (nib_base_x + nx * (pen_w * 0.35), nib_base_y + ny * (pen_w * 0.35)),
        (nib_base_x - nx * (pen_w * 0.35), nib_base_y - ny * (pen_w * 0.35))
    ], fill=color)
    
    grip_len = 45
    grip_end_x = nib_base_x - dx * grip_len
    grip_end_y = nib_base_y - dy * grip_len
    draw.polygon([
        (nib_base_x + nx * (pen_w * 0.45), nib_base_y - ny * (pen_w * 0.45)),
        (nib_base_x - nx * (pen_w * 0.45), nib_base_y - ny * (pen_w * 0.45)),
        (grip_end_x - nx * (pen_w * 0.5), grip_end_y - ny * (pen_w * 0.5)),
        (grip_end_x + nx * (pen_w * 0.5), grip_end_y + ny * (pen_w * 0.5))
    ], fill=(45, 52, 64, 255))
    
    body_end_x = grip_end_x - dx * (pen_len - grip_len - nib_len)
    body_end_y = grip_end_y - dy * (pen_len - grip_len - nib_len)
    draw.polygon([
        (grip_end_x + nx * (pen_w * 0.5), grip_end_y + ny * (pen_w * 0.5)),
        (grip_end_x - nx * (pen_w * 0.5), grip_end_y - ny * (pen_w * 0.5)),
        (body_end_x - nx * (pen_w * 0.5), body_end_y - ny * (pen_w * 0.5)),
        (body_end_x + nx * (pen_w * 0.5), body_end_y + ny * (pen_w * 0.5))
    ], fill=(240, 243, 248, 255), outline=(180, 190, 205, 255), width=2)
    
    # Accent color band
    band_start_x = grip_end_x - dx * 15
    band_start_y = grip_end_y - dy * 15
    band_end_x = band_start_x - dx * 18
    band_end_y = band_start_y - dy * 18
    draw.polygon([
        (band_start_x + nx * (pen_w * 0.5), band_start_y + ny * (pen_w * 0.5)),
        (band_start_x - nx * (pen_w * 0.5), band_start_y - ny * (pen_w * 0.5)),
        (band_end_x - nx * (pen_w * 0.5), band_end_y - ny * (pen_w * 0.5)),
        (band_end_x + nx * (pen_w * 0.5), band_end_y + ny * (pen_w * 0.5))
    ], fill=color)

def draw_whiteboard_stickman(draw, cx, cy, pose="pointing_up", scale=1.0, color=COLOR_INK_BLACK, facing=1):
    """Draws an expressive, multi-joint whiteboard stickman with rich poses."""
    head_r = int(32 * scale)
    head_y = int(cy - 190 * scale)
    neck_y = int(head_y + head_r)
    hip_y = int(cy - 75 * scale)
    w_line = max(4, int(6.5 * scale))
    
    # Head with hand-drawn circle
    draw.ellipse([(cx - head_r, head_y - head_r), (cx + head_r, head_y + head_r)], outline=color, width=int(6 * scale))
    
    # Spine
    draw.line([(cx, neck_y), (cx, hip_y)], fill=color, width=int(7 * scale))
    
    f = 1 if facing >= 0 else -1
    
    if pose == "pushing_snowball":
        draw.line([(cx, neck_y), (cx - 20 * scale * f, hip_y)], fill=color, width=int(7 * scale))
        draw.line([(cx - 10 * scale * f, neck_y + 15 * scale), (cx + 35 * scale * f, neck_y + 30 * scale)], fill=color, width=w_line)
        draw.line([(cx + 35 * scale * f, neck_y + 30 * scale), (cx + 70 * scale * f, neck_y + 20 * scale)], fill=color, width=w_line)
        draw.line([(cx - 10 * scale * f, neck_y + 25 * scale), (cx + 40 * scale * f, neck_y + 45 * scale)], fill=color, width=w_line)
        draw.line([(cx + 40 * scale * f, neck_y + 45 * scale), (cx + 75 * scale * f, neck_y + 40 * scale)], fill=color, width=w_line)
        draw.line([(cx - 20 * scale * f, hip_y), (cx - 65 * scale * f, cy)], fill=color, width=w_line)
        draw.line([(cx - 20 * scale * f, hip_y), (cx + 15 * scale * f, cy)], fill=color, width=w_line)
        draw.ellipse([(cx - 35 * scale * f, head_y - 15 * scale), (cx - 28 * scale * f, head_y - 8 * scale)], fill=COLOR_COBALT)
        
    elif pose == "quitting_frustrated":
        draw.line([(cx, neck_y + 15 * scale), (cx - 45 * scale * f, neck_y - 45 * scale)], fill=color, width=w_line)
        draw.line([(cx - 45 * scale * f, neck_y - 45 * scale), (cx - 60 * scale * f, neck_y - 80 * scale)], fill=color, width=w_line)
        draw.line([(cx, neck_y + 15 * scale), (cx + 40 * scale * f, neck_y - 40 * scale)], fill=color, width=w_line)
        draw.line([(cx + 40 * scale * f, neck_y - 40 * scale), (cx + 55 * scale * f, neck_y - 75 * scale)], fill=color, width=w_line)
        draw.line([(cx, hip_y), (cx - 40 * scale * f, cy)], fill=color, width=w_line)
        draw.line([(cx, hip_y), (cx + 30 * scale * f, cy)], fill=color, width=w_line)
        for i in range(8):
            sx = int(cx + (i - 4) * 8 * scale)
            sy = int(head_y - head_r - 20 * scale + (i % 2) * 12 * scale)
            draw.line([(sx, sy), (sx + 8, sy - 8)], fill=COLOR_CRIMSON, width=3)
            
    elif pose == "confident_arms_crossed":
        draw.line([(cx, neck_y + 20 * scale), (cx - 35 * scale, neck_y + 45 * scale)], fill=color, width=w_line)
        draw.line([(cx - 35 * scale, neck_y + 45 * scale), (cx + 35 * scale, neck_y + 45 * scale)], fill=color, width=w_line)
        draw.line([(cx, neck_y + 20 * scale), (cx + 35 * scale, neck_y + 45 * scale)], fill=color, width=w_line)
        draw.line([(cx, hip_y), (cx - 35 * scale, cy)], fill=color, width=w_line)
        draw.line([(cx, hip_y), (cx + 35 * scale, cy)], fill=color, width=w_line)
        sg_y = head_y - int(4 * scale)
        draw.line([(cx - int(24 * scale), sg_y), (cx + int(24 * scale), sg_y)], fill=color, width=int(5 * scale))
        draw.rectangle([(cx - int(22 * scale), sg_y), (cx - int(4 * scale), sg_y + int(12 * scale))], fill=color)
        draw.rectangle([(cx + int(4 * scale), sg_y), (cx + int(22 * scale), sg_y + int(12 * scale))], fill=color)
        
    elif pose == "pointing_up":
        draw.line([(cx, neck_y + 20 * scale), (cx + 50 * scale * f, neck_y - 30 * scale)], fill=color, width=w_line)
        draw.line([(cx + 50 * scale * f, neck_y - 30 * scale), (cx + 80 * scale * f, neck_y - 95 * scale)], fill=color, width=w_line)
        draw.line([(cx, neck_y + 20 * scale), (cx - 40 * scale * f, neck_y + 40 * scale)], fill=color, width=w_line)
        draw.line([(cx - 40 * scale * f, neck_y + 40 * scale), (cx - 15 * scale * f, hip_y)], fill=color, width=w_line)
        draw.line([(cx, hip_y), (cx - 45 * scale, cy)], fill=color, width=w_line)
        draw.line([(cx, hip_y), (cx + 45 * scale, cy)], fill=color, width=w_line)
        
    elif pose == "pointing_viewer":
        draw.line([(cx, neck_y + 20 * scale), (cx + 25 * scale, neck_y + 50 * scale)], fill=color, width=w_line)
        draw.ellipse([(cx + 25 * scale - 12, neck_y + 50 * scale - 12), (cx + 25 * scale + 12, neck_y + 50 * scale + 12)], fill=color)
        draw.line([(cx, neck_y + 20 * scale), (cx - 40 * scale, neck_y + 40 * scale)], fill=color, width=w_line)
        draw.line([(cx - 40 * scale, neck_y + 40 * scale), (cx - 15 * scale, hip_y)], fill=color, width=w_line)
        draw.line([(cx, hip_y), (cx - 35 * scale, cy)], fill=color, width=w_line)
        draw.line([(cx, hip_y), (cx + 35 * scale, cy)], fill=color, width=w_line)
        
    elif pose == "hamster_running":
        cycle = (scale * 5.0) % 1.0
        leg_ang = math.sin(cycle * math.pi * 2)
        draw.line([(cx, neck_y), (cx + 20 * scale * f, hip_y)], fill=color, width=w_line)
        draw.line([(cx + 10 * scale * f, neck_y + 15 * scale), (cx + 45 * scale * f, neck_y + (15 + leg_ang * 25) * scale)], fill=color, width=w_line)
        draw.line([(cx + 10 * scale * f, neck_y + 15 * scale), (cx - 30 * scale * f, neck_y + (15 - leg_ang * 25) * scale)], fill=color, width=w_line)
        draw.line([(cx + 20 * scale * f, hip_y), (cx + (40 + leg_ang * 35) * scale * f, cy)], fill=color, width=w_line)
        draw.line([(cx + 20 * scale * f, hip_y), (cx - (20 + leg_ang * 35) * scale * f, cy)], fill=color, width=w_line)

def draw_hamster_wheel_crowd(draw, base_x, base_y, progress=0.0):
    """Draws a multi-character crowd trapped in the daily hamster wheel chasing quick dopamine."""
    wheel_r = 135
    wheel_cx = base_x
    wheel_cy = base_y - wheel_r - 20
    
    draw.ellipse([(wheel_cx - wheel_r, wheel_cy - wheel_r), (wheel_cx + wheel_r, wheel_cy + wheel_r)], outline=COLOR_INK_MUTED, width=6)
    draw.ellipse([(wheel_cx - wheel_r + 14, wheel_cy - wheel_r + 14), (wheel_cx + wheel_r - 14, wheel_cy + wheel_r - 14)], outline=(200, 210, 225, 255), width=2)
    
    ang_offset = progress * 6.0
    for s in range(8):
        a = ang_offset + s * (math.pi / 4)
        sx = wheel_cx + math.cos(a) * (wheel_r - 14)
        sy = wheel_cy + math.sin(a) * (wheel_r - 14)
        draw.line([(wheel_cx, wheel_cy), (sx, sy)], fill=(180, 190, 205, 255), width=3)
    draw.ellipse([(wheel_cx - 16, wheel_cy - 16), (wheel_cx + 16, wheel_cy + 16)], fill=COLOR_INK_MUTED)
    
    draw_whiteboard_stickman(draw, wheel_cx - 15, wheel_cy + wheel_r - 20, pose="hamster_running", scale=0.75, color=COLOR_CRIMSON, facing=1)
    
    bait_x = wheel_cx + wheel_r + 55
    bait_y = wheel_cy - 40 + int(math.sin(progress * 10) * 12)
    draw.line([(wheel_cx + 40, wheel_cy - wheel_r - 10), (bait_x, bait_y - 25)], fill=COLOR_INK_MUTED, width=3)
    draw.line([(bait_x, bait_y - 25), (bait_x, bait_y)], fill=(150, 160, 175, 255), width=2)
    draw.ellipse([(bait_x - 22, bait_y - 22), (bait_x + 22, bait_y + 22)], fill=COLOR_AMBER, outline=(180, 120, 0, 255), width=3)
    draw.text((bait_x - 8, bait_y - 16), "$", fill=(255, 255, 255, 255), font=get_font(28))
    
    for ci in range(3):
        cx_pos = wheel_cx - wheel_r - 65 - ci * 70
        draw_whiteboard_stickman(draw, cx_pos, base_y, pose="quitting_frustrated", scale=0.85 - ci * 0.08, color=COLOR_CROWD, facing=1)

def draw_whiteboard_header(draw, badge_text, title_text, sub_text, badge_color=COLOR_COBALT):
    """Draws a standardized high-retention whiteboard header card."""
    pill_w = 460
    pill_h = 56
    pill_x = WIDTH // 2 - pill_w // 2
    pill_y = 150
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=16, fill=(238, 242, 250, 255), outline=badge_color, width=2)
    draw_centered_text(draw, WIDTH // 2, pill_y + 12, badge_text, FONT_BADGE, badge_color)
    
    draw_centered_text(draw, WIDTH // 2, 235, title_text, FONT_TITLE, COLOR_INK_BLACK)
    
    sub_bbox = FONT_SUB.getbbox(sub_text)
    sub_w = sub_bbox[2] - sub_bbox[0]
    hl_y = 330
    draw.rounded_rectangle([(WIDTH // 2 - sub_w // 2 - 16, hl_y), (WIDTH // 2 + sub_w // 2 + 16, hl_y + 44)], radius=8, fill=COLOR_AMBER_BG)
    draw_centered_text(draw, WIDTH // 2, hl_y + 4, sub_text, FONT_SUB, (180, 83, 9, 255))

def draw_bottom_caption_bar(draw, caption_text, accent_color=COLOR_COBALT):
    """Anchors the caption card safely at the very bottom edge (MarginV ~120), perfectly padded."""
    c_bbox = FONT_CAPTION.getbbox(caption_text)
    cw = c_bbox[2] - c_bbox[0]
    card_w = min(1000, max(720, cw + 80))
    card_h = 76
    card_x = WIDTH // 2 - card_w // 2
    card_y = 1760
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=18, fill=(20, 24, 34, 255), outline=accent_color, width=2)
    draw_centered_text(draw, WIDTH // 2, card_y + 22, caption_text, FONT_CAPTION, (255, 255, 255, 255))

# =========================================================================
# SCENE 1: THE FLATLINE TRAP & THE 37.8x PARADOX
# =========================================================================
def render_whiteboard_scene1(t, duration=8.5):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(40, 40), (WIDTH - 40, HEIGHT - 40)], radius=24, outline=(225, 230, 238, 255), width=3)
    
    draw_whiteboard_header(draw, "THE 1% RULE", "THE 37.8x PARADOX", "1.01^365 vs 0.99^365", COLOR_COBALT)
    
    origin_x, origin_y = 180, 1260
    max_x, min_y = WIDTH - 160, 560
    for gy in range(min_y, origin_y + 1, 140):
        draw.line([(origin_x, gy), (max_x, gy)], fill=(228, 234, 244, 255), width=2)
    for gx in range(origin_x, max_x + 1, 140):
        draw.line([(gx, min_y), (gx, origin_y)], fill=(228, 234, 244, 255), width=2)
    draw_hand_drawn_line(draw, [(origin_x, min_y), (origin_x, origin_y), (max_x, origin_y)], COLOR_INK_BLACK, width=7)
    
    base_y = origin_y - 180
    draw.line([(origin_x, base_y), (max_x - 100, base_y)], fill=(160, 172, 190, 255), width=3)
    draw.text((origin_x + 20, base_y + 10), "Status Quo (No Change)", fill=COLOR_INK_MUTED, font=get_font(24))
    
    flat_prog = min(1.0, t / 4.0)
    flat_len = int(flat_prog * 450)
    draw_hand_drawn_line(draw, [(origin_x, base_y), (origin_x + flat_len, base_y)], COLOR_COBALT, width=8)
    
    if flat_len > 10:
        pen_x = origin_x + flat_len
        draw_marker_pen(draw, pen_x, base_y, angle_deg=-45, color=COLOR_COBALT)
        
    hero_x = origin_x + int(flat_prog * 360) + 40
    ball_r = 35 + int(flat_prog * 20)
    draw.ellipse([(hero_x + 60 - ball_r, base_y - ball_r * 2), (hero_x + 60 + ball_r, base_y)], fill=(255, 255, 255, 255), outline=COLOR_INK_BLACK, width=4)
    draw.text((hero_x + 50, base_y - ball_r - 14), "$", fill=COLOR_AMBER, font=get_font(32))
    
    draw_whiteboard_stickman(draw, hero_x, base_y, pose="pushing_snowball", scale=1.1, color=COLOR_INK_BLACK, facing=1)
    
    draw_pill_badge(draw, WIDTH // 2, 1400, "DAY 1 TO 180: ZERO VISIBLE CHANGE", FONT_SUB, (180, 83, 9, 255), COLOR_AMBER_BG, COLOR_AMBER, padding_x=32, height=58)
    
    draw_bottom_caption_bar(draw, "IF YOU GET 1% BETTER EVERY DAY FOR A YEAR...", COLOR_COBALT)
    return img

# =========================================================================
# SCENE 2: THE VALLEY OF DISAPPOINTMENT
# =========================================================================
def render_whiteboard_scene2(t, duration=8.5):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(40, 40), (WIDTH - 40, HEIGHT - 40)], radius=24, outline=(225, 230, 238, 255), width=3)
    
    draw_whiteboard_header(draw, "THE COGNITIVE BIAS", "THE VALLEY OF DISAPPOINTMENT", "Expectations vs Harsh Reality", COLOR_CRIMSON)
    
    origin_x, origin_y = 180, 1260
    max_x, min_y = WIDTH - 160, 560
    for gy in range(min_y, origin_y + 1, 140):
        draw.line([(origin_x, gy), (max_x, gy)], fill=(228, 234, 244, 255), width=2)
    for gx in range(origin_x, max_x + 1, 140):
        draw.line([(gx, min_y), (gx, origin_y)], fill=(228, 234, 244, 255), width=2)
    draw_hand_drawn_line(draw, [(origin_x, min_y), (origin_x, origin_y), (max_x, origin_y)], COLOR_INK_BLACK, width=7)
    
    base_y = origin_y - 180
    
    draw.line([(origin_x, base_y), (max_x - 120, min_y + 120)], fill=(120, 150, 220, 200), width=4)
    draw.text((origin_x + 180, min_y + 220), "What We Expect (Linear)", fill=COLOR_COBALT, font=get_font(24))
    
    decay_pts = []
    prog = min(1.0, t / 4.0)
    steps = int(prog * 25)
    for step in range(steps + 1):
        ratio = step / 24.0
        x = origin_x + int(ratio * 680)
        decay = math.exp(-2.5 * ratio)
        y = int(base_y + (origin_y - base_y - 40) * (1.0 - decay))
        decay_pts.append((x, y))
    if len(decay_pts) > 1:
        draw_hand_drawn_line(draw, decay_pts, COLOR_CRIMSON, width=8)
        draw_marker_pen(draw, decay_pts[-1][0], decay_pts[-1][1], angle_deg=-45, color=COLOR_CRIMSON)
        
    draw.rounded_rectangle([(340, 880), (WIDTH - 200, 1020)], radius=14, fill=COLOR_CRIMSON_BG, outline=COLOR_CRIMSON, width=2)
    draw_centered_text(draw, (340 + WIDTH - 200) // 2, 905, "THE VALLEY OF DISAPPOINTMENT", get_font(26), COLOR_CRIMSON)
    draw_centered_text(draw, (340 + WIDTH - 200) // 2, 955, "Where 99% Give Up & Quit", get_font(24), COLOR_INK_MUTED)
    
    draw_whiteboard_stickman(draw, 820, 1600, pose="quitting_frustrated", scale=1.3, color=COLOR_CRIMSON, facing=1)
    
    draw_bottom_caption_bar(draw, "MOST PEOPLE QUIT BECAUSE PROGRESS FEELS INVISIBLE", COLOR_CRIMSON)
    return img

# =========================================================================
# SCENE 3: THE SNOWBALL CRITICAL MASS
# =========================================================================
def render_whiteboard_scene3(t, duration=8.5):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(40, 40), (WIDTH - 40, HEIGHT - 40)], radius=24, outline=(225, 230, 238, 255), width=3)
    
    draw_whiteboard_header(draw, "THE MECHANISM", "THE CRITICAL MASS THRESHOLD", "Effort Stacks Before Results Show", COLOR_AMBER)
    
    incline_x1, incline_y1 = 120, 720
    incline_x2, incline_y2 = WIDTH - 120, 1280
    draw_hand_drawn_line(draw, [(incline_x1, incline_y1), (incline_x2, incline_y2)], COLOR_INK_BLACK, width=8)
    
    roll_prog = min(1.0, t / 5.0)
    ball_cx = int(incline_x1 + roll_prog * (incline_x2 - incline_x1 - 150))
    ball_cy = int(incline_y1 + roll_prog * (incline_y2 - incline_y1 - 150))
    ball_r = int(50 + roll_prog * 90)
    
    draw.ellipse([(ball_cx - ball_r, ball_cy - ball_r * 2), (ball_cx + ball_r, ball_cy)], fill=COLOR_WB_CARD, outline=COLOR_EMERALD, width=8)
    draw.text((ball_cx - 25, ball_cy - ball_r - 20), "$$$", fill=COLOR_EMERALD, font=get_font(42))
    
    for i in range(5):
        lx = ball_cx - ball_r - 30 - i * 35
        ly = ball_cy - ball_r + i * 15
        draw.line([(lx, ly), (lx + 25, ly)], fill=COLOR_INK_MUTED, width=4)
        
    draw_whiteboard_stickman(draw, 240, 720, pose="confident_arms_crossed", scale=1.2, color=COLOR_INK_BLACK)
    
    draw_pill_badge(draw, WIDTH // 2, 1420, "CRITICAL MASS: MOMENTUM TAKES OVER", FONT_SUB, COLOR_EMERALD, COLOR_EMERALD_BG, COLOR_EMERALD, padding_x=34, height=58)
    
    draw_bottom_caption_bar(draw, "COMPOUNDING REWARDS ENDURANCE OVER INTENSITY", COLOR_AMBER)
    return img

# =========================================================================
# SCENE 4: THE VERTICAL SKYROCKET
# =========================================================================
def render_whiteboard_scene4(t, duration=8.5):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(40, 40), (WIDTH - 40, HEIGHT - 40)], radius=24, outline=(225, 230, 238, 255), width=3)
    
    draw_whiteboard_header(draw, "THE BREAKTHROUGH", "THE CURVE GOES VERTICAL", "Day 300 to 365 = 80% Of All Returns", COLOR_EMERALD)
    
    origin_x, origin_y = 180, 1260
    max_x, min_y = WIDTH - 160, 560
    for gy in range(min_y, origin_y + 1, 140):
        draw.line([(origin_x, gy), (max_x, gy)], fill=(228, 234, 244, 255), width=2)
    for gx in range(origin_x, max_x + 1, 140):
        draw.line([(gx, min_y), (gx, origin_y)], fill=(228, 234, 244, 255), width=2)
    draw_hand_drawn_line(draw, [(origin_x, min_y), (origin_x, origin_y), (max_x, origin_y)], COLOR_INK_BLACK, width=7)
    
    base_y = origin_y - 180
    draw.line([(origin_x, base_y), (max_x - 100, base_y)], fill=(160, 172, 190, 255), width=3)
    
    growth_pts = []
    prog = min(1.0, t / 4.5)
    steps = int(prog * 25)
    for step in range(steps + 1):
        ratio = step / 24.0
        x = origin_x + int(ratio * 700)
        growth = (math.exp(2.8 * ratio) - 1.0) / (math.exp(2.8) - 1.0)
        y = int(base_y - growth * (base_y - min_y - 40))
        growth_pts.append((x, y))
        
    if len(growth_pts) > 1:
        draw_hand_drawn_line(draw, growth_pts, COLOR_EMERALD, width=10)
        draw_marker_pen(draw, growth_pts[-1][0], growth_pts[-1][1], angle_deg=-45, color=COLOR_EMERALD)
        
    if len(growth_pts) > 15:
        peak_x = growth_pts[-1][0]
        peak_y = growth_pts[-1][1]
        draw_pill_badge(draw, peak_x - 120, peak_y - 85, "+37.8x GAIN", get_font(34), (255, 255, 255, 255), COLOR_EMERALD, (5, 150, 100, 255), padding_x=22, height=54)
        
    draw_whiteboard_stickman(draw, 340, 1580, pose="pointing_up", scale=1.35, color=COLOR_INK_BLACK)
    
    draw_bottom_caption_bar(draw, "ONCE THE INFLECTION HITS, RETURNS EXPLODE VERTICALLY", COLOR_EMERALD)
    return img

# =========================================================================
# SCENE 5: THE CROWD vs THE TOP 1%
# =========================================================================
def render_whiteboard_scene5(t, duration=8.5):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(40, 40), (WIDTH - 40, HEIGHT - 40)], radius=24, outline=(225, 230, 238, 255), width=3)
    
    draw_whiteboard_header(draw, "THE DIVERGENCE", "THE HAMSTER WHEEL vs WEALTH", "Where Most Get Trapped Forever", COLOR_COBALT)
    
    draw.line([(WIDTH // 2, 450), (WIDTH // 2, 1600)], fill=(215, 222, 235, 255), width=4)
    
    draw.rounded_rectangle([(100, 480), (WIDTH // 2 - 40, 540)], radius=12, fill=COLOR_CRIMSON_BG, outline=COLOR_CRIMSON, width=2)
    draw_centered_text(draw, (100 + WIDTH // 2 - 40) // 2, 495, "99% DOPAMINE CHASER", get_font(24), COLOR_CRIMSON)
    
    draw.rounded_rectangle([(WIDTH // 2 + 40, 480), (WIDTH - 100, 540)], radius=12, fill=COLOR_EMERALD_BG, outline=COLOR_EMERALD, width=2)
    draw_centered_text(draw, (WIDTH // 2 + 40 + WIDTH - 100) // 2, 495, "1% COMPOUND BUILDER", get_font(24), COLOR_EMERALD)
    
    draw_hamster_wheel_crowd(draw, 340, 1200, progress=t)
    draw.text((120, 1340), "- Resets every 90 days", fill=COLOR_CRIMSON, font=get_font(24))
    draw.text((120, 1380), "- Chases shiny objects", fill=COLOR_CRIMSON, font=get_font(24))
    
    tree_x = 760
    tree_base_y = 1250
    draw_hand_drawn_line(draw, [(tree_x, tree_base_y), (tree_x, tree_base_y - 220)], COLOR_INK_BLACK, width=12)
    draw.line([(tree_x, tree_base_y - 120), (tree_x - 60, tree_base_y - 180)], fill=COLOR_INK_BLACK, width=7)
    draw.line([(tree_x, tree_base_y - 150), (tree_x + 70, tree_base_y - 210)], fill=COLOR_INK_BLACK, width=7)
    draw.ellipse([(tree_x - 110, tree_base_y - 340), (tree_x + 110, tree_base_y - 180)], fill=COLOR_EMERALD_BG, outline=COLOR_EMERALD, width=4)
    draw.text((tree_x - 20, tree_base_y - 280), "$$$", fill=COLOR_AMBER, font=get_font(36))
    
    draw_whiteboard_stickman(draw, tree_x - 150, tree_base_y, pose="confident_arms_crossed", scale=1.1, color=COLOR_INK_BLACK)
    draw.text((WIDTH // 2 + 80, 1340), "+ Endures the boring flatline", fill=COLOR_EMERALD, font=get_font(24))
    draw.text((WIDTH // 2 + 80, 1380), "+ Owns compounding assets", fill=COLOR_EMERALD, font=get_font(24))
    
    draw_bottom_caption_bar(draw, "THE CROWD CHASES DOPAMINE. THE TOP 1% EMBRACE BOREDOM.", COLOR_COBALT)
    return img

# =========================================================================
# SCENE 6: THE RULE & THE INFINITE LOOP
# =========================================================================
def render_whiteboard_scene6(t, duration=8.0):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(40, 40), (WIDTH - 40, HEIGHT - 40)], radius=24, outline=(225, 230, 238, 255), width=3)
    
    draw_whiteboard_header(draw, "THE GOLDEN TAKEAWAY", "SURVIVE THE FLATLINE", "The Math Never Lies", COLOR_AMBER)
    
    board_w = 860
    board_h = 420
    board_x = WIDTH // 2 - board_w // 2
    board_y = 520
    draw.rounded_rectangle([(board_x, board_y), (board_x + board_w, board_y + board_h)], radius=22, fill=COLOR_WB_CARD, outline=COLOR_INK_BLACK, width=4)
    
    draw.text((board_x + 60, board_y + 60), "1.01", fill=COLOR_EMERALD, font=get_font(72))
    draw.text((board_x + 220, board_y + 40), "365", fill=COLOR_EMERALD, font=get_font(38))
    draw.text((board_x + 300, board_y + 60), "=  37.78", fill=COLOR_EMERALD, font=get_font(72))
    draw.text((board_x + 620, board_y + 80), "(+3,778%)", fill=COLOR_EMERALD, font=get_font(32))
    
    draw.line([(board_x + 40, board_y + 200), (board_x + board_w - 40, board_y + 200)], fill=(225, 230, 240, 255), width=2)
    draw.text((board_x + 60, board_y + 250), "0.99", fill=COLOR_CRIMSON, font=get_font(72))
    draw.text((board_x + 220, board_y + 230), "365", fill=COLOR_CRIMSON, font=get_font(38))
    draw.text((board_x + 300, board_y + 250), "=  0.03", fill=COLOR_CRIMSON, font=get_font(72))
    draw.text((board_x + 620, board_y + 270), "(-97%)", fill=COLOR_CRIMSON, font=get_font(32))
    
    draw_whiteboard_stickman(draw, WIDTH // 2, 1480, pose="pointing_viewer", scale=1.45, color=COLOR_INK_BLACK)
    
    draw_pill_badge(draw, WIDTH // 2, 1020, "REFUSE TO QUIT DURING THE FLATLINE", get_font(32), (180, 83, 9, 255), COLOR_AMBER_BG, COLOR_AMBER, padding_x=32, height=62)
    
    draw_bottom_caption_bar(draw, "BECAUSE IF YOU GET 1% BETTER EVERY SINGLE DAY...", COLOR_COBALT)
    return img

def render_whiteboard_frame(scene_idx, t, duration):
    if scene_idx == 1:
        return render_whiteboard_scene1(t, duration)
    elif scene_idx == 2:
        return render_whiteboard_scene2(t, duration)
    elif scene_idx == 3:
        return render_whiteboard_scene3(t, duration)
    elif scene_idx == 4:
        return render_whiteboard_scene4(t, duration)
    elif scene_idx == 5:
        return render_whiteboard_scene5(t, duration)
    elif scene_idx == 6:
        return render_whiteboard_scene6(t, duration)
    return render_whiteboard_scene1(t, duration)

def render_whiteboard_short(output_path, total_duration_sec=51.5):
    """Renders the complete 6-scene whiteboard video directly through an FFmpeg pipe."""
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    total_frames = int(total_duration_sec * FPS)
    scene_dur = total_duration_sec / 6.0
    
    print(f"\n[Whiteboard Engine] Rendering {total_duration_sec:.1f}s ({total_frames} frames @ {FPS} fps)")
    print(f"[Whiteboard Engine] Destination: {output_path}")
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for frame_idx in range(total_frames):
        t_global = frame_idx / FPS
        scene_idx = min(6, int(t_global / scene_dur) + 1)
        t_scene = t_global - (scene_idx - 1) * scene_dur
        
        img = render_whiteboard_frame(scene_idx, t_scene, scene_dur)
        rgb_data = img.convert("RGB").tobytes()
        proc.stdin.write(rgb_data)
        
        if frame_idx % 150 == 0:
            pct = (frame_idx / total_frames) * 100
            print(f"[Whiteboard Render] Frame {frame_idx}/{total_frames} ({pct:.1f}%) | Scene {scene_idx}")
            
    proc.stdin.close()
    proc.wait()
    print(f"[Whiteboard Engine] Video successfully rendered to: {output_path}")

if __name__ == "__main__":
    out_dir = Path("C:/Users/Arnav112/.gemini/antigravity-ide/brain/3aeee31a-0a79-4162-a09a-0ee01f84f16c/scratch")
    out_dir.mkdir(exist_ok=True)
    for s in range(1, 7):
        frame = render_whiteboard_frame(s, t=4.5, duration=8.5)
        rgb = frame.convert("RGB")
        frame_path = out_dir / f"wb_scene{s}.jpg"
        rgb.save(frame_path, quality=95)
        print(f"[OK] Scene {s} saved: {frame_path}")
