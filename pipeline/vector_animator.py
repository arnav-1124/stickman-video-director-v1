import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1080
HEIGHT = 1920
FPS = 30
FLOOR_Y = 1420

# Premium Ink Noir & Dark Psychology Palette
COLOR_BG = (10, 11, 15, 255)
COLOR_WHITE = (245, 247, 250, 255)
COLOR_CYAN = (0, 240, 255, 255)
COLOR_CYAN_DIM = (0, 180, 200, 180)
COLOR_CRIMSON = (255, 45, 85, 255)
COLOR_CRIMSON_DIM = (200, 30, 65, 180)
COLOR_GOLD = (255, 215, 0, 255)
COLOR_GOLD_DIM = (200, 170, 0, 180)
COLOR_MUTED = (90, 95, 115, 255)
COLOR_CROWD = (55, 60, 78, 160)
COLOR_CARD_BG = (18, 20, 28, 230)

def get_font(size):
    for font_name in ["arialbd.ttf", "segoeuib.ttf", "consola.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return ImageFont.load_default()

FONT_MICRO = get_font(20)
FONT_BADGE = get_font(26)
FONT_QUOTE = get_font(32)
FONT_TITLE = get_font(38)
FONT_LARGE = get_font(52)
FONT_HUGE = get_font(90)

# Pre-computed volumetric spotlights (cached for high-FPS rendering)
_SPOTLIGHT_CACHE = {}

def get_volumetric_spotlight(color_rgba, apex_x, apex_y, base_x1, base_x2, base_y):
    key = (color_rgba, apex_x, apex_y, base_x1, base_x2, base_y)
    if key in _SPOTLIGHT_CACHE:
        return _SPOTLIGHT_CACHE[key]
    
    sw, sh = WIDTH // 4, HEIGHT // 4
    cone_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cone_img)
    
    sa_x, sa_y = apex_x // 4, apex_y // 4
    sb_x1, sb_x2, sb_y = base_x1 // 4, base_x2 // 4, base_y // 4
    
    cdraw.polygon([(sa_x, sa_y), (sb_x1, sb_y), (sb_x2, sb_y)], fill=color_rgba)
    cdraw.ellipse([(sb_x1, sb_y - 12), (sb_x2, sb_y + 12)], fill=color_rgba)
    
    cone_img = cone_img.filter(ImageFilter.GaussianBlur(8))
    full_cone = cone_img.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
    
    _SPOTLIGHT_CACHE[key] = full_cone
    return full_cone

def draw_vignette_and_floor(draw, progress=0.0):
    draw.line([(80, FLOOR_Y), (WIDTH - 80, FLOOR_Y)], fill=(32, 36, 48, 255), width=3)
    draw.line([(120, FLOOR_Y + 3), (WIDTH - 120, FLOOR_Y + 3)], fill=(18, 20, 28, 255), width=2)
    
    for i in range(22):
        px = int((i * 137.5 + progress * 20 * (1 + (i % 3))) % (WIDTH - 160) + 80)
        py = int((FLOOR_Y - 800 + i * 45 - progress * 15 * (1 + (i % 2))) % 750 + (FLOOR_Y - 800))
        alpha = int(40 + 35 * math.sin(progress * 3 + i))
        draw.ellipse([(px - 2, py - 2), (px + 2, py + 2)], fill=(200, 210, 230, alpha))

