import math
import random
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Institutional Financial Palette (Clean, High-Contrast Whiteboard)
COLOR_WB_BG = (247, 249, 252, 255)       # Premium crisp vellum canvas
COLOR_WB_CARD = (255, 255, 255, 255)     # Opaque white card fill
COLOR_WB_BORDER = (220, 226, 236, 255)   # Technical card stroke
COLOR_INK_BLACK = (18, 24, 38, 255)      # Charcoal dry-erase black
COLOR_INK_MUTED = (95, 110, 132, 255)    # Financial sub-label slate
COLOR_GRID_LINE = (230, 236, 245, 255)   # Subtle accounting ledger grid

COLOR_EMERALD = (16, 185, 129, 255)      # Wealth / Positive ROI green
COLOR_EMERALD_BG = (236, 253, 245, 255)  # Soft mint fill
COLOR_EMERALD_BORDER = (167, 243, 208, 255)

COLOR_CRIMSON = (239, 68, 68, 255)       # Loss / Decay / Trap red
COLOR_CRIMSON_BG = (254, 242, 242, 255)  # Soft crimson fill
COLOR_CRIMSON_BORDER = (254, 202, 202, 255)

COLOR_COBALT = (37, 99, 235, 255)        # Principal / Linear benchmark blue
COLOR_COBALT_BG = (239, 246, 255, 255)   # Soft blue fill
COLOR_COBALT_BORDER = (191, 219, 254, 255)

COLOR_AMBER = (217, 119, 6, 255)         # Multiplier / Inflection gold
COLOR_AMBER_BG = (254, 243, 199, 255)    # Soft gold fill
COLOR_AMBER_BORDER = (253, 230, 138, 255)

# Premium Font Scale (Segoe UI Bold / Arial Bold)
def get_font(size):
    for font_name in ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf", "tahomabd.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return ImageFont.load_default()

FONT_TINY = get_font(18)
FONT_MICRO = get_font(22)
FONT_BADGE = get_font(26)
FONT_BODY = get_font(26)
FONT_SUB = get_font(30)
FONT_STAT_MD = get_font(38)
FONT_STAT_LG = get_font(48)
FONT_TITLE = get_font(56)
FONT_HERO = get_font(68)

def draw_centered_text(draw, cx, y, text, font, fill):
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, y), text, fill=fill, font=font)
    return w

