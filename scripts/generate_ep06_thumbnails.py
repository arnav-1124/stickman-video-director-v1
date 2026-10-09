import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def render_thumbnail(base_image_path, text_lines, out_path, font_path, badge_path=None):
    im = Image.open(base_image_path).convert("RGBA")
    w, h = im.size
    draw = ImageDraw.Draw(im)

    # Calculate font sizes
    # Line 1: ~78px, Line 2: ~88px, Line 3: ~78px, Line 4: ~72px for 1536x2752
    scale = w / 1536.0
    f_size_std = int(82 * scale)
    f_size_hero = int(96 * scale)
    f_size_sub = int(74 * scale)

    font_std = ImageFont.truetype(str(font_path), f_size_std)
    font_hero = ImageFont.truetype(str(font_path), f_size_hero)
    font_sub = ImageFont.truetype(str(font_path), f_size_sub)

    # Starting Y position in the upper third
    start_y = int(220 * scale)
    line_spacing = int(24 * scale)

    current_y = start_y
    for i, (text, color, is_hero, is_sub) in enumerate(text_lines):
        f = font_hero if is_hero else (font_sub if is_sub else font_std)
        bbox = draw.textbbox((0, 0), text, font=f)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (w - text_w) // 2

        # Draw clean shadow/glow for pop
        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3)]:
            draw.text((x + dx, current_y + dy), text, font=f, fill=(255, 255, 255, 180))
        # Draw main text
        draw.text((x, current_y), text, font=f, fill=color)
        current_y += text_h + line_spacing

    # Place channel PhD badge in bottom right corner if provided
    if badge_path and Path(badge_path).exists():
        badge = Image.open(badge_path).convert("RGBA")
        badge_w, badge_h = badge.size
        # Resize badge slightly for high-res
        target_badge_w = int(140 * scale)
        target_badge_h = int(140 * scale)
        badge = badge.resize((target_badge_w, target_badge_h), Image.Resampling.LANCZOS)
        badge_x = w - target_badge_w - int(45 * scale)
        badge_y = h - target_badge_h - int(45 * scale)
        im.paste(badge, (badge_x, badge_y), badge)

    # Convert to RGB and save
    final_rgb = im.convert("RGB")
    final_rgb.save(out_path, quality=95)
    print(f"Saved: {out_path} ({w}x{h})")

def main():
    base_dir = Path("f:/Arnav - YT/stickman-video-director").resolve()
    ep_dir = base_dir / "projects" / "sticky_in_dark" / "shorts" / "ep06_when_you_make_eye_contact_in_public"
    slides_dir = ep_dir / "slides"
    thumbs_dir = ep_dir / "thumbnails"
    thumbs_dir.mkdir(parents=True, exist_ok=True)
    renders_dir = base_dir / "renders" / "shorts" / "ep06_when_you_make_eye_contact_in_public"
    renders_dir.mkdir(parents=True, exist_ok=True)

    font_path = base_dir / "assets" / "fonts" / "PermanentMarker-Regular.ttf"
    badge_path = base_dir / "assets" / "branding" / "sticky_in_dark_badge.png"

    # Color Palette from Ep 05
    c_black = (10, 13, 20)       # #0A0D14
    c_red = (255, 42, 77)        # #FF2A4D Crimson Red
    c_yellow = (229, 169, 60)    # #E5A93C Mustard / Canary Gold

    # Option 1: Top Recommended (Confrontation Anchor + Relatable Hook)
    lines_opt1 = [
        ("WHEN YOU MAKE", c_black, False, False),
        ("EYE CONTACT", c_red, True, False),
        ("IN PUBLIC", c_black, False, False),
        ("(NEVER FAKE TEXT)", c_yellow, False, True),
    ]
    render_thumbnail(slides_dir / "slide_01.jpg", lines_opt1, thumbs_dir / "thumb_option_1_laser_confrontation.jpg", font_path, badge_path)

    # Option 2: The Social Panic Face (Close-up Spiral Eyes + Direct Curiosity)
    lines_opt2 = [
        ("WHY EYE CONTACT", c_black, False, False),
        ("FEELS SO AWKWARD", c_red, True, False),
        ("IN PUBLIC", c_black, False, False),
        ("(DON'T LOOK DOWN)", c_yellow, False, True),
    ]
    render_thumbnail(slides_dir / "slide_02.jpg", lines_opt2, thumbs_dir / "thumb_option_2_spiral_panic.jpg", font_path, badge_path)

    # Option 3: The Fake-Texting Trap (Hunched Phone Stare + The Callout)
    lines_opt3 = [
        ("THEY KNOW", c_black, False, False),
        ("YOU'RE FAKING", c_red, True, False),
        ("ON YOUR PHONE", c_black, False, False),
        ("(DO THIS INSTEAD)", c_yellow, False, True),
    ]
    render_thumbnail(slides_dir / "slide_04.jpg", lines_opt3, thumbs_dir / "thumb_option_3_fake_texting_trap.jpg", font_path, badge_path)

    # Option 4: The 3-Step Solution (Action-driven)
    lines_opt4 = [
        ("HOW TO WALK", c_black, False, False),
        ("PAST ANYONE", c_red, True, False),
        ("UNBOTHERED", c_black, False, False),
        ("(THE 3-STEP NOD)", c_yellow, False, True),
    ]
    render_thumbnail(slides_dir / "slide_01.jpg", lines_opt4, thumbs_dir / "thumb_option_4_unbothered_walk.jpg", font_path, badge_path)

    # Set Option 1 as primary master thumbnail
    master_thumb = ep_dir / "thumbnail.jpg"
    render_thumb = renders_dir / "WHEN_YOU_MAKE_EYE_CONTACT_IN_PUBLIC_THUMBNAIL.jpg"

    import shutil
    shutil.copy2(thumbs_dir / "thumb_option_1_laser_confrontation.jpg", master_thumb)
    shutil.copy2(thumbs_dir / "thumb_option_1_laser_confrontation.jpg", render_thumb)
    print("\nMaster Thumbnail published to:")
    print("1.", master_thumb)
    print("2.", render_thumb)

if __name__ == "__main__":
    main()