def draw_header_pill(draw, category, title, color_accent=COLOR_CYAN):
    full_text = f"{category} // {title}"
    bbox = FONT_BADGE.getbbox(full_text)
    tw = bbox[2] - bbox[0]
    pill_w = tw + 70
    pill_h = 56
    pill_x = WIDTH // 2 - pill_w // 2
    pill_y = 150
    
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=14, fill=COLOR_CARD_BG, outline=color_accent, width=2)
    draw.text((WIDTH // 2 - tw // 2, pill_y + 14), full_text, fill=color_accent, font=FONT_BADGE)

def draw_alan_becker_stickman(draw, x, y, pose="idle", progress=0.0, color=COLOR_WHITE, scale=1.0, facing=1):
    lw = max(4, int(8 * scale))
    
    head_r = int(38 * scale)
    head_cy = y - int(245 * scale)
    head_cx = x
    
    squash_y = 1.0
    squash_x = 1.0
    
    if pose == "flail":
        squash_y = 0.85 + 0.25 * math.sin(progress * 28)
        squash_x = 1.0 / math.sqrt(max(0.6, squash_y))
        head_cx += int(math.sin(progress * 35) * 12)
    elif pose == "recoil":
        squash_y = 0.88
        squash_x = 1.12
        head_cx -= int(facing * 30 * scale)
    elif pose == "ponder":
        head_cx += int(facing * 10 * scale)
    elif pose == "point_throw":
        head_cx += int(facing * 25 * scale)
    elif pose == "phone":
        head_cx += int(facing * 18 * scale)
        head_cy += int(14 * scale)
    elif pose == "smug":
        head_cy -= int(8 * scale)
        head_cx -= int(facing * 8 * scale)
    elif pose == "hunched_shame":
        head_cy += int(80 * scale)
        head_cx -= int(facing * 15 * scale)
    elif pose == "walk":
        bob = math.sin(progress * 12) * int(8 * scale)
        head_cy += bob
    elif pose == "arms_crossed":
        breathe = math.sin(progress * 3) * int(3 * scale)
        head_cy += breathe
        
    rx = int(head_r * squash_x)
    ry = int(head_r * squash_y)
    
    draw.ellipse([(head_cx - rx, head_cy - ry), (head_cx + rx, head_cy + ry)], outline=color, width=lw)
    
    neck_x = head_cx
    neck_y = head_cy + ry
    pelvis_y = y - int(105 * scale)
    pelvis_x = x
    
    if pose == "flail":
        pelvis_x += int(math.sin(progress * 25) * 16)
        pelvis_y += int(15 * scale)
    elif pose == "recoil":
        pelvis_x -= int(facing * 45 * scale)
        pelvis_y += int(30 * scale)
    elif pose == "point_throw":
        pelvis_x -= int(facing * 20 * scale)
    elif pose == "phone":
        pelvis_x -= int(facing * 10 * scale)
    elif pose == "smug":
        pelvis_x += int(facing * 12 * scale)
    elif pose == "hunched_shame":
        pelvis_y += int(60 * scale)
        pelvis_x -= int(facing * 10 * scale)
    elif pose == "ponder":
        pelvis_x -= int(facing * 15 * scale)
    elif pose == "walk":
        pelvis_y += math.sin(progress * 12) * int(8 * scale)
        pelvis_x += int(facing * 10 * scale)
        
    draw.line([(neck_x, neck_y), (pelvis_x, pelvis_y)], fill=color, width=lw)
    
    shoulder_y = neck_y + int(18 * scale)
    shoulder_x = neck_x
    
    # Arms posing
    if pose == "arms_crossed":
        arm_span = int(45 * scale)
        elbow_drop = int(38 * scale)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - arm_span, shoulder_y + elbow_drop)], fill=color, width=lw)
        draw.line([(shoulder_x - arm_span, shoulder_y + elbow_drop), (shoulder_x + int(35 * scale), shoulder_y + elbow_drop + int(5 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x + arm_span, shoulder_y + elbow_drop)], fill=color, width=lw)
        draw.line([(shoulder_x + arm_span, shoulder_y + elbow_drop), (shoulder_x - int(35 * scale), shoulder_y + elbow_drop + int(5 * scale))], fill=color, width=lw)
        
    elif pose == "smug":
        hip_drop = int(55 * scale)
        elbow_flare = int(50 * scale)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - elbow_flare, shoulder_y + int(hip_drop * 0.5))], fill=color, width=lw)
        draw.line([(shoulder_x - elbow_flare, shoulder_y + int(hip_drop * 0.5)), (pelvis_x - int(20 * scale), pelvis_y)], fill=color, width=lw)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x + elbow_flare, shoulder_y + int(hip_drop * 0.5))], fill=color, width=lw)
        draw.line([(shoulder_x + elbow_flare, shoulder_y + int(hip_drop * 0.5)), (pelvis_x + int(20 * scale), pelvis_y)], fill=color, width=lw)
        
    elif pose == "phone":
        # Holding glowing phone in front of chest, head tilted down
        hand_x = shoulder_x + int(facing * 40 * scale)
        hand_y = shoulder_y + int(30 * scale)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x + int(facing * 20 * scale), shoulder_y + int(45 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x + int(facing * 20 * scale), shoulder_y + int(45 * scale)), (hand_x, hand_y)], fill=color, width=lw)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - int(facing * 15 * scale), shoulder_y + int(45 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x - int(facing * 15 * scale), shoulder_y + int(45 * scale)), (hand_x, hand_y)], fill=color, width=lw)
        # Glowing cyan phone screen
        draw.rounded_rectangle([(hand_x - 3, hand_y - 12), (hand_x + 9, hand_y + 12)], radius=2, fill=COLOR_CYAN)
        
    elif pose == "point_throw":
        draw.line([(shoulder_x, shoulder_y), (shoulder_x + int(facing * 60 * scale), shoulder_y - int(10 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x + int(facing * 60 * scale), shoulder_y - int(10 * scale)), (shoulder_x + int(facing * 110 * scale), shoulder_y - int(15 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - int(facing * 45 * scale), shoulder_y + int(45 * scale))], fill=color, width=lw)
        
    elif pose == "ponder":
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - int(35 * scale * facing), shoulder_y + int(45 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x - int(35 * scale * facing), shoulder_y + int(45 * scale)), (shoulder_x + int(20 * scale * facing), shoulder_y + int(50 * scale))], fill=color, width=lw)
        elbow_x = shoulder_x + int(25 * scale * facing)
        elbow_y = shoulder_y + int(48 * scale)
        draw.line([(shoulder_x, shoulder_y), (elbow_x, elbow_y)], fill=color, width=lw)
        draw.line([(elbow_x, elbow_y), (head_cx + int(facing * 20 * scale), head_cy + int(ry * 0.8))], fill=color, width=lw)
        
    elif pose == "shield":
        arm_fwd_x = shoulder_x + int(facing * 75 * scale)
        arm_fwd_y = shoulder_y - int(5 * scale)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x + int(facing * 40 * scale), shoulder_y - int(15 * scale))], fill=COLOR_CYAN, width=lw)
        draw.line([(shoulder_x + int(facing * 40 * scale), shoulder_y - int(15 * scale)), (arm_fwd_x, arm_fwd_y)], fill=COLOR_CYAN, width=lw)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - int(facing * 40 * scale), shoulder_y + int(45 * scale))], fill=color, width=lw)
        
    elif pose == "hunched_shame":
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - int(30 * scale), shoulder_y + int(35 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x - int(30 * scale), shoulder_y + int(35 * scale)), (head_cx, head_cy + int(10 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x + int(30 * scale), shoulder_y + int(35 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x + int(30 * scale), shoulder_y + int(35 * scale)), (head_cx, head_cy + int(10 * scale))], fill=color, width=lw)
        
    elif pose == "flail":
        f_l_x = shoulder_x - int(60 * scale)
        f_l_y = shoulder_y - int(30 * scale) + int(math.sin(progress * 30) * 45)
        f_r_x = shoulder_x + int(60 * scale)
        f_r_y = shoulder_y - int(30 * scale) - int(math.cos(progress * 30) * 45)
        draw.line([(shoulder_x, shoulder_y), (f_l_x, f_l_y)], fill=color, width=lw)
        draw.line([(f_l_x, f_l_y), (f_l_x - int(40 * scale), f_l_y - int(45 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x, shoulder_y), (f_r_x, f_r_y)], fill=color, width=lw)
        draw.line([(f_r_x, f_r_y), (f_r_x + int(40 * scale), f_r_y - int(45 * scale))], fill=color, width=lw)
        
    elif pose == "recoil":
        h_l_x = shoulder_x - int(facing * 35 * scale)
        h_l_y = shoulder_y - int(25 * scale)
        draw.line([(shoulder_x, shoulder_y), (h_l_x, h_l_y)], fill=color, width=lw)
        draw.line([(h_l_x, h_l_y), (h_l_x - int(facing * 30 * scale), h_l_y - int(30 * scale))], fill=color, width=lw)
        
    elif pose == "walk":
        arm_sway = math.sin(progress * 12) * int(40 * scale)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - arm_sway, shoulder_y + int(65 * scale))], fill=color, width=lw)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x + arm_sway, shoulder_y + int(65 * scale))], fill=color, width=lw)
        
    else: # idle
        breathe = math.sin(progress * 3) * int(5 * scale)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x - int(32 * scale), shoulder_y + int(70 * scale) + breathe)], fill=color, width=lw)
        draw.line([(shoulder_x, shoulder_y), (shoulder_x + int(32 * scale), shoulder_y + int(70 * scale) + breathe)], fill=color, width=lw)
        
    # Legs & Feet
    knee_l_x = pelvis_x - int(28 * scale)
    knee_r_x = pelvis_x + int(28 * scale)
    knee_y = pelvis_y + int(55 * scale)
    foot_l_x = pelvis_x - int(42 * scale)
    foot_r_x = pelvis_x + int(42 * scale)
    foot_l_y = y
    foot_r_y = y
    
    if pose == "walk":
        stride_phase = progress * 12
        stride_l = math.sin(stride_phase) * int(45 * scale)
        stride_r = -stride_l
        foot_l_x = pelvis_x + int(stride_l * facing)
        foot_r_x = pelvis_x + int(stride_r * facing)
        foot_l_y = y - max(0, int(math.cos(stride_phase) * 22 * scale))
        foot_r_y = y - max(0, int(-math.cos(stride_phase) * 22 * scale))
        knee_l_x = (pelvis_x + foot_l_x) // 2 + int(facing * 15 * scale)
        knee_r_x = (pelvis_x + foot_r_x) // 2 + int(facing * 15 * scale)
    elif pose == "hunched_shame":
        knee_l_x = pelvis_x - int(45 * scale)
        knee_r_x = pelvis_x + int(45 * scale)
        knee_y = y - int(25 * scale)
        foot_l_y = y
        foot_r_y = y
    elif pose == "point_throw":
        foot_l_x = pelvis_x + int(facing * 55 * scale)
        foot_r_x = pelvis_x - int(facing * 45 * scale)
        knee_l_x = (pelvis_x + foot_l_x) // 2
        knee_r_x = (pelvis_x + foot_r_x) // 2
    elif pose == "recoil":
        knee_l_x -= int(facing * 20 * scale)
        knee_r_x -= int(facing * 20 * scale)
        foot_l_x -= int(facing * 35 * scale)
        foot_r_x -= int(facing * 15 * scale)
        knee_y += int(15 * scale)
    elif pose == "flail":
        knee_l_x -= int(35 * scale)
        knee_r_x += int(35 * scale)
        knee_y += int(20 * scale)
        foot_l_x -= int(65 * scale)
        foot_r_x += int(65 * scale)
        
    draw.line([(pelvis_x, pelvis_y), (knee_l_x, knee_y)], fill=color, width=lw)
    draw.line([(knee_l_x, knee_y), (foot_l_x, foot_l_y)], fill=color, width=lw)
    draw.line([(foot_l_x, foot_l_y), (foot_l_x + int(facing * 22 * scale), foot_l_y)], fill=color, width=lw)
    
    draw.line([(pelvis_x, pelvis_y), (knee_r_x, knee_y)], fill=color, width=lw)
    draw.line([(knee_r_x, knee_y), (foot_r_x, foot_r_y)], fill=color, width=lw)
    draw.line([(foot_r_x, foot_r_y), (foot_r_x + int(facing * 22 * scale), foot_r_y)], fill=color, width=lw)

