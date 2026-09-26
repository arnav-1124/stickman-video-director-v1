import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

WIDTH = 1080
HEIGHT = 1920
FPS = 30

def create_background():
    # Dark Slate with subtle vignette
    base = Image.new("RGBA", (WIDTH, HEIGHT), (11, 11, 14, 255))
    draw = ImageDraw.Draw(base)
    # Draw subtle floor baseline
    draw.line([(80, 1450), (WIDTH - 80, 1450)], fill=(35, 35, 45, 255), width=4)
    return base

def draw_spotlight(draw, center_x, ground_y, radius=320, color=(255, 42, 77, 40)):
    # Draw radial conic spotlight on floor
    draw.ellipse(
        [(center_x - radius, ground_y - 60), (center_x + radius, ground_y + 60)],
        fill=color
    )
    # Spotlight cone from ceiling
    draw.polygon(
        [(center_x - 40, 0), (center_x + 40, 0), (center_x + radius, ground_y), (center_x - radius, ground_y)],
        fill=(color[0], color[1], color[2], 18)
    )

def draw_stickman(draw, x, y, pose="idle", progress=0.0, color=(255, 255, 255, 255), line_width=8):
    # Head
    head_radius = 42
    head_center_y = y - 260
    
    # Alan Becker squash & stretch factor
    squash = 1.0
    if pose == "recoil":
        squash = 0.85 + 0.15 * math.cos(progress * math.pi * 2)
    elif pose == "calm":
        squash = 1.0 + 0.05 * math.sin(progress * math.pi)

    head_ry = head_radius * squash
    head_rx = head_radius / math.sqrt(squash)
    
    # Head outline (hollow circular head)
    draw.ellipse(
        [(x - head_rx, head_center_y - head_ry), (x + head_rx, head_center_y + head_ry)],
        outline=color,
        width=line_width
    )
    
    # Spine
    neck_y = head_center_y + head_ry
    pelvis_y = y - 110
    pelvis_x = x
    if pose == "recoil":
        pelvis_x -= 25
    draw.line([(x, neck_y), (pelvis_x, pelvis_y)], fill=color, width=line_width)
    
    # Arms
    shoulder_y = neck_y + 25
    if pose == "calm":
        # Arms crossed
        draw.line([(x, shoulder_y), (x - 45, shoulder_y + 40)], fill=color, width=line_width)
        draw.line([(x - 45, shoulder_y + 40), (x + 35, shoulder_y + 45)], fill=color, width=line_width)
        draw.line([(x, shoulder_y), (x + 45, shoulder_y + 40)], fill=color, width=line_width)
        draw.line([(x + 45, shoulder_y + 40), (x - 35, shoulder_y + 45)], fill=color, width=line_width)
    elif pose == "recoil":
        # Hands up in shock
        draw.line([(x, shoulder_y), (x - 60, shoulder_y - 20)], fill=color, width=line_width)
        draw.line([(x - 60, shoulder_y - 20), (x - 80, shoulder_y - 70)], fill=color, width=line_width)
        draw.line([(x, shoulder_y), (x + 60, shoulder_y - 15)], fill=color, width=line_width)
        draw.line([(x + 60, shoulder_y - 15), (x + 85, shoulder_y - 65)], fill=color, width=line_width)
    else:
        # Idle gentle sway
        arm_sway = math.sin(progress * math.pi * 2) * 12
        draw.line([(x, shoulder_y), (x - 40 + arm_sway, shoulder_y + 70)], fill=color, width=line_width)
        draw.line([(x, shoulder_y), (x + 40 - arm_sway, shoulder_y + 70)], fill=color, width=line_width)

    # Legs & Feet
    knee_l_x = pelvis_x - 35
    knee_r_x = pelvis_x + 35
    foot_l_y = y
    foot_r_y = y
    
    draw.line([(pelvis_x, pelvis_y), (knee_l_x, pelvis_y + 60)], fill=color, width=line_width)
    draw.line([(knee_l_x, pelvis_y + 60), (pelvis_x - 40, foot_l_y)], fill=color, width=line_width)
    draw.line([(pelvis_x - 40, foot_l_y), (pelvis_x - 60, foot_l_y)], fill=color, width=line_width)
    
    draw.line([(pelvis_x, pelvis_y), (knee_r_x, pelvis_y + 60)], fill=color, width=line_width)
    draw.line([(knee_r_x, pelvis_y + 60), (pelvis_x + 40, foot_r_y)], fill=color, width=line_width)
    draw.line([(pelvis_x + 40, foot_r_y), (pelvis_x + 60, foot_r_y)], fill=color, width=line_width)

def render_sample_clip(output_path, duration_sec=3):
    total_frames = int(duration_sec * FPS)
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
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    base_bg = create_background()
    
    for f in range(total_frames):
        t = f / FPS
        frame = base_bg.copy()
        draw = ImageDraw.Draw(frame)
        
        # Spotlight activates at 1.0s
        if t >= 1.0:
            spot_alpha = min(70, int((t - 1.0) * 120))
            draw_spotlight(draw, 540, 1450, radius=280, color=(255, 42, 77, spot_alpha))
            
        pose = "idle"
        if t >= 1.0:
            pose = "recoil"
            
        draw_stickman(draw, 540, 1450, pose=pose, progress=t)
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
    print(f"[Renderer] Successfully rendered {total_frames} frames to {output_path}")

if __name__ == "__main__":
    render_sample_clip("temp/test_stickman.mp4", duration_sec=3)