def draw_pill_badge(draw, cx, y, text, font, text_color, fill_color, outline_color, padding_x=28, height=52, radius=14):
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    box_w = min(940, w + padding_x * 2)
    x1 = cx - box_w // 2
    x2 = x1 + box_w
    draw.rounded_rectangle([(x1, y), (x2, y + height)], radius=radius, fill=fill_color, outline=outline_color, width=2)
    draw_centered_text(draw, cx, y + (height - (bbox[3] - bbox[1])) // 2 - 2, text, font, text_color)
    return box_w

def draw_hand_drawn_line(draw, points, color, width=6, jitter=1.2, seed=42):
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
    rad = math.radians(angle_deg)
    pen_len = 135
    pen_w = 22
    dx = math.cos(rad)
    dy = math.sin(rad)
    nx = -dy
    ny = dx
    nib_len = 18
    nib_base_x = tip_x - dx * nib_len
    nib_base_y = tip_y - dy * nib_len
    
    # Nib
    draw.polygon([
        (tip_x, tip_y),
        (nib_base_x + nx * (pen_w * 0.35), nib_base_y + ny * (pen_w * 0.35)),
        (nib_base_x - nx * (pen_w * 0.35), nib_base_y - ny * (pen_w * 0.35))
    ], fill=color)
    
    # Grip
    grip_len = 34
    grip_end_x = nib_base_x - dx * grip_len
    grip_end_y = nib_base_y - dy * grip_len
    draw.polygon([
        (nib_base_x + nx * (pen_w * 0.45), nib_base_y - ny * (pen_w * 0.45)),
        (nib_base_x - nx * (pen_w * 0.45), nib_base_y - ny * (pen_w * 0.45)),
        (grip_end_x - nx * (pen_w * 0.5), grip_end_y - ny * (pen_w * 0.5)),
        (grip_end_x + nx * (pen_w * 0.5), grip_end_y + ny * (pen_w * 0.5))
    ], fill=(42, 48, 60, 255))
    
    # Barrel
    body_end_x = grip_end_x - dx * (pen_len - grip_len - nib_len)
    body_end_y = grip_end_y - dy * (pen_len - grip_len - nib_len)
    draw.polygon([
        (grip_end_x + nx * (pen_w * 0.5), grip_end_y - ny * (pen_w * 0.5)),
        (grip_end_x - nx * (pen_w * 0.5), grip_end_y - ny * (pen_w * 0.5)),
        (body_end_x - nx * (pen_w * 0.5), body_end_y - ny * (pen_w * 0.5)),
        (body_end_x + nx * (pen_w * 0.5), body_end_y + ny * (pen_w * 0.5))
    ], fill=(244, 246, 250, 255), outline=(180, 190, 205, 255), width=2)
    
    # Accent ring
    band_start_x = grip_end_x - dx * 12
    band_start_y = grip_end_y - dy * 12
    band_end_x = band_start_x - dx * 14
    band_end_y = band_start_y - dy * 14
    draw.polygon([
        (band_start_x + nx * (pen_w * 0.5), band_start_y - ny * (pen_w * 0.5)),
        (band_start_x - nx * (pen_w * 0.5), band_start_y - ny * (pen_w * 0.5)),
        (band_end_x - nx * (pen_w * 0.5), band_end_y - ny * (pen_w * 0.5)),
        (band_end_x + nx * (pen_w * 0.5), band_end_y + ny * (pen_w * 0.5))
    ], fill=color)

def draw_whiteboard_header(draw, badge_text, title_text, sub_text, badge_color=COLOR_COBALT):
    """Unified Header Hierarchy: Category Pill -> Major Title -> Key Takeaway Subtitle"""
    pill_w = 480
    pill_h = 52
    pill_x = WIDTH // 2 - pill_w // 2
    pill_y = 120
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=14, fill=COLOR_COBALT_BG, outline=badge_color, width=2)
    draw_centered_text(draw, WIDTH // 2, pill_y + 12, badge_text, FONT_BADGE, badge_color)
    
    draw_centered_text(draw, WIDTH // 2, 198, title_text, FONT_TITLE, COLOR_INK_BLACK)
    
    sub_bbox = FONT_SUB.getbbox(sub_text)
    sub_w = sub_bbox[2] - sub_bbox[0]
    hl_y = 286
    draw.rounded_rectangle([(WIDTH // 2 - sub_w // 2 - 20, hl_y), (WIDTH // 2 + sub_w // 2 + 20, hl_y + 44)], radius=10, fill=COLOR_AMBER_BG, outline=COLOR_AMBER_BORDER, width=1)
    draw_centered_text(draw, WIDTH // 2, hl_y + 6, sub_text, FONT_SUB, COLOR_AMBER)

def draw_kpi_metric_strip(draw, y, col1, col2, col3):
    """Standardized 3-Column Institutional Financial Metric Strip"""
    card_w = 950
    card_h = 120
    card_x = WIDTH // 2 - card_w // 2
    draw.rounded_rectangle([(card_x, y), (card_x + card_w, y + card_h)], radius=18, fill=COLOR_WB_CARD, outline=COLOR_WB_BORDER, width=2)
    
    # Dividers
    draw.line([(card_x + 316, y + 18), (card_x + 316, y + card_h - 18)], fill=COLOR_WB_BORDER, width=2)
    draw.line([(card_x + 633, y + 18), (card_x + 633, y + card_h - 18)], fill=COLOR_WB_BORDER, width=2)
    
    columns = [
        (card_x + 20, col1),
        (card_x + 336, col2),
        (card_x + 653, col3),
    ]
    for start_x, (tag, val, delta, val_color, delta_color) in columns:
        draw.text((start_x + 15, y + 14), tag.upper(), fill=COLOR_INK_MUTED, font=FONT_TINY)
        draw.text((start_x + 15, y + 40), val, fill=val_color, font=FONT_STAT_MD)
        draw.text((start_x + 15, y + 86), delta, fill=delta_color, font=FONT_MICRO)

# =========================================================================
# SCENE 1: THE 37.8x PARADOX & INITIAL CAPITAL MATRIX
# =========================================================================
def render_whiteboard_scene1(t, duration=9.0):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(35, 35), (WIDTH - 35, HEIGHT - 35)], radius=24, outline=COLOR_WB_BORDER, width=3)
    
    draw_whiteboard_header(draw, "FINANCIAL MENTAL MODEL", "THE 1% COMPOUND LAW", "1.01^365 vs 0.99^365 Capital Simulation", COLOR_COBALT)
    
    # Standardized 3-Column Financial Metric Strip
    draw_kpi_metric_strip(draw, 355,
        ("Starting Principal", "$10,000", "Base Capital (1.00x)", COLOR_COBALT, COLOR_INK_MUTED),
        ("1% Daily Gain (+1.0%)", "$377,834", "+3,778% ROI (37.78x)", COLOR_EMERALD, COLOR_EMERALD),
        ("1% Daily Decay (-1.0%)", "$255", "-97.5% Loss (0.03x)", COLOR_CRIMSON, COLOR_CRIMSON)
    )
    
    # Institutional Chart Coordinates & Grid
    origin_x, origin_y = 150, 1420
    max_x, min_y = WIDTH - 100, 560
    
    # Grid lines with Currency Labels
    y_ticks = [
        ("$0", origin_y),
        ("$100K", origin_y - 220),
        ("$200K", origin_y - 440),
        ("$378K", min_y + 20)
    ]
    for label, gy in y_ticks:
        draw.line([(origin_x, gy), (max_x, gy)], fill=COLOR_GRID_LINE, width=2)
        draw.text((origin_x - 95, gy - 12), label, fill=COLOR_INK_MUTED, font=FONT_MICRO)
        
    for gx in range(origin_x, max_x + 1, 160):
        draw.line([(gx, min_y), (gx, origin_y)], fill=COLOR_GRID_LINE, width=2)
        
    # Main Axes
    draw_hand_drawn_line(draw, [(origin_x, min_y), (origin_x, origin_y), (max_x, origin_y)], COLOR_INK_BLACK, width=7)
    draw.polygon([(origin_x, min_y - 15), (origin_x - 12, min_y + 10), (origin_x + 12, min_y + 10)], fill=COLOR_INK_BLACK)
    draw.polygon([(max_x + 15, origin_y), (max_x - 10, origin_y - 12), (max_x - 10, origin_y + 12)], fill=COLOR_INK_BLACK)
    
    # Timeline x-axis markers
    for idx, (label, mult_label, pct) in enumerate([
        ("Day 0", "$10K", 0.0),
        ("Day 90", "$24.5K", 0.25),
        ("Day 180", "$60.0K", 0.50),
        ("Day 270", "$146.8K", 0.75),
        ("Day 365", "$377.8K", 1.0)
    ]):
        lx = origin_x + int(pct * (max_x - origin_x - 40))
        draw.line([(lx, origin_y), (lx, origin_y + 10)], fill=COLOR_INK_BLACK, width=3)
        draw.text((lx - 35, origin_y + 16), label, fill=COLOR_INK_BLACK, font=FONT_MICRO)
        draw.text((lx - 32, origin_y + 44), mult_label, fill=COLOR_INK_MUTED, font=FONT_TINY)
        
    # Baseline Capital Line ($10,000 Zero Growth)
    base_y = origin_y - 70
    draw.line([(origin_x, base_y), (max_x - 40, base_y)], fill=(180, 190, 205, 255), width=3)
    # Text positioned cleanly below the gray line so it never touches the blue line
    draw.text((origin_x + 25, base_y + 12), "Baseline Principal ($10,000 Zero Growth Benchmark)", fill=COLOR_INK_MUTED, font=FONT_MICRO)
    
    # Progressively drawn Flatline Trap (Day 1 - 180)
    flat_prog = min(1.0, t / 4.5)
    flat_len = int(flat_prog * 460)
    draw_hand_drawn_line(draw, [(origin_x, base_y - 25), (origin_x + flat_len, base_y - 35)], COLOR_COBALT, width=8)
    draw_marker_pen(draw, origin_x + flat_len, base_y - 35, angle_deg=-60, color=COLOR_COBALT)
    
    # Floating Institutional Highlight Badge
    draw_pill_badge(draw, WIDTH // 2, 1525, "DAY 1 TO 180: CAPITAL GAINS FEEL INVISIBLE (+$49,958 / 6.0x)", FONT_SUB, COLOR_AMBER, COLOR_AMBER_BG, COLOR_AMBER_BORDER, padding_x=32, height=60)
    draw_centered_text(draw, WIDTH // 2, 1612, "The initial 50% of the timeline only reveals 15% of the total payoff", FONT_BODY, COLOR_INK_MUTED)
    return img

# =========================================================================
# SCENE 2: THE VALLEY OF DISAPPOINTMENT & THE EXPECTATION GAP
# =========================================================================
def render_whiteboard_scene2(t, duration=9.0):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(35, 35), (WIDTH - 35, HEIGHT - 35)], radius=24, outline=COLOR_WB_BORDER, width=3)
    
    draw_whiteboard_header(draw, "THE COGNITIVE BIAS", "THE VALLEY OF DISAPPOINTMENT", "Why Linear Expectations Destroy Compounding", COLOR_CRIMSON)
    
    # Standardized 3-Column Financial Metric Strip
    draw_kpi_metric_strip(draw, 355,
        ("Linear Expectation", "$185,000", "Mental Target (Month 6)", COLOR_COBALT, COLOR_COBALT),
        ("Actual Result", "$59,958", "True Balance (Month 6)", COLOR_EMERALD, COLOR_INK_MUTED),
        ("Frustration Spread", "-$125,042", "Negative Expectation Gap", COLOR_CRIMSON, COLOR_CRIMSON)
    )
    
    # Graph Area
    origin_x, origin_y = 150, 1420
    max_x, min_y = WIDTH - 100, 560
    
    for gy in range(min_y, origin_y + 1, 140):
        draw.line([(origin_x, gy), (max_x, gy)], fill=COLOR_GRID_LINE, width=2)
    for gx in range(origin_x, max_x + 1, 160):
        draw.line([(gx, min_y), (gx, origin_y)], fill=COLOR_GRID_LINE, width=2)
    draw_hand_drawn_line(draw, [(origin_x, min_y), (origin_x, origin_y), (max_x, origin_y)], COLOR_INK_BLACK, width=7)
    
    base_y = origin_y - 20
    
    # Linear Expectation Line (Solid Blue)
    lin_end_x = max_x - 100
    lin_end_y = min_y + 60
    draw.line([(origin_x, base_y), (lin_end_x, lin_end_y)], fill=COLOR_COBALT, width=5)
    draw.text((lin_end_x - 250, lin_end_y + 85), "Linear ($185K Target)", fill=COLOR_COBALT, font=FONT_MICRO)
    
    # Compounding Reality Line (Curved slow start)
    reality_pts = []
    for step in range(25):
        ratio = step / 24.0
        x = origin_x + int(ratio * (lin_end_x - origin_x))
        curve = (math.exp(1.8 * ratio) - 1.0) / (math.exp(1.8) - 1.0)
        y = int(base_y - curve * (base_y - lin_end_y))
        reality_pts.append((x, y))
    draw_hand_drawn_line(draw, reality_pts, COLOR_EMERALD, width=4)
    draw.text((origin_x + 360, origin_y - 120), "Compounding Reality ($59,958 at Mo. 6)", fill=COLOR_EMERALD, font=FONT_MICRO)
    
    # Quitting Decay Curve (-1% daily drop when quitting at Month 3)
    decay_pts = []
    prog = min(1.0, t / 4.5)
    steps = int(prog * 25)
    for step in range(steps + 1):
        ratio = step / 24.0
        x = origin_x + int(ratio * 720)
        decay = math.exp(-2.6 * ratio)
        y = int(base_y - (1.0 - decay) * 260)
        decay_pts.append((x, y))
        
    if len(decay_pts) > 1:
        draw_hand_drawn_line(draw, decay_pts, COLOR_CRIMSON, width=8)
        draw_marker_pen(draw, decay_pts[-1][0], decay_pts[-1][1], angle_deg=-45, color=COLOR_CRIMSON)
        
    # Shaded Valley of Disappointment Region Card (Cleanly positioned in open upper-left quadrant)
    box_w = 500
    box_h = 160
    box_x = 175
    box_y = 560
    draw.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=18, fill=COLOR_WB_CARD, outline=COLOR_CRIMSON, width=3)
    draw_pill_badge(draw, box_x + box_w // 2, box_y + 16, "THE VALLEY OF DISAPPOINTMENT", FONT_TINY, COLOR_CRIMSON, COLOR_CRIMSON_BG, COLOR_CRIMSON_BORDER, padding_x=16, height=34)
    draw_centered_text(draw, box_x + box_w // 2, box_y + 64, "99% Quit In This Negative Spread", FONT_SUB, COLOR_INK_BLACK)
    draw_centered_text(draw, box_x + box_w // 2, box_y + 110, "Mental: $185K Target  vs  Reality: $60K", FONT_MICRO, COLOR_CRIMSON)
    
    # Downward pointer arrow towards the gap
    draw.polygon([(box_x + box_w // 2, box_y + box_h + 16), (box_x + box_w // 2 - 12, box_y + box_h), (box_x + box_w // 2 + 12, box_y + box_h)], fill=COLOR_CRIMSON)
    
    draw_pill_badge(draw, WIDTH // 2, 1525, "TRAP: LINEAR EFFORT PRODUCES BACK-LOADED REWARDS", FONT_SUB, COLOR_CRIMSON, COLOR_CRIMSON_BG, COLOR_CRIMSON_BORDER, padding_x=32, height=60)
    draw_centered_text(draw, WIDTH // 2, 1612, "Quitting at Month 3 resets all compounded interest back to zero", FONT_BODY, COLOR_INK_MUTED)
    return img

# =========================================================================
# SCENE 3: CRITICAL MASS & CAPITAL STACKING TABLE
# =========================================================================
def render_whiteboard_scene3(t, duration=9.0):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(35, 35), (WIDTH - 35, HEIGHT - 35)], radius=24, outline=COLOR_WB_BORDER, width=3)
    
    draw_whiteboard_header(draw, "KINETIC ACCELERATION", "THE CRITICAL MASS THRESHOLD", "Quarterly Capital Stacking & Milestone Analysis", COLOR_AMBER)
    
    # 4-Stage Capital Stacking Table with Mathematical Precision & Daily Yields
    table_y = 355
    table_w = 950
    table_x = WIDTH // 2 - table_w // 2
    card_h = 195
    gap_y = 30
    
    tiers = [
        ("STAGE 1: DAY 90 (MONTH 3)", "2.45x", "$24,486", "+$14,486 Gain (+145%)", "+$245 / Day", COLOR_INK_MUTED, (246, 248, 252, 255), COLOR_WB_BORDER),
        ("STAGE 2: DAY 180 (MONTH 6)", "6.00x", "$59,958", "+$49,958 Gain (+500%)", "+$600 / Day", COLOR_COBALT, COLOR_COBALT_BG, COLOR_COBALT_BORDER),
        ("STAGE 3: DAY 270 (MONTH 9)", "14.68x", "$146,815", "+$136,815 Gain (+1,368%)", "+$1,468 / Day", COLOR_AMBER, COLOR_AMBER_BG, COLOR_AMBER_BORDER),
        ("STAGE 4: DAY 365 (MONTH 12)", "37.78x", "$377,834", "+$367,834 Gain (+3,778%)", "+$3,778 / Day", COLOR_EMERALD, COLOR_EMERALD_BG, COLOR_EMERALD_BORDER),
    ]
    
    for idx, (tier_title, mult, capital, gain, daily_yield, color_accent, bg_color, border_color) in enumerate(tiers):
        ty = table_y + idx * (card_h + gap_y)
        draw.rounded_rectangle([(table_x, ty), (table_x + table_w, ty + card_h)], radius=18, fill=bg_color, outline=border_color, width=2)
        
        # Header Badge of the Stage
        draw_pill_badge(draw, table_x + 190, ty + 16, tier_title, FONT_TINY, color_accent, COLOR_WB_CARD, border_color, padding_x=16, height=34)
        
        # Big Multiple Stat
        draw.text((table_x + 40, ty + 78), mult, fill=color_accent, font=FONT_HERO)
        
        # Balance Figure
        draw.text((table_x + 280, ty + 70), "PORTFOLIO BALANCE:", fill=COLOR_INK_MUTED, font=FONT_TINY)
        draw.text((table_x + 280, ty + 96), capital, fill=COLOR_INK_BLACK, font=FONT_STAT_MD)
        
        # Net Gain Figure
        draw.text((table_x + 580, ty + 70), "NET COMPOUNDED GAIN:", fill=COLOR_INK_MUTED, font=FONT_TINY)
        draw.text((table_x + 580, ty + 96), gain, fill=color_accent, font=FONT_BODY)
        
        # Daily Interest Yield Pill Badge
        draw.rounded_rectangle([(table_x + 280, ty + 148), (table_x + table_w - 40, ty + 182)], radius=8, fill=COLOR_WB_CARD, outline=border_color, width=1)
        draw.text((table_x + 295, ty + 154), f"Autonomous Daily Cashflow Output:  {daily_yield} Yield", fill=COLOR_INK_BLACK, font=FONT_TINY)
        
    draw_pill_badge(draw, WIDTH // 2, 1490, "CRITICAL MASS INFLECTION: DAY 270 ($146,815 / 14.68x)", FONT_SUB, COLOR_EMERALD, COLOR_EMERALD_BG, COLOR_EMERALD_BORDER, padding_x=34, height=60)
    draw_centered_text(draw, WIDTH // 2, 1575, "Beyond Day 270, daily interest yield exceeds the original $10,000 principal", FONT_BODY, COLOR_INK_BLACK)
    return img

# =========================================================================
# SCENE 4: THE VERTICAL SKYROCKET (+3,778% ROI)
# =========================================================================
def render_whiteboard_scene4(t, duration=9.0):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(35, 35), (WIDTH - 35, HEIGHT - 35)], radius=24, outline=COLOR_WB_BORDER, width=3)
    
    draw_whiteboard_header(draw, "ASYMMETRIC HARVEST", "THE CURVE GOES VERTICAL", "83% Of Total Wealth Generated In Final 65 Days", COLOR_EMERALD)
    
    # Standardized 3-Column Financial Metric Strip
    draw_kpi_metric_strip(draw, 355,
        ("Initial Capital", "$10,000", "Baseline Principal", COLOR_INK_BLACK, COLOR_INK_MUTED),
        ("Final Balance", "$377,834", "+$367,834 Net Profit", COLOR_EMERALD, COLOR_EMERALD),
        ("Net Multiplier", "37.78x", "+3,778% Total ROI", COLOR_EMERALD, COLOR_EMERALD)
    )
    
    # Large Graph Arena - Ceiling at 640px leaves generous breathing room
    origin_x, origin_y = 150, 1420
    max_x, min_y = WIDTH - 100, 640
    
    y_ticks = [
        ("$0", origin_y),
        ("$100K", origin_y - 200),
        ("$200K", origin_y - 400),
        ("$378K", min_y + 20)
    ]
    for label, gy in y_ticks:
        draw.line([(origin_x, gy), (max_x, gy)], fill=COLOR_GRID_LINE, width=2)
        draw.text((origin_x - 95, gy - 12), label, fill=COLOR_INK_MUTED, font=FONT_MICRO)
        
    for gx in range(origin_x, max_x + 1, 160):
        draw.line([(gx, min_y), (gx, origin_y)], fill=COLOR_GRID_LINE, width=2)
    draw_hand_drawn_line(draw, [(origin_x, min_y), (origin_x, origin_y), (max_x, origin_y)], COLOR_INK_BLACK, width=7)
    
    # Timeline x-axis markers
    for idx, (label, mult_label, pct) in enumerate([
        ("Day 0", "$10K", 0.0),
        ("Day 90", "$24.5K", 0.25),
        ("Day 180", "$60.0K", 0.50),
        ("Day 270", "$146.8K", 0.75),
        ("Day 365", "$377.8K", 1.0)
    ]):
        lx = origin_x + int(pct * (max_x - origin_x - 40))
        draw.line([(lx, origin_y), (lx, origin_y + 10)], fill=COLOR_INK_BLACK, width=3)
        draw.text((lx - 35, origin_y + 16), label, fill=COLOR_INK_BLACK, font=FONT_MICRO)
        draw.text((lx - 32, origin_y + 44), mult_label, fill=COLOR_INK_MUTED, font=FONT_TINY)
        
    base_y = origin_y - 20
    draw.line([(origin_x, base_y), (max_x - 40, base_y)], fill=(180, 190, 205, 255), width=3)
    
    # Compounding green curve soaring into stratosphere
    growth_pts = []
    prog = min(1.0, t / 4.5)
    steps = int(prog * 25)
    for step in range(steps + 1):
        ratio = step / 24.0
        x = origin_x + int(ratio * 760)
        growth = (math.exp(2.8 * ratio) - 1.0) / (math.exp(2.8) - 1.0)
        y = int(base_y - growth * (base_y - min_y - 20))
        growth_pts.append((x, y))
        
    if len(growth_pts) > 1:
        draw_hand_drawn_line(draw, growth_pts, COLOR_EMERALD, width=12)
        draw_marker_pen(draw, growth_pts[-1][0], growth_pts[-1][1], angle_deg=-45, color=COLOR_EMERALD)
        
    # Peak callout banner (Positioned safely to the left of the peak)
    if len(growth_pts) > 15:
        peak_x = growth_pts[-1][0]
        peak_y = growth_pts[-1][1]
        draw_pill_badge(draw, peak_x - 240, peak_y + 35, "+37.8x ($377,834)", FONT_SUB, (255, 255, 255, 255), COLOR_EMERALD, (5, 140, 95, 255), padding_x=28, height=60)
        
    # Key Milestones along the curve
    if len(growth_pts) > 12:
        m1 = growth_pts[12]
        draw.ellipse([(m1[0] - 8, m1[1] - 8), (m1[0] + 8, m1[1] + 8)], fill=COLOR_EMERALD)
        draw.text((m1[0] - 40, m1[1] + 16), "Day 180: $60K (6.0x)", fill=COLOR_INK_MUTED, font=FONT_TINY)
    if len(growth_pts) > 18:
        m2 = growth_pts[18]
        draw.ellipse([(m2[0] - 8, m2[1] - 8), (m2[0] + 8, m2[1] + 8)], fill=COLOR_EMERALD)
        draw.text((m2[0] - 50, m2[1] + 16), "Day 270: $147K (14.7x)", fill=COLOR_INK_MUTED, font=FONT_TINY)
        
    draw_pill_badge(draw, WIDTH // 2, 1525, "DAY 300 TO 365 GENERATES 83% OF TOTAL ANNUAL WEALTH", FONT_SUB, COLOR_EMERALD, COLOR_EMERALD_BG, COLOR_EMERALD_BORDER, padding_x=32, height=60)
    draw_centered_text(draw, WIDTH // 2, 1612, "The patience tax is high, but the backend return is overwhelmingly asymmetric", FONT_BODY, COLOR_INK_BLACK)
    return img

# =========================================================================
# SCENE 5: THE 5-YEAR WEALTH DIVIDE (TWO BALANCE SHEETS)
# =========================================================================
def render_whiteboard_scene5(t, duration=9.0):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(35, 35), (WIDTH - 35, HEIGHT - 35)], radius=24, outline=COLOR_WB_BORDER, width=3)
    
    draw_whiteboard_header(draw, "5-YEAR WEALTH AUDIT", "THE 5-YEAR BALANCE SHEET", "Dopamine Chaser vs Disciplined Compounder", COLOR_COBALT)
    
    # Split Screen Columns with Institutional Layout
    col_w = 450
    y_top = 355
    y_bottom = 1450
    
    # LEFT COLUMN: THE 99% (DOPAMINE CHASER)
    col1_x = 65
    draw.rounded_rectangle([(col1_x, y_top), (col1_x + col_w, y_bottom)], radius=20, fill=COLOR_CRIMSON_BG, outline=COLOR_CRIMSON, width=3)
    draw_pill_badge(draw, col1_x + col_w // 2, y_top + 22, "THE 99% (DOPAMINE CHASER)", FONT_MICRO, COLOR_CRIMSON, COLOR_WB_CARD, COLOR_CRIMSON, padding_x=18, height=44)
    
    metrics_left = [
        ("Base Monthly Salary", "$5,000 / mo", False),
        ("Monthly Savings Rate", "0% ($0 Saved)", True),
        ("Yield Reinvestment", "0% (All Consumed)", True),
        ("Strategy Pivot Rate", "Every 60-90 Days", True),
        ("High-Interest Debt", "$18,500 Overhead", True),
        ("5-Year Net Equity", "$0 (Zero Net Worth)", True)
    ]
    for mi, (label, val, is_bad) in enumerate(metrics_left):
        my = y_top + 105 + mi * 135
        icon = "[X] " if is_bad else "    "
        draw.text((col1_x + 30, my), (icon + label).upper(), fill=COLOR_INK_MUTED, font=FONT_TINY)
        val_color = COLOR_CRIMSON if is_bad else COLOR_INK_BLACK
        draw.text((col1_x + 30, my + 30), val, fill=val_color, font=FONT_STAT_MD)
        if mi < len(metrics_left) - 1:
            draw.line([(col1_x + 25, my + 95), (col1_x + col_w - 25, my + 95)], fill=(245, 215, 215, 255), width=2)
            
    # RIGHT COLUMN: THE 1% (COMPOUND INVESTOR)
    col2_x = WIDTH - col_w - 65
    draw.rounded_rectangle([(col2_x, y_top), (col2_x + col_w, y_bottom)], radius=20, fill=COLOR_EMERALD_BG, outline=COLOR_EMERALD, width=3)
    draw_pill_badge(draw, col2_x + col_w // 2, y_top + 22, "THE 1% (COMPOUND INVESTOR)", FONT_MICRO, COLOR_EMERALD, COLOR_WB_CARD, COLOR_EMERALD, padding_x=18, height=44)
    
    metrics_right = [
        ("Base Monthly Salary", "$5,000 / mo", False),
        ("Monthly Savings Rate", "25% ($1,250 / mo)", True),
        ("Yield Reinvestment", "100% Reinvested", True),
        ("Strategy Pivot Rate", "0 (Boring Index Hold)", True),
        ("High-Interest Debt", "$0 (Debt Free)", True),
        ("5-Year Net Equity", "$103,450+ Net Worth", True)
    ]
    for mi, (label, val, is_good) in enumerate(metrics_right):
        my = y_top + 105 + mi * 135
        icon = "[OK] " if is_good else "     "
        draw.text((col2_x + 30, my), (icon + label).upper(), fill=COLOR_INK_MUTED, font=FONT_TINY)
        val_color = COLOR_EMERALD if is_good else COLOR_INK_BLACK
        draw.text((col2_x + 30, my + 30), val, fill=val_color, font=FONT_STAT_MD)
        if mi < len(metrics_right) - 1:
            draw.line([(col2_x + 25, my + 95), (col2_x + col_w - 25, my + 95)], fill=(210, 240, 225, 255), width=2)
            
    draw_pill_badge(draw, WIDTH // 2, 1525, "NET WEALTH DIVIDE: $103,450 FROM THE IDENTICAL INCOME", FONT_SUB, COLOR_COBALT, COLOR_COBALT_BG, COLOR_COBALT_BORDER, padding_x=32, height=60)
    draw_centered_text(draw, WIDTH // 2, 1612, "Wealth is rarely an income problem. It is an endurance problem.", FONT_BODY, COLOR_INK_BLACK)
    return img

# =========================================================================
# SCENE 6: THE GOLDEN MATH MATRIX (1,480x ADVANTAGE)
# =========================================================================
def render_whiteboard_scene6(t, duration=8.5):
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_WB_BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(35, 35), (WIDTH - 35, HEIGHT - 35)], radius=24, outline=COLOR_WB_BORDER, width=3)
    
    draw_whiteboard_header(draw, "MATHEMATICAL LAW", "THE POWER OF 365 DAYS", "The Complete Annual Compounding Matrix", COLOR_AMBER)
    
    # Grand Math Comparison Box
    box_w = 950
    box_h = 560
    box_x = WIDTH // 2 - box_w // 2
    box_y = 355
    draw.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=22, fill=COLOR_WB_CARD, outline=COLOR_INK_BLACK, width=3)
    
    # Row 1: 1% Better Daily
    draw.text((box_x + 50, box_y + 32), "1.01", fill=COLOR_EMERALD, font=FONT_HERO)
    draw.text((box_x + 195, box_y + 18), "365", fill=COLOR_EMERALD, font=FONT_MICRO)
    draw.text((box_x + 260, box_y + 32), "=  37.78x", fill=COLOR_EMERALD, font=FONT_HERO)
    draw.text((box_x + 610, box_y + 46), "(+3,778% GAIN)", fill=COLOR_EMERALD, font=FONT_SUB)
    draw.text((box_x + 50, box_y + 115), "Initial $10,000 Grows to $377,834 (+37.8x Multiplier)", fill=COLOR_INK_MUTED, font=FONT_BODY)
    
    draw.line([(box_x + 35, box_y + 168), (box_x + box_w - 35, box_y + 168)], fill=COLOR_WB_BORDER, width=2)
    
    # Row 2: Status Quo
    draw.text((box_x + 50, box_y + 198), "1.00", fill=COLOR_COBALT, font=FONT_HERO)
    draw.text((box_x + 195, box_y + 184), "365", fill=COLOR_COBALT, font=FONT_MICRO)
    draw.text((box_x + 260, box_y + 198), "=   1.00x", fill=COLOR_COBALT, font=FONT_HERO)
    draw.text((box_x + 610, box_y + 212), "(0% ZERO GROWTH)", fill=COLOR_COBALT, font=FONT_SUB)
    draw.text((box_x + 50, box_y + 280), "Initial $10,000 Unchanged (Lost to Inflation & Cost of Living)", fill=COLOR_INK_MUTED, font=FONT_BODY)
    
    draw.line([(box_x + 35, box_y + 332), (box_x + box_w - 35, box_y + 332)], fill=COLOR_WB_BORDER, width=2)
    
    # Row 3: 1% Worse Daily
    draw.text((box_x + 50, box_y + 362), "0.99", fill=COLOR_CRIMSON, font=FONT_HERO)
    draw.text((box_x + 195, box_y + 348), "365", fill=COLOR_CRIMSON, font=FONT_MICRO)
    draw.text((box_x + 260, box_y + 362), "=   0.03x", fill=COLOR_CRIMSON, font=FONT_HERO)
    draw.text((box_x + 610, box_y + 376), "(-97.5% EROSION)", fill=COLOR_CRIMSON, font=FONT_SUB)
    draw.text((box_x + 50, box_y + 444), "Initial $10,000 Decayed to $255 Left (-97.5% Capital Destruction)", fill=COLOR_INK_MUTED, font=FONT_BODY)
    
    # Multiplier Advantage Callout (Fits cleanly within bounds)
    draw_pill_badge(draw, WIDTH // 2, 960, "TOTAL DIVERGENCE: 1,480.7x ADVANTAGE (37.78x vs 0.03x)", FONT_SUB, COLOR_AMBER, COLOR_AMBER_BG, COLOR_AMBER_BORDER, padding_x=28, height=62)
    
    # Bottom Golden Takeaway Card
    takeaway_w = 950
    takeaway_h = 185
    takeaway_x = WIDTH // 2 - takeaway_w // 2
    takeaway_y = 1060
    draw.rounded_rectangle([(takeaway_x, takeaway_y), (takeaway_x + takeaway_w, takeaway_y + takeaway_h)], radius=20, fill=(18, 24, 38, 255), outline=COLOR_AMBER, width=3)
    
    draw_centered_text(draw, WIDTH // 2, takeaway_y + 24, "THE GOLDEN COMPOUNDING RULE", FONT_SUB, COLOR_AMBER)
    draw_centered_text(draw, WIDTH // 2, takeaway_y + 72, "\"SURVIVE THE FLATLINE TO EARN THE MULTIPLIER.\"", FONT_STAT_MD, (255, 255, 255, 255))
    draw_centered_text(draw, WIDTH // 2, takeaway_y + 126, "Boring consistency always beats flashes of erratic intensity.", FONT_BODY, (180, 195, 220, 255))
    
    # Secondary 3-Pillar Benchmark strip
    draw_pill_badge(draw, WIDTH // 2, 1285, "PRINCIPAL: $10,000  |  PATIENCE: 365 DAYS  |  PAYOFF: $377,834", FONT_BADGE, COLOR_COBALT, COLOR_COBALT_BG, COLOR_COBALT_BORDER, padding_x=28, height=52)
    
    draw_pill_badge(draw, WIDTH // 2, 1525, "THE SECRET: DURATION IN MARKET WINS OVER INTENSITY", FONT_SUB, COLOR_EMERALD, COLOR_EMERALD_BG, COLOR_EMERALD_BORDER, padding_x=32, height=60)
    draw_centered_text(draw, WIDTH // 2, 1612, "Start today. Endure the flatline. Let the math do the heavy lifting.", FONT_BODY, COLOR_INK_BLACK)
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

def render_whiteboard_short(output_path, total_duration_sec=56.0):
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    total_frames = int(total_duration_sec * FPS)
    scene_dur = total_duration_sec / 6.0
    
    print(f"\n[Whiteboard Engine] Rendering Data-Dense Whiteboard Short: {total_duration_sec:.1f}s ({total_frames} frames @ {FPS} fps)")
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
        
        if frame_idx % 200 == 0:
            pct = (frame_idx / total_frames) * 100
            print(f"[Whiteboard Render] Frame {frame_idx}/{total_frames} ({pct:.1f}%) | Scene {scene_idx}")
            
    proc.stdin.close()
    proc.wait()
    print(f"[Whiteboard Engine] Video successfully rendered to: {output_path}")

if __name__ == "__main__":
    out_dir = Path("C:/Users/Arnav112/.gemini/antigravity-ide/brain/3aeee31a-0a79-4162-a09a-0ee01f84f16c/scratch")
    out_dir.mkdir(exist_ok=True)
    for s in range(1, 7):
        frame = render_whiteboard_frame(s, t=4.5, duration=9.0)
        rgb = frame.convert("RGB")
        frame_path = out_dir / f"finance_scene{s}.jpg"
        rgb.save(frame_path, quality=95)
        print(f"[OK] Scene {s} (Finance Figures) saved: {frame_path}")