# =============================================================================
# FLEXIBLE CROWD ENGINE (Supports 1 Person, 2 Persons, or a Full Crowd)
# =============================================================================
def draw_crowd(draw, y=FLOOR_Y, count=8, x_min=120, x_max=960, style="phone", progress=0.0, base_scale=0.75):
    """
    Renders a crowd of stick figures with depth layering (back row / front row),
    supporting various crowd attitudes: 'phone', 'staring', 'pointing', 'walking'.
    """
    step = (x_max - x_min) / max(1, count - 1)
    for i in range(count):
        cx = int(x_min + i * step + math.sin(i * 1.7) * 12)
        # Depth alternation: even = background layer, odd = midground
        is_bg = (i % 2 == 0)
        c_scale = base_scale * (0.82 if is_bg else 0.95)
        cy = y - (12 if is_bg else 0)
        c_alpha = 110 if is_bg else 170
        crowd_color = (75, 82, 105, c_alpha)
        
        # Center-facing orientation
        facing_dir = -1 if cx > WIDTH // 2 else 1
        
        if style == "phone":
            draw_alan_becker_stickman(draw, cx, cy, pose="phone", progress=progress + i * 0.4, color=crowd_color, scale=c_scale, facing=facing_dir)
        elif style == "pointing":
            draw_alan_becker_stickman(draw, cx, cy, pose="point_throw", progress=progress + i * 0.2, color=crowd_color, scale=c_scale, facing=facing_dir)
        elif style == "staring":
            draw_alan_becker_stickman(draw, cx, cy, pose="idle", progress=progress + i * 0.3, color=crowd_color, scale=c_scale, facing=facing_dir)
        elif style == "walk":
            draw_alan_becker_stickman(draw, cx, cy, pose="walk", progress=progress + i * 0.8, color=crowd_color, scale=c_scale, facing=1)

def render_frame_at_time(t, frame_idx=0):
    frame = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(frame)
    draw_vignette_and_floor(draw, progress=t)
    
    # =========================================================================
    # SCENE 1 (0.0s - 7.5s): DUAL CONFRONTATION (ATTACKER THROWS -> HERO SHIELDS)
    # =========================================================================
    if t < 7.5:
        spotlight = get_volumetric_spotlight((0, 240, 255, 14), 420, 0, 140, 720, FLOOR_Y)
        frame.alpha_composite(spotlight)
        draw = ImageDraw.Draw(frame)
        
        draw_header_pill(draw, "01", "THE LAW OF SILENCE", COLOR_CYAN)
        
        # PROTAGONIST (Person B) on left
        is_shielded = (t >= 3.6)
        draw_alan_becker_stickman(
            draw, 380, FLOOR_Y,
            pose="shield" if is_shielded else "arms_crossed",
            progress=t,
            color=COLOR_WHITE,
            scale=1.1,
            facing=1
        )
        
        # ATTACKER (Aggressor) on right
        attacker_pose = "point_throw" if (2.6 <= t < 4.2) else ("recoil" if t >= 4.2 else "idle")
        draw_alan_becker_stickman(
            draw, 880, FLOOR_Y,
            pose=attacker_pose,
            progress=t,
            color=COLOR_CRIMSON,
            scale=1.05,
            facing=-1
        )
        
        # Attack Projectile hurled by Attacker (2.8s -> 4.2s)
        if 2.8 <= t < 4.2:
            p = (t - 2.8) / 1.4
            missile_x = int(840 - p * (840 - 480))
            missile_y = FLOOR_Y - 240
            draw.line([(missile_x + 80, missile_y), (missile_x, missile_y)], fill=COLOR_CRIMSON, width=10)
            draw.polygon([(missile_x, missile_y - 18), (missile_x - 30, missile_y), (missile_x, missile_y + 18)], fill=COLOR_CRIMSON)
            for pi in range(5):
                fx = missile_x + 90 + pi * 16
                fy = missile_y + int(math.sin(t * 30 + pi) * 10)
                draw.ellipse([(fx - 4, fy - 4), (fx + 4, fy + 4)], fill=COLOR_CRIMSON_DIM)
            draw.text((missile_x + 10, missile_y - 55), "INSULT", fill=COLOR_CRIMSON, font=FONT_BADGE)
            
        # Glowing Cyan Energy Barrier pops up at 3.6s
        if t >= 3.6:
            shield_cx = 480
            shield_cy = FLOOR_Y - 240
            draw.arc([(shield_cx - 40, shield_cy - 200), (shield_cx + 40, shield_cy + 200)], start=-80, end=80, fill=COLOR_CYAN, width=8)
            draw.arc([(shield_cx - 55, shield_cy - 215), (shield_cx + 25, shield_cy + 215)], start=-75, end=75, fill=(0, 240, 255, 90), width=4)
            
        # Shattering impact & spark explosion at 4.2s -> 7.5s
        if t >= 4.2:
            dt = t - 4.2
            impact_x = 480
            impact_y = FLOOR_Y - 240
            if dt < 1.0:
                ring_r = int(dt * 240)
                ring_alpha = int(max(0, 255 * (1.0 - dt)))
                draw.ellipse([(impact_x - ring_r, impact_y - ring_r), (impact_x + ring_r, impact_y + ring_r)], outline=(0, 240, 255, ring_alpha), width=4)
            for i in range(24):
                angle = (i * 0.26) - 1.57
                speed = 220 + (i % 6) * 60
                sp_x = impact_x + math.cos(angle) * (dt * speed)
                sp_y = impact_y + math.sin(angle) * (dt * speed) + (0.5 * 300 * dt * dt)
                if 0 <= sp_x < WIDTH and 0 <= sp_y < HEIGHT:
                    spark_color = COLOR_CRIMSON if i % 2 == 0 else COLOR_CYAN
                    draw.ellipse([(sp_x - 3, sp_y - 3), (sp_x + 3, sp_y + 3)], fill=spark_color)
                    
    # =========================================================================
    # SCENE 2 (7.5s - 16.5s): TRAP-SETTER VS TARGET + BACKGROUND CROWD
    # =========================================================================
    elif 7.5 <= t < 16.5:
        spotlight = get_volumetric_spotlight((255, 45, 85, 20), 540, 0, 240, 840, FLOOR_Y)
        frame.alpha_composite(spotlight)
        draw = ImageDraw.Draw(frame)
        
        draw_header_pill(draw, "02", "THE EGO BAIT", COLOR_CRIMSON)
        
        # Subtle Background Crowd (Phone zombies / bystanders observing)
        draw_crowd(draw, y=FLOOR_Y, count=6, x_min=80, x_max=1000, style="staring", progress=t, base_scale=0.68)
        
        # Bear Trap on center floor
        trap_x = 540
        trap_y = FLOOR_Y - 8
        draw.line([(trap_x - 170, trap_y), (trap_x + 170, trap_y)], fill=(80, 85, 105, 255), width=10)
        for ti in range(-7, 8):
            tx = trap_x + ti * 22
            th = 42 if (ti % 2 == 0) else 30
            draw.polygon([(tx - 10, trap_y), (tx, trap_y - th), (tx + 10, trap_y)], fill=COLOR_CRIMSON)
            draw.polygon([(tx - 6, trap_y), (tx, trap_y - th + 4), (tx + 6, trap_y)], fill=(255, 120, 145, 255))
        draw.ellipse([(trap_x - 22, trap_y - 20), (trap_x + 22, trap_y + 8)], fill=(60, 65, 80, 255), outline=COLOR_CRIMSON, width=3)
        
        # Floating Bait
        bait_y = trap_y - 150 + int(math.sin(t * 5) * 12)
        wave_r = int(70 + (t * 40) % 60)
        wave_a = int(max(0, 160 * (1.0 - ((t * 40) % 60) / 60.0)))
        draw.ellipse([(trap_x - wave_r, bait_y - wave_r // 2), (trap_x + wave_r, bait_y + wave_r // 2)], outline=(255, 45, 85, wave_a), width=2)
        
        draw.rounded_rectangle([(trap_x - 120, bait_y - 32), (trap_x + 120, bait_y + 32)], radius=12, fill=COLOR_CARD_BG, outline=COLOR_CRIMSON, width=3)
        draw.text((trap_x - 90, bait_y - 14), "[REACTION]", fill=COLOR_WHITE, font=FONT_BADGE)
        
        # Person B on left (target) in ponder pose
        draw_alan_becker_stickman(
            draw, 220, FLOOR_Y,
            pose="ponder",
            progress=t,
            color=COLOR_WHITE,
            scale=1.05,
            facing=1
        )
        
        # Manipulator on right (trap-setter) gesturing eagerly
        manip_pose = "point_throw" if (11.0 <= t < 15.0) else "smug"
        draw_alan_becker_stickman(
            draw, 860, FLOOR_Y,
            pose=manip_pose,
            progress=t,
            color=COLOR_CRIMSON,
            scale=1.05,
            facing=-1
        )
        
    # =========================================================================
    # SCENE 3 (16.5s - 23.0s): PERSON A (REACTIVE MELTDOWN) VS SMUG OPPONENT
    # =========================================================================
    elif 16.5 <= t < 23.0:
        shake_x = int(math.sin(t * 45) * 8)
        spotlight = get_volumetric_spotlight((255, 30, 60, 26), 400 + shake_x, 0, 120, 760, FLOOR_Y)
        frame.alpha_composite(spotlight)
        draw = ImageDraw.Draw(frame)
        
        draw_header_pill(draw, "03", "PERSON A: REACTIVE", COLOR_CRIMSON)
        
        # Person A in frantic meltdown on left
        person_a_x = 360 + shake_x
        draw_alan_becker_stickman(
            draw, person_a_x, FLOOR_Y,
            pose="flail",
            progress=t,
            color=COLOR_CRIMSON,
            scale=1.15,
            facing=1
        )
        
        # Steam zig-zag trails
        for si in range(4):
            sx = person_a_x - 50 + si * 35
            sy = FLOOR_Y - 400 - int(math.sin(t * 20 + si) * 25)
            draw.line([(sx, sy), (sx + 15, sy - 25), (sx - 10, sy - 50)], fill=COLOR_CRIMSON, width=5)
            
        # Shouting bubble
        sb_x = person_a_x + 110
        sb_y = FLOOR_Y - 370
        spikes = []
        for ai in range(14):
            ang = ai * (2 * math.pi / 14)
            sr = 120 if ai % 2 == 0 else 85
            spikes.append((sb_x + math.cos(ang) * sr, sb_y + math.sin(ang) * sr))
        draw.polygon(spikes, fill=COLOR_CARD_BG, outline=COLOR_CRIMSON)
        
        shout_txt = "! # ? @ !"
        s_box = FONT_LARGE.getbbox(shout_txt)
        stw = s_box[2] - s_box[0]
        draw.text((sb_x - stw // 2, sb_y - 26), shout_txt, fill=COLOR_WHITE, font=FONT_LARGE)
        
        # Smug Opponent on right watching Person A lose control
        draw_alan_becker_stickman(
            draw, 840, FLOOR_Y,
            pose="smug",
            progress=t,
            color=COLOR_WHITE,
            scale=1.1,
            facing=-1
        )
        
    # =========================================================================
    # SCENE 4 (23.0s - 33.5s): FACE-TO-FACE (ATTACKER PROVOKES -> HERO FREEZES)
    # =========================================================================
    elif 23.0 <= t < 33.5:
        spotlight = get_volumetric_spotlight((0, 240, 255, 22), 540, 0, 180, 900, FLOOR_Y)
        frame.alpha_composite(spotlight)
        draw = ImageDraw.Draw(frame)
        
        draw_header_pill(draw, "04", "PERSON B: COMPOSED", COLOR_CYAN)
        
        # Attacker on left (initially shouting, then faltering as silence holds)
        att_pose = "point_throw" if t < 26.5 else "recoil"
        draw_alan_becker_stickman(
            draw, 320, FLOOR_Y,
            pose=att_pose,
            progress=t,
            color=COLOR_CRIMSON,
            scale=1.1,
            facing=1
        )
        
        # Person B on right, rock-solid composure
        draw_alan_becker_stickman(
            draw, 760, FLOOR_Y,
            pose="arms_crossed",
            progress=t,
            color=COLOR_WHITE,
            scale=1.2,
            facing=-1
        )
        
        # 3-Second Holographic Countdown HUD in center
        if 25.5 <= t < 31.0:
            elapsed = t - 25.5
            sec_left = max(1, 3 - int(elapsed))
            hud_cx = 540
            hud_cy = FLOOR_Y - 560
            
            for ti in range(24):
                ang = ti * (math.pi / 12)
                r1 = 100
                r2 = 115 if ti % 6 == 0 else 108
                draw.line([
                    (hud_cx + math.cos(ang) * r1, hud_cy + math.sin(ang) * r1),
                    (hud_cx + math.cos(ang) * r2, hud_cy + math.sin(ang) * r2)
                ], fill=COLOR_CYAN_DIM, width=2)
                
            arc_p = (elapsed % 1.0)
            start_ang = -90
            end_ang = -90 + int(arc_p * 360)
            draw.arc([(hud_cx - 90, hud_cy - 90), (hud_cx + 90, hud_cy + 90)], start=start_ang, end=end_ang, fill=COLOR_CYAN, width=6)
            
            num_str = f"0{sec_left}"
            bbox = FONT_HUGE.getbbox(num_str)
            nw = bbox[2] - bbox[0]
            draw.text((hud_cx - nw // 2, hud_cy - 48), num_str, fill=COLOR_CYAN, font=FONT_HUGE)
            
            sub_lbl = "FRAME LOCKED // EYE CONTACT 100%"
            bbox = FONT_MICRO.getbbox(sub_lbl)
            lw = bbox[2] - bbox[0]
            draw.text((hud_cx - lw // 2, hud_cy + 120), sub_lbl, fill=COLOR_CYAN, font=FONT_MICRO)

    # =========================================================================
    # SCENE 5 (33.5s - 40.0s): THE PRESSURE ECHO & ATTACKER COLLAPSE
    # =========================================================================
    elif 33.5 <= t < 40.0:
        draw_header_pill(draw, "05", "THE PRESSURE ECHO", COLOR_GOLD)
        
        # Center Translucent Mirror Barrier
        mirror_x = 540
        draw.line([(mirror_x, FLOOR_Y - 500), (mirror_x, FLOOR_Y)], fill=(120, 160, 220, 140), width=4)
        draw.line([(mirror_x + 3, FLOOR_Y - 500), (mirror_x + 3, FLOOR_Y)], fill=(0, 240, 255, 80), width=2)
        
        # Person B on right, standing tall & unmoved
        draw_alan_becker_stickman(
            draw, 780, FLOOR_Y,
            pose="arms_crossed",
            progress=t,
            color=COLOR_WHITE,
            scale=1.15,
            facing=-1
        )
        
        # Attacker on left shrinking and recoiling
        dt = t - 33.5
        shrink_scale = max(0.68, 1.15 - dt * 0.08)
        draw_alan_becker_stickman(
            draw, 280, FLOOR_Y,
            pose="recoil",
            progress=t,
            color=COLOR_CRIMSON,
            scale=shrink_scale,
            facing=1
        )
        
        # Deflecting soundwaves
        wave_cycle = (dt * 1.5) % 1.0
        if wave_cycle < 0.5:
            wx = int(320 + wave_cycle * 2 * (mirror_x - 340))
            draw.arc([(wx - 30, FLOOR_Y - 260), (wx + 30, FLOOR_Y - 200)], start=-80, end=80, fill=COLOR_CRIMSON, width=5)
        else:
            wx = int(mirror_x - (wave_cycle - 0.5) * 2 * (mirror_x - 300))
            draw.arc([(wx - 30, FLOOR_Y - 260), (wx + 30, FLOOR_Y - 200)], start=100, end=260, fill=COLOR_CYAN, width=6)
            
        for si in range(3):
            sx = 280 - 25 + si * 25
            sy = FLOOR_Y - int(240 * shrink_scale) + int((dt * 150 + si * 40) % 90)
            draw.ellipse([(sx - 4, sy - 7), (sx + 4, sy + 7)], fill=COLOR_CYAN)

    # =========================================================================
    # SCENE 6 (40.0s - 51.5s): THE 48 LAWS OF POWER & STRIDING PAST DEFEATED ENEMY
    # =========================================================================
    else:
        spotlight = get_volumetric_spotlight((255, 215, 0, 16), WIDTH - 80, 0, WIDTH - 300, WIDTH + 100, FLOOR_Y)
        frame.alpha_composite(spotlight)
        draw = ImageDraw.Draw(frame)
        
        card_w = 920
        card_h = 160
        card_x = WIDTH // 2 - card_w // 2
        card_y = 150
        
        draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=16, fill=COLOR_CARD_BG, outline=COLOR_GOLD, width=3)
        cb_len = 25
        draw.line([(card_x - 4, card_y), (card_x + cb_len, card_y)], fill=COLOR_GOLD, width=5)
        draw.line([(card_x, card_y - 4), (card_x + cb_len, card_y)], fill=COLOR_GOLD, width=5)
        draw.line([(card_x + card_w - cb_len, card_y), (card_x + card_w + 4, card_y)], fill=COLOR_GOLD, width=5)
        draw.line([(card_x + card_w, card_y - 4), (card_x + card_w, card_y + cb_len)], fill=COLOR_GOLD, width=5)
        
        draw.text((card_x + 35, card_y + 25), "THE 48 LAWS OF POWER // LAW 4", fill=COLOR_GOLD, font=FONT_BADGE)
        draw.text((card_x + 35, card_y + 80), "Never interrupt an enemy destroying themselves.", fill=COLOR_WHITE, font=FONT_QUOTE)
        
        # Defeated Opponent slumped on the floor in shame on left
        draw_alan_becker_stickman(
            draw, 220, FLOOR_Y,
            pose="hunched_shame",
            progress=t,
            color=COLOR_MUTED,
            scale=0.9,
            facing=1
        )
        
        # Person B strides past the defeated opponent into the golden light
        walk_x = int(380 + (t - 40.0) * 52)
        draw_alan_becker_stickman(
            draw, walk_x, FLOOR_Y,
            pose="walk",
            progress=t,
            color=COLOR_WHITE,
            scale=1.1,
            facing=1
        )
        
        for step_i in range(5):
            foot_x = walk_x - (step_i + 1) * 70
            if foot_x > 360:
                draw.ellipse([(foot_x - 15, FLOOR_Y + 2), (foot_x + 15, FLOOR_Y + 6)], fill=(0, 240, 255, max(0, 80 - step_i * 16)))
                
    return frame

def render_ink_noir_short(output_path, total_duration_sec=51.4):
    total_frames = int(total_duration_sec * FPS)
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    for f in range(total_frames):
        t = f / FPS
        frame = render_frame_at_time(t, f)
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
