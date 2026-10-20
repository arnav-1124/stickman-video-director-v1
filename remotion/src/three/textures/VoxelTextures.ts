import * as THREE from "three";

/**
 * Creates a standard 16x16 Minecraft CanvasTexture configured with NearestFilter
 * to guarantee razor-sharp, authentic pixel art rendering without blur.
 */
function createPixelTexture(draw: (ctx: CanvasRenderingContext2D) => void): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 16;
  canvas.height = 16;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;
  draw(ctx);

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.generateMipmaps = true;
  texture.minFilter = THREE.LinearMipmapLinearFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.anisotropy = 16;
  return texture;
}

/**
 * Authentic 16x16 Minecraft Grass Block (Side View)
 * Rich dirt base with jagged green grass fringe hanging down from the top edge.
 */
export function createMinecraftGrassSideTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    // Dirt base with pixel variation
    const dirtShades = ["#866043", "#745237", "#60432c", "#533722", "#8f6648"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        const rand = (x * 7 + y * 13) % dirtShades.length;
        ctx.fillStyle = dirtShades[rand];
        ctx.fillRect(x, y, 1, 1);
      }
    }

    // Jagged grass overhang fringe (3 to 5 pixels deep)
    const grassShades = ["#4c7c28", "#5c8c34", "#3d661e", "#689c3a"];
    const fringeDepths = [3, 4, 3, 5, 4, 3, 4, 3, 5, 4, 3, 4, 5, 3, 4, 3];
    for (let x = 0; x < 16; x++) {
      const depth = fringeDepths[x];
      for (let y = 0; y < depth; y++) {
        const rand = (x * 3 + y * 5) % grassShades.length;
        ctx.fillStyle = grassShades[rand];
        ctx.fillRect(x, y, 1, 1);
      }
      // Grass tip highlight
      ctx.fillStyle = "#2d4e16";
      ctx.fillRect(x, depth, 1, 1);
    }
  });
}

/**
 * Authentic 16x16 Minecraft Grass Block (Top View)
 */
export function createMinecraftGrassTopTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const grassShades = ["#4c7c28", "#5c8c34", "#3d661e", "#689c3a", "#54882e"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        const rand = (x * 11 + y * 17) % grassShades.length;
        ctx.fillStyle = grassShades[rand];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  });
}

/**
 * Authentic 16x16 Minecraft Coarse Dirt Block
 */
export function createMinecraftDirtTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const dirtShades = ["#866043", "#745237", "#60432c", "#533722", "#8f6648"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        const rand = (x * 9 + y * 19) % dirtShades.length;
        ctx.fillStyle = dirtShades[rand];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  });
}

/**
 * Authentic 16x16 Minecraft Oak Log Bark (Side View)
 */
export function createMinecraftOakLogSideTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const barkShades = ["#6b5232", "#594326", "#4d391e", "#382914", "#775b37"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        // Vertical bark grooves
        const stripe = (x % 3 === 0) ? 2 : (x * 5 + y) % barkShades.length;
        ctx.fillStyle = barkShades[stripe];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  });
}

/**
 * Authentic 16x16 Minecraft Oak Log Rings (Top/Bottom View)
 */
export function createMinecraftOakLogTopTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    ctx.fillStyle = "#4d391e"; // Bark rim
    ctx.fillRect(0, 0, 16, 16);

    ctx.fillStyle = "#8f6f46"; // Outer wood
    ctx.fillRect(1, 1, 14, 14);

    ctx.fillStyle = "#6e5230"; // Growth ring 1
    ctx.strokeRect(3.5, 3.5, 9, 9);

    ctx.fillStyle = "#a88458"; // Core heartwood
    ctx.fillRect(5, 5, 6, 6);

    ctx.fillStyle = "#5c4122"; // Pith center
    ctx.fillRect(7, 7, 2, 2);
  });
}

/**
 * Authentic 16x16 Minecraft Oak Wood Planks
 */
export function createOakPlanksTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const plankColors = ["#b88755", "#aa7c4c", "#9c6f42", "#8f6339"];
    // 4 horizontal wood planks (each 4 pixels tall)
    for (let plank = 0; plank < 4; plank++) {
      const py = plank * 4;
      const base = plankColors[plank % plankColors.length];
      ctx.fillStyle = base;
      ctx.fillRect(0, py, 16, 3);

      // Plank divider seam
      ctx.fillStyle = "#3d2714";
      ctx.fillRect(0, py + 3, 16, 1);

      // Tiny nail spots
      ctx.fillStyle = "#50361e";
      ctx.fillRect(plank % 2 === 0 ? 2 : 13, py + 1, 1, 1);
    }
  });
}

/**
 * Authentic 16x16 Minecraft Spruce Wood Floor Planks
 */
export function createSpruceFloorTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const plankColors = ["#684e32", "#5c4329", "#4f3922", "#45321d"];
    for (let plank = 0; plank < 4; plank++) {
      const py = plank * 4;
      ctx.fillStyle = plankColors[plank % plankColors.length];
      ctx.fillRect(0, py, 16, 3);

      ctx.fillStyle = "#22160a";
      ctx.fillRect(0, py + 3, 16, 1);
    }
  });
}

/**
 * Authentic 16x16 Minecraft Stone Block
 */
export function createMinecraftStoneTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const stoneShades = ["#737373", "#828282", "#646464", "#575757", "#909090"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        const rand = (x * 13 + y * 7) % stoneShades.length;
        ctx.fillStyle = stoneShades[rand];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  });
}

/**
 * Authentic 16x16 Minecraft Park Gravel Path / Cobble Walkway Texture
 * Cohesive earthy stone hues with zero high-frequency pixel scintillation.
 */
export function createParkGravelPathTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const gravelTones = ["#8c867c", "#969085", "#7e786e", "#9e978d", "#868076", "#736d64"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        const rand = (x * 7 + y * 11) % gravelTones.length;
        ctx.fillStyle = gravelTones[rand];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  });
}

/**
 * Authentic 16x16 Minecraft Oak Foliage Leaves
 */
export function createMinecraftLeavesTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const leafShades = ["#2f591e", "#3a6d25", "#244517", "#48852e"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        const rand = (x * 17 + y * 19) % leafShades.length;
        ctx.fillStyle = leafShades[rand];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  });
}

/**
 * Authentic 16x16 Minecraft Red Wool Block (Bed Mattress)
 */
export function createMinecraftRedWoolTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const redShades = ["#a02720", "#b8332a", "#871d18", "#c93d33"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        const rand = (x * 5 + y * 9) % redShades.length;
        ctx.fillStyle = redShades[rand];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  });
}

/**
 * Authentic 16x16 Minecraft White Wool Block (Bed Pillow)
 */
export function createMinecraftWhiteWoolTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    const whiteShades = ["#edebe6", "#e0ded9", "#f5f4f0", "#d1cfca"];
    for (let x = 0; x < 16; x++) {
      for (let y = 0; y < 16; y++) {
        const rand = (x * 11 + y * 3) % whiteShades.length;
        ctx.fillStyle = whiteShades[rand];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  });
}

/**
 * Authentic 16x16 Minecraft Bookshelf Block
 */
export function createBookshelfTexture(): THREE.CanvasTexture {
  return createPixelTexture((ctx) => {
    // Oak frame
    ctx.fillStyle = "#9c6f42";
    ctx.fillRect(0, 0, 16, 16);

    ctx.fillStyle = "#3d2714";
    ctx.fillRect(1, 1, 14, 6);
    ctx.fillRect(1, 9, 14, 6);

    // Row 1 books
    const b1 = ["#b8332a", "#3c5999", "#3b7a3d", "#d1a13b", "#b8332a"];
    b1.forEach((c, idx) => {
      ctx.fillStyle = c;
      ctx.fillRect(2 + idx * 2.5, 2, 2, 5);
    });

    // Row 2 books
    const b2 = ["#d1a13b", "#8b4f9e", "#3c5999", "#3b7a3d", "#b8332a"];
    b2.forEach((c, idx) => {
      ctx.fillStyle = c;
      ctx.fillRect(2 + idx * 2.5, 10, 2, 5);
    });
  });
}

/**
 * Authentic Glowing Minecraft Digital Alarm Clock Face
 * High-resolution canvas with razor-sharp 7-segment/digital typography,
 * clearly visible "AM" indicator, and zero clutter/dots.
 */
export function createDigitalClockTexture(
  timeStr: string = "02:00",
  blink: boolean = true,
  color: "red" | "cyan" | "white" | "amber" = "red",
  ampm: "AM" | "PM" = "AM"
): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 128;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = true;

  const colorPalettes = {
    red: { bg: "#080204", scan: "#120508", glow: "#ff1a40", core: "#ffffff", am: "#ff2a4d", amCore: "#ffe6ea" },
    cyan: { bg: "#02070c", scan: "#05131e", glow: "#38bdf8", core: "#f0f9ff", am: "#38bdf8", amCore: "#e0f2fe" },
    white: { bg: "#050608", scan: "#0f1218", glow: "#94a3b8", core: "#ffffff", am: "#cbd5e1", amCore: "#f8fafc" },
    amber: { bg: "#080602", scan: "#151004", glow: "#f59e0b", core: "#fffbeb", am: "#f59e0b", amCore: "#fef3c7" },
  };
  const pal = colorPalettes[color] || colorPalettes.red;

  // Screen background (deep dark tinted LCD screen)
  ctx.fillStyle = pal.bg;
  ctx.fillRect(0, 0, 256, 128);

  // Subtle LCD scanline overlay
  ctx.fillStyle = pal.scan;
  for (let y = 0; y < 128; y += 4) {
    ctx.fillRect(0, y, 256, 1.5);
  }

  // Glowing Digital LED Digits
  ctx.font = "bold 56px 'Courier New', monospace";
  ctx.textAlign = "left";
  ctx.textBaseline = "middle";

  const displayTime = blink ? timeStr : timeStr.replace(":", " ");

  // Outer Neon Glow
  ctx.shadowColor = pal.glow;
  ctx.shadowBlur = 18;
  ctx.fillStyle = pal.glow;
  ctx.fillText(displayTime, 20, 64);

  // Core Bright Text
  ctx.shadowBlur = 3;
  ctx.fillStyle = pal.core;
  ctx.fillText(displayTime, 20, 64);

  // Clear, high-visibility AM / PM indicator
  ctx.font = "bold 20px 'Arial Black', Impact, sans-serif";
  ctx.textAlign = "center";
  ctx.shadowColor = pal.glow;
  ctx.shadowBlur = 10;
  ctx.fillStyle = pal.am;
  ctx.fillText(ampm, 216, 64);

  // Inner core highlight for AM / PM
  ctx.shadowBlur = 1;
  ctx.fillStyle = pal.amCore;
  ctx.fillText(ampm, 216, 64);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  texture.generateMipmaps = false;
  return texture;
}

/**
 * Modern Smartphone Glass Screen Texture (Dark OLED Lockscreen)
 */
export function createPhoneScreenTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 128;
  canvas.height = 256;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = true;

  // Deep dark OLED panel
  ctx.fillStyle = "#07080c";
  ctx.fillRect(0, 0, 128, 256);

  // Subtle glass reflection gradient across screen
  const sheen = ctx.createLinearGradient(0, 0, 128, 256);
  sheen.addColorStop(0.0, "rgba(255, 255, 255, 0.08)");
  sheen.addColorStop(0.4, "rgba(255, 255, 255, 0.02)");
  sheen.addColorStop(0.6, "rgba(255, 255, 255, 0.0)");
  sheen.addColorStop(1.0, "rgba(255, 255, 255, 0.04)");
  ctx.fillStyle = sheen;
  ctx.fillRect(0, 0, 128, 256);

  // Top speaker / Dynamic Island camera notch
  ctx.fillStyle = "#020204";
  ctx.beginPath();
  ctx.roundRect(48, 12, 32, 9, 4.5);
  ctx.fill();

  // Subtle Lock Icon
  ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(58, 44, 12, 9);
  ctx.beginPath();
  ctx.arc(64, 44, 4, Math.PI, 0);
  ctx.stroke();

  // Faint Lockscreen Digital Clock
  ctx.font = "bold 24px -apple-system, BlinkMacSystemFont, sans-serif";
  ctx.fillStyle = "rgba(255, 255, 255, 0.22)";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("02:00", 64, 76);

  // Bottom home indicator bar
  ctx.fillStyle = "rgba(255, 255, 255, 0.35)";
  ctx.beginPath();
  ctx.roundRect(44, 242, 40, 3, 1.5);
  ctx.fill();

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  return texture;
}

/**
 * Authentic 8x8 Minecraft Character Head Face Texture
 * Crisp 8x8 pixel grid with hair, 2x2 pixel eyes (dark pupil, white catchlight), skin.
 */
export function createVoxelFaceTexture(isTired: boolean = false): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 8;
  canvas.height = 8;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  // Clean skin base tone
  ctx.fillStyle = "#f6d7b0";
  ctx.fillRect(0, 0, 8, 8);

  // Dark brown pixel hair on top 2 rows
  ctx.fillStyle = "#2c1c0f";
  ctx.fillRect(0, 0, 8, 2);
  ctx.fillRect(0, 2, 1, 2);
  ctx.fillRect(7, 2, 1, 2);

  // 2x2 Pixel Eyes: Left eye (x=1..2, y=3..4), Right eye (x=5..6, y=3..4)
  // White sclera
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(1, 3, 2, 2);
  ctx.fillRect(5, 3, 2, 2);

  // Dark navy/black pupil with catchlight
  ctx.fillStyle = "#1e2b3e";
  ctx.fillRect(2, 3, 1, 2);
  ctx.fillRect(6, 3, 1, 2);

  // Tired heavy eyelids / under-eye bags
  if (isTired) {
    ctx.fillStyle = "#aa8270";
    ctx.fillRect(1, 3, 2, 1);
    ctx.fillRect(5, 3, 2, 1);
    ctx.fillRect(1, 5, 2, 1);
    ctx.fillRect(5, 5, 2, 1);
  }

  // Pixel mouth
  ctx.fillStyle = "#8a5840";
  ctx.fillRect(3, 6, 2, 1);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.NearestFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.generateMipmaps = false;
  return texture;
}

/**
 * Authentic Minecraft Character Hair Texture with chunky hair locks (no high-frequency moire)
 */
export function createVoxelHairTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 16;
  canvas.height = 16;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  // Solid rich dark brown base
  ctx.fillStyle = "#382414";
  ctx.fillRect(0, 0, 16, 16);

  // Chunky 4x4 pixel hair clusters
  const hairHighlights = ["#482f1b", "#301e10", "#402917", "#382414"];
  for (let bx = 0; bx < 4; bx++) {
    for (let by = 0; by < 4; by++) {
      const shade = hairHighlights[(bx * 2 + by * 3) % hairHighlights.length];
      ctx.fillStyle = shade;
      ctx.fillRect(bx * 4, by * 4, 4, 4);
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.NearestFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.generateMipmaps = false;
  return texture;
}

/**
 * Authentic Minecraft Character Shirt / Torso Texture (Clean Teal / Cyan Tunic)
 */
export function createVoxelTorsoTexture(type: "Alex" | "Marcus" = "Alex"): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 16;
  canvas.height = 24;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  const isMarcus = type === "Marcus";

  // Base tunic color
  ctx.fillStyle = isMarcus ? "#1e2638" : "#009aa6";
  ctx.fillRect(0, 0, 16, 24);

  // Subtle tonal seams
  ctx.fillStyle = isMarcus ? "#161d2b" : "#008894";
  ctx.fillRect(0, 0, 2, 24);
  ctx.fillRect(14, 0, 2, 24);

  // Collar / V-neck
  ctx.fillStyle = isMarcus ? "#8d5524" : "#f6d7b0";
  ctx.fillRect(6, 0, 4, 4);
  ctx.fillRect(6, 4, 4, 2);

  // Golden / bronze embroidery trim for Marcus
  if (isMarcus) {
    ctx.fillStyle = "#d4af37";
    ctx.fillRect(5, 0, 1, 6);
    ctx.fillRect(10, 0, 1, 6);
    ctx.fillRect(6, 6, 4, 1);
  }

  // Dark belt line on bottom rows
  ctx.fillStyle = "#18181c";
  ctx.fillRect(0, 21, 16, 3);
  ctx.fillStyle = "#d4af37"; // Belt buckle
  ctx.fillRect(6, 21, 4, 3);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearMipmapLinearFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.generateMipmaps = true;
  return texture;
}

/**
 * Authentic Minecraft Character Arm Sleeve & Skin Hands
 */
export function createVoxelArmTexture(type: "Alex" | "Marcus" = "Alex"): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 4;
  canvas.height = 12;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  const isMarcus = type === "Marcus";

  // Sleeve (top 8 rows)
  ctx.fillStyle = isMarcus ? "#1e2638" : "#008a94";
  ctx.fillRect(0, 0, 4, 8);
  ctx.fillStyle = isMarcus ? "#d4af37" : "#00a8b5"; // Gold cuff rim for Marcus
  ctx.fillRect(0, 7, 4, 1);

  // Bare skin hand (bottom 4 rows)
  ctx.fillStyle = isMarcus ? "#8d5524" : "#f6d7b0";
  ctx.fillRect(0, 8, 4, 4);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.NearestFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.generateMipmaps = false;
  return texture;
}

/**
 * Authentic Minecraft Character Pants & Shoes
 * Clean solid denim indigo with zipper fly stitching and mipmapped filtering
 * to prevent pixel shimmering / moiré flickering during camera movement.
 */
export function createVoxelLegTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 16;
  canvas.height = 32;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  // Solid rich dark denim navy base
  ctx.fillStyle = "#253456";
  ctx.fillRect(0, 0, 16, 24);

  // Subtle tonal leg crease / side shading (no noisy alternating checkerboard)
  ctx.fillStyle = "#2c3d64";
  ctx.fillRect(4, 0, 8, 24);

  ctx.fillStyle = "#1e2b48";
  ctx.fillRect(0, 0, 2, 24);
  ctx.fillRect(14, 0, 2, 24);

  // Gold / tan zipper fly stitching at the top
  ctx.fillStyle = "#8a6d3b";
  ctx.fillRect(7, 0, 2, 6);
  ctx.fillStyle = "#c29b53"; // Zipper pull tab
  ctx.fillRect(7, 1, 2, 2);

  // Dark boots (bottom 8 rows)
  ctx.fillStyle = "#242426";
  ctx.fillRect(0, 24, 16, 8);
  ctx.fillStyle = "#18181a";
  ctx.fillRect(0, 30, 16, 2);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearMipmapLinearFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.generateMipmaps = true;
  return texture;
}

/**
 * Generates dynamic texture for authentic Minecraft Voxel DAY 4 notice board.
 */
export function createDayFourTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 256;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  // 1. Dark Spruce / Oak Wood Planks Background with authentic pixel grain
  const woodShades = ["#2b1810", "#362015", "#42281a", "#4a2d1d", "#22130c"];
  for (let py = 0; py < 256; py += 8) {
    for (let px = 0; px < 512; px += 8) {
      const idx = (Math.floor(px / 8) * 7 + Math.floor(py / 8) * 13) % woodShades.length;
      ctx.fillStyle = woodShades[idx];
      ctx.fillRect(px, py, 8, 8);
    }
  }

  // Horizontal plank seam dividers
  ctx.fillStyle = "#160b07";
  for (let seamY = 64; seamY < 256; seamY += 64) {
    ctx.fillRect(0, seamY - 2, 512, 4);
  }

  // 2. Heavy Dark Iron / Stone Beveled Outer Border
  const borderThick = 20;
  ctx.fillStyle = "#18202c";
  ctx.fillRect(0, 0, 512, borderThick); // Top
  ctx.fillRect(0, 256 - borderThick, 512, borderThick); // Bottom
  ctx.fillRect(0, 0, borderThick, 256); // Left
  ctx.fillRect(512 - borderThick, 0, borderThick, 256); // Right

  // Inner beveled rim
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 4;
  ctx.strokeRect(borderThick, borderThick, 512 - borderThick * 2, 256 - borderThick * 2);

  // Corner Iron Studs / Rivets (3D pixel metallic bolts)
  const drawBolt = (bx: number, by: number) => {
    ctx.fillStyle = "#0f172a";
    ctx.fillRect(bx - 6, by - 6, 12, 12);
    ctx.fillStyle = "#64748b";
    ctx.fillRect(bx - 4, by - 4, 8, 8);
    ctx.fillStyle = "#94a3b8";
    ctx.fillRect(bx - 2, by - 2, 4, 4);
  };
  drawBolt(10, 10);
  drawBolt(502, 10);
  drawBolt(10, 246);
  drawBolt(502, 246);

  // 3. Pixel Glyph Typography for "DAY 4"
  // Authentic 5x7 Voxel Letter Bitmaps
  const glyphs: Record<string, number[][]> = {
    D: [
      [1, 1, 1, 1, 0],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 0],
    ],
    A: [
      [0, 1, 1, 1, 0],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
    ],
    Y: [
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [0, 1, 0, 1, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
    ],
    "4": [
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1],
      [0, 0, 0, 0, 1],
    ],
  };

  const word = ["D", "A", "Y", " ", "4"];
  const pixelSize = 14;
  const letterW = 5 * pixelSize; // 70px
  const letterH = 7 * pixelSize; // 98px
  const letterSpacing = 14;
  const wordSpacing = 42;

  let totalTextW = 0;
  for (const ch of word) {
    if (ch === " ") totalTextW += wordSpacing;
    else totalTextW += letterW + letterSpacing;
  }
  totalTextW -= letterSpacing;

  let startX = Math.floor((512 - totalTextW) / 2);
  const startY = Math.floor((256 - letterH) / 2);

  // Render each glyph with deep 3D drop shadow, bevel, and vibrant voxel face
  for (const ch of word) {
    if (ch === " ") {
      startX += wordSpacing;
      continue;
    }
    const map = glyphs[ch];
    if (map) {
      // 1. Deep 3D Drop Shadow
      ctx.fillStyle = "#0a0705";
      for (let r = 0; r < 7; r++) {
        for (let c = 0; c < 5; c++) {
          if (map[r][c] === 1) {
            ctx.fillRect(startX + c * pixelSize + 8, startY + r * pixelSize + 8, pixelSize, pixelSize);
          }
        }
      }

      // 2. Voxel Bevel Rim
      ctx.fillStyle = ch === "4" ? "#991b1b" : "#b45309";
      for (let r = 0; r < 7; r++) {
        for (let c = 0; c < 5; c++) {
          if (map[r][c] === 1) {
            ctx.fillRect(startX + c * pixelSize + 2, startY + r * pixelSize + 2, pixelSize, pixelSize);
          }
        }
      }

      // 3. Crisp Voxel Face (Crimson Red for "4", Crisp Ivory/Gold for "DAY")
      for (let r = 0; r < 7; r++) {
        for (let c = 0; c < 5; c++) {
          if (map[r][c] === 1) {
            ctx.fillStyle = ch === "4" ? "#ef4444" : "#fef08a";
            ctx.fillRect(startX + c * pixelSize, startY + r * pixelSize, pixelSize, pixelSize);
            // Highlight pixel at top-left of each voxel
            ctx.fillStyle = ch === "4" ? "#fca5a5" : "#ffffff";
            ctx.fillRect(startX + c * pixelSize, startY + r * pixelSize, 3, 3);
          }
        }
      }
    }
    startX += letterW + letterSpacing;
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.NearestFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.generateMipmaps = false;
  return texture;
}

/**
 * Real House Interior Plaster Wall Texture (Warm contemporary greige)
 */
export function createPlasterWallTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 64;
  canvas.height = 64;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  const plasterShades = ["#ECE7DF", "#E6E1D9", "#EAE5DD", "#E2DDD5", "#EDE9E2"];
  for (let x = 0; x < 64; x += 2) {
    for (let y = 0; y < 64; y += 2) {
      const idx = (x * 7 + y * 13) % plasterShades.length;
      ctx.fillStyle = plasterShades[idx];
      ctx.fillRect(x, y, 2, 2);
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.minFilter = THREE.NearestFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.generateMipmaps = false;
  return texture;
}

/**
 * Framed Landscape Wall Art (Mountains & Sunrise over pine forest)
 */
export function createFramedArtTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 128;
  canvas.height = 96;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  // Sky gradient
  const skyGrad = ctx.createLinearGradient(0, 0, 0, 70);
  skyGrad.addColorStop(0, "#1A2536"); // Twilight navy
  skyGrad.addColorStop(0.5, "#4A3B5C"); // Dusky purple
  skyGrad.addColorStop(0.85, "#D97D54"); // Warm dawn amber
  skyGrad.addColorStop(1, "#F3C68F"); // Golden horizon
  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, 128, 70);

  // Distant sun
  ctx.fillStyle = "#FFF2CC";
  ctx.beginPath();
  ctx.arc(88, 32, 9, 0, Math.PI * 2);
  ctx.fill();

  // Mountain range 1
  ctx.fillStyle = "#3B2E4A";
  ctx.beginPath();
  ctx.moveTo(10, 70);
  ctx.lineTo(44, 26);
  ctx.lineTo(80, 70);
  ctx.fill();

  // Mountain range 2
  ctx.fillStyle = "#222D3E";
  ctx.beginPath();
  ctx.moveTo(50, 70);
  ctx.lineTo(88, 32);
  ctx.lineTo(122, 70);
  ctx.fill();

  // Snowcap
  ctx.fillStyle = "#E8EEF5";
  ctx.beginPath();
  ctx.moveTo(44, 26);
  ctx.lineTo(36, 38);
  ctx.lineTo(52, 38);
  ctx.closePath();
  ctx.fill();

  // Pine forest silhouette (bottom band)
  ctx.fillStyle = "#121922";
  ctx.fillRect(0, 70, 128, 26);
  for (let x = 4; x < 124; x += 8) {
    const treeH = 14 + (x % 5) * 3;
    ctx.beginPath();
    ctx.moveTo(x + 4, 70 - treeH);
    ctx.lineTo(x, 70);
    ctx.lineTo(x + 8, 70);
    ctx.fill();
  }

  // Elegant dark oak frame border
  ctx.lineWidth = 6;
  ctx.strokeStyle = "#2D1D12";
  ctx.strokeRect(3, 3, 122, 90);

  // Inner gold trim line
  ctx.lineWidth = 1.5;
  ctx.strokeStyle = "#8C6A3C";
  ctx.strokeRect(7, 7, 114, 82);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  return texture;
}

/**
 * Hanging Wall Calendar with Month Header & Day 1 Highlight
 */
export function createWallCalendarTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 96;
  canvas.height = 128;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  // Calendar page white background
  ctx.fillStyle = "#FBFBFA";
  ctx.fillRect(0, 0, 96, 128);

  // Spiral / Wire binder top bar
  ctx.fillStyle = "#333333";
  ctx.fillRect(0, 0, 96, 8);
  for (let x = 8; x < 90; x += 10) {
    ctx.fillStyle = "#E0E0E0";
    ctx.fillRect(x, 2, 4, 10);
  }

  // Red Header Banner
  ctx.fillStyle = "#B33927";
  ctx.fillRect(0, 14, 96, 22);

  // Month Text
  ctx.font = "bold 13px 'Arial Black', sans-serif";
  ctx.fillStyle = "#FFFFFF";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("OCTOBER", 48, 25);

  // Days of Week Header
  const days = ["S", "M", "T", "W", "T", "F", "S"];
  ctx.font = "bold 8px monospace";
  ctx.fillStyle = "#666666";
  const colW = 12;
  const startX = 6;
  for (let i = 0; i < 7; i++) {
    ctx.fillText(days[i], startX + i * colW + colW / 2, 42);
  }

  // Horizontal separator
  ctx.fillStyle = "#E0E0E0";
  ctx.fillRect(6, 47, 84, 1);

  // Calendar Day Numbers Grid
  ctx.font = "7px sans-serif";
  let dayNum = 1;
  const rowH = 14;
  for (let row = 0; row < 5; row++) {
    for (let col = 0; col < 7; col++) {
      if (row === 0 && col < 2) continue;
      if (dayNum > 31) break;

      const cx = startX + col * colW + colW / 2;
      const cy = 54 + row * rowH;

      if (dayNum === 1) {
        ctx.fillStyle = "#B33927";
        ctx.beginPath();
        ctx.arc(cx, cy, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#FFFFFF";
        ctx.font = "bold 8px sans-serif";
        ctx.fillText(dayNum.toString(), cx, cy);
        ctx.font = "7px sans-serif";
      } else {
        ctx.fillStyle = "#333333";
        ctx.fillText(dayNum.toString(), cx, cy);
      }
      dayNum++;
    }
  }

  // Outer calendar border
  ctx.strokeStyle = "#D0CCC4";
  ctx.lineWidth = 2;
  ctx.strokeRect(1, 1, 94, 126);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  return texture;
}

/**
 * Authentic Crisp Linen / Cotton Bed-Sheet Texture
 */
export function createBedSheetTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 64;
  canvas.height = 64;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = false;

  // Crisp warm-ivory linen base
  const shades = ["#F4F0E8", "#EFEBE3", "#F7F3EB", "#ECE7DF"];
  for (let x = 0; x < 64; x += 2) {
    for (let y = 0; y < 64; y += 2) {
      const idx = (x * 5 + y * 11) % shades.length;
      ctx.fillStyle = shades[idx];
      ctx.fillRect(x, y, 2, 2);
    }
  }

  // Subtle woven grid lines
  ctx.fillStyle = "rgba(220, 214, 204, 0.4)";
  for (let i = 0; i < 64; i += 8) {
    ctx.fillRect(0, i, 64, 1);
    ctx.fillRect(i, 0, 1, 64);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.minFilter = THREE.NearestFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.generateMipmaps = false;
  return texture;
}

/**
 * 5:00 AM Dawn Outdoor Sky Texture (with stars and horizon glow)
 */
export function createDawnSkyTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 128;
  canvas.height = 128;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = true;

  const grad = ctx.createLinearGradient(0, 0, 0, 128);
  grad.addColorStop(0, "#080E1E"); // Deep space night
  grad.addColorStop(0.45, "#15243E"); // Dusky indigo
  grad.addColorStop(0.75, "#2C3D5A"); // 5 AM blue hour
  grad.addColorStop(0.92, "#5D5262"); // Pre-dawn mauve
  grad.addColorStop(1, "#A87258"); // Horizon dawn amber
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 128, 128);

  // Distant twinkling morning stars
  const stars = [
    [18, 14], [45, 22], [82, 10], [105, 28], [30, 40],
    [95, 48], [62, 32], [14, 52], [115, 16], [70, 18],
  ];
  ctx.fillStyle = "#FFFFFF";
  for (const [sx, sy] of stars) {
    ctx.globalAlpha = 0.7 + (sx % 3) * 0.15;
    ctx.fillRect(sx, sy, 1.5, 1.5);
  }
  ctx.globalAlpha = 1.0;

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  return texture;
}

/**
 * 2:00 AM Dark Midnight Outdoor Sky Texture
 * Features deep obsidian space, delicate starfield, and an atmospheric luminous moon
 * painted directly into the celestial canvas with radial bloom (not a hard sticker/decal).
 */
export function createMidnightSkyTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext("2d")!;
  ctx.imageSmoothingEnabled = true;

  // Deep midnight cosmic gradient
  const grad = ctx.createLinearGradient(0, 0, 0, 512);
  grad.addColorStop(0.0, "#010307"); // Pitch black space
  grad.addColorStop(0.45, "#040813"); // Deep navy void
  grad.addColorStop(0.80, "#071022"); // Subtle midnight atmospheric glow
  grad.addColorStop(1.0, "#0a152b"); // Low horizon twilight
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 512, 512);

  // 120+ crisp distant stars scattered across the celestial dome
  for (let i = 0; i < 140; i++) {
    const sx = (i * 97 + (i % 7) * 43) % 512;
    const sy = (i * 131 + (i % 11) * 37) % 480;
    const brightness = 0.35 + ((i % 5) * 0.15);
    const starSize = (i % 9 === 0) ? 2.0 : (i % 4 === 0) ? 1.5 : 1.0;

    ctx.fillStyle = (i % 8 === 0) ? "#d0e4ff" : (i % 12 === 0) ? "#fff6d9" : "#ffffff";
    ctx.globalAlpha = brightness;
    ctx.fillRect(sx, sy, starSize, starSize);
  }
  ctx.globalAlpha = 1.0;

  // Atmospheric Celestial Moon (Painted directly into the distant texture)
  // Positioned at (x: 340, y: 190) to align cleanly with upper window pane unobstructed by trees
  const moonX = 340;
  const moonY = 190;
  const moonRadius = 28;

  // 1. Wide diffuse celestial halo / atmospheric backscatter
  const wideGlow = ctx.createRadialGradient(moonX, moonY, moonRadius * 0.5, moonX, moonY, moonRadius * 3.5);
  wideGlow.addColorStop(0.0, "rgba(225, 238, 255, 0.35)");
  wideGlow.addColorStop(0.35, "rgba(180, 210, 255, 0.15)");
  wideGlow.addColorStop(0.70, "rgba(130, 170, 240, 0.05)");
  wideGlow.addColorStop(1.0, "rgba(100, 140, 220, 0.0)");
  ctx.fillStyle = wideGlow;
  ctx.beginPath();
  ctx.arc(moonX, moonY, moonRadius * 3.5, 0, Math.PI * 2);
  ctx.fill();

  // 2. Medium ambient moon corona
  const coronaGlow = ctx.createRadialGradient(moonX, moonY, moonRadius * 0.8, moonX, moonY, moonRadius * 1.6);
  coronaGlow.addColorStop(0.0, "rgba(255, 253, 240, 0.85)");
  coronaGlow.addColorStop(0.5, "rgba(240, 248, 255, 0.45)");
  coronaGlow.addColorStop(1.0, "rgba(200, 225, 255, 0.0)");
  ctx.fillStyle = coronaGlow;
  ctx.beginPath();
  ctx.arc(moonX, moonY, moonRadius * 1.6, 0, Math.PI * 2);
  ctx.fill();

  // 3. Luminous Moon Disc with soft edge antialiasing
  const discGrad = ctx.createRadialGradient(moonX - 4, moonY - 4, 2, moonX, moonY, moonRadius);
  discGrad.addColorStop(0.0, "#ffffff");
  discGrad.addColorStop(0.65, "#fbf8ec");
  discGrad.addColorStop(0.92, "#ede8d2");
  discGrad.addColorStop(1.0, "#d5d0b9");
  ctx.fillStyle = discGrad;
  ctx.beginPath();
  ctx.arc(moonX, moonY, moonRadius, 0, Math.PI * 2);
  ctx.fill();

  // 4. Subtle Lunar Maria (craters & seas for authentic celestial depth)
  ctx.fillStyle = "rgba(175, 170, 155, 0.32)";
  const craters = [
    [moonX - 7, moonY - 6, 5],
    [moonX + 6, moonY - 8, 4],
    [moonX - 4, moonY + 7, 6],
    [moonX + 8, moonY + 4, 5],
    [moonX + 2, moonY - 1, 3],
    [moonX - 11, moonY + 2, 4],
  ];
  for (const [cx, cy, cr] of craters) {
    ctx.beginPath();
    ctx.arc(cx, cy, cr, 0, Math.PI * 2);
    ctx.fill();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  return texture;
}

/**
 * Modern Dark Code Editor / IDE Screen Texture for Laptop
 */
export function createLaptopScreenTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 64;
  canvas.height = 40;
  const ctx = canvas.getContext("2d")!;

  // Background editor theme (Dark Navy / Slate)
  ctx.fillStyle = "#0f172a";
  ctx.fillRect(0, 0, 64, 40);

  // Left sidebar (File tree)
  ctx.fillStyle = "#090d16";
  ctx.fillRect(0, 0, 14, 40);

  // File tree items
  ctx.fillStyle = "#38bdf8";
  ctx.fillRect(2, 4, 8, 2);
  ctx.fillStyle = "#94a3b8";
  ctx.fillRect(4, 9, 7, 1);
  ctx.fillRect(4, 13, 8, 1);
  ctx.fillRect(4, 17, 6, 1);

  // Top tab bar
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(14, 0, 50, 5);
  ctx.fillStyle = "#38bdf8";
  ctx.fillRect(16, 1, 14, 3);

  // Editor syntax lines
  const lines = [
    { y: 8, x: 18, w: 10, c: "#f43f5e" },
    { y: 8, x: 30, w: 14, c: "#38bdf8" },
    { y: 12, x: 22, w: 8, c: "#c084fc" },
    { y: 12, x: 32, w: 18, c: "#4ade80" },
    { y: 16, x: 26, w: 16, c: "#fbbf24" },
    { y: 20, x: 26, w: 12, c: "#38bdf8" },
    { y: 20, x: 40, w: 10, c: "#94a3b8" },
    { y: 24, x: 22, w: 6, c: "#c084fc" },
    { y: 28, x: 18, w: 14, c: "#38bdf8" },
    { y: 32, x: 22, w: 22, c: "#4ade80" },
    { y: 36, x: 18, w: 4, c: "#f43f5e" },
  ];
  for (const l of lines) {
    ctx.fillStyle = l.c;
    ctx.fillRect(l.x, l.y, l.w, 1.5);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Clean Ruled Note Taking Paper / Notepad Texture
 */
export function createNotePaperTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 32;
  canvas.height = 40;
  const ctx = canvas.getContext("2d")!;

  // Warm cream paper
  ctx.fillStyle = "#faf7eb";
  ctx.fillRect(0, 0, 32, 40);

  // Top header margin (pale orange/gold header)
  ctx.fillStyle = "#fef08a";
  ctx.fillRect(0, 0, 32, 6);

  // Red left margin line
  ctx.fillStyle = "#f87171";
  ctx.fillRect(5, 0, 1, 40);

  // Thin blue horizontal ruled lines
  ctx.fillStyle = "#cbd5e1";
  for (let y = 10; y < 40; y += 4) {
    ctx.fillRect(0, y, 32, 1);
  }

  // Handwritten bullet points & notes (graphite grey)
  ctx.fillStyle = "#334155";
  ctx.fillRect(7, 8, 18, 1.5);
  ctx.fillRect(7, 12, 14, 1.2);
  ctx.fillRect(7, 16, 20, 1.2);
  ctx.fillRect(7, 20, 12, 1.2);
  ctx.fillRect(7, 24, 16, 1.2);
  ctx.fillRect(7, 28, 9, 1.2);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates futuristic holographic HUD telemetry plate for Scene 13 (Brain Energy Conservation).
 */
export function createBrainTelemetryTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 160;
  const ctx = canvas.getContext("2d")!;

  // Translucent dark cyber glass background
  ctx.fillStyle = "rgba(6, 12, 22, 0.92)";
  ctx.fillRect(0, 0, 512, 160);

  // Outer glowing neon cyan border
  ctx.strokeStyle = "#00f0ff";
  ctx.lineWidth = 4;
  ctx.strokeRect(4, 4, 504, 152);

  // Corner brackets
  ctx.fillStyle = "#00f0ff";
  ctx.fillRect(4, 4, 18, 6);
  ctx.fillRect(4, 4, 6, 18);
  ctx.fillRect(490, 4, 18, 6);
  ctx.fillRect(502, 4, 6, 18);
  ctx.fillRect(4, 150, 18, 6);
  ctx.fillRect(4, 138, 6, 18);
  ctx.fillRect(490, 150, 18, 6);
  ctx.fillRect(502, 138, 6, 18);

  // Top header telemetry label
  ctx.fillStyle = "#80ffff";
  ctx.font = "bold 20px 'Arial Black', Impact, sans-serif";
  ctx.fillText("HOMEOSTASIS TELEMETRY", 24, 38);

  // Main status metric
  ctx.fillStyle = "#ffffff";
  ctx.font = "900 28px 'Arial Black', Impact, sans-serif";
  ctx.fillText("ENERGY CONSERVED: 94%", 24, 82);

  // Visual battery segments
  ctx.fillStyle = "#00ffaa";
  for (let b = 0; b < 10; b++) {
    ctx.fillRect(24 + b * 22, 102, 18, 14);
  }

  // Survival Mode pill
  ctx.fillStyle = "#ffaa00";
  ctx.font = "bold 18px 'Arial Black', Impact, sans-serif";
  ctx.fillText("[SURVIVAL PROTOCOL: ACTIVE]", 250, 116);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates emergency status screen texture for Scene 14 (Biological Alarm).
 */
export function createEmergencyAlarmTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 256;
  const ctx = canvas.getContext("2d")!;

  // Deep crimson emergency bunker screen background
  ctx.fillStyle = "#1e0408";
  ctx.fillRect(0, 0, 512, 256);

  // Top & bottom hazard chevron striping
  const chevronW = 24;
  for (let x = 0; x < 512; x += chevronW * 2) {
    ctx.fillStyle = "#ffcc00";
    ctx.fillRect(x, 0, chevronW, 20);
    ctx.fillRect(x, 236, chevronW, 20);
    ctx.fillStyle = "#111111";
    ctx.fillRect(x + chevronW, 0, chevronW, 20);
    ctx.fillRect(x + chevronW, 236, chevronW, 20);
  }

  // Neon crimson glowing border
  ctx.strokeStyle = "#ff0033";
  ctx.lineWidth = 4;
  ctx.strokeRect(6, 24, 500, 208);

  // Header tag
  ctx.fillStyle = "#ff5577";
  ctx.font = "bold 18px 'Arial Black', Impact, sans-serif";
  ctx.fillText("! SYSTEM ALERT // LEVEL 5 OVERLOAD !", 28, 56);

  // Massive Alarm Title
  ctx.fillStyle = "#ffffff";
  ctx.font = "900 32px 'Arial Black', Impact, sans-serif";
  ctx.fillText("HOMEOSTATIC ALARM", 28, 104);

  // Warning body
  ctx.fillStyle = "#ff2244";
  ctx.font = "bold 22px 'Arial Black', Impact, sans-serif";
  ctx.fillText("BIOLOGY IN REJECTION CASCADE", 28, 148);

  // Subtext status
  ctx.fillStyle = "#ffd700";
  ctx.font = "bold 18px monospace";
  ctx.fillText("DRIFT DETECTED: FORCE EXHAUSTION", 28, 186);

  ctx.fillStyle = "#ff0033";
  ctx.fillRect(28, 200, 456, 16);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates industrial gym banner for Scene 15 ("SUPERHUMAN DISCIPLINE").
 */
export function createGymBannerTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 128;
  const ctx = canvas.getContext("2d")!;

  // Heavy dark steel plate background
  ctx.fillStyle = "#18181c";
  ctx.fillRect(0, 0, 512, 128);

  // Red accent border
  ctx.strokeStyle = "#d32f2f";
  ctx.lineWidth = 4;
  ctx.strokeRect(4, 4, 504, 120);

  // Corner rivets
  ctx.fillStyle = "#666666";
  for (const rx of [16, 496]) {
    for (const ry of [16, 112]) {
      ctx.beginPath();
      ctx.arc(rx, ry, 6, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Header
  ctx.fillStyle = "#ffcc00";
  ctx.font = "bold 18px 'Arial Black', Impact, sans-serif";
  ctx.fillText("IRON FORGE GYM // EXTREME STRAIN", 28, 42);

  // Main bold slogan
  ctx.fillStyle = "#ffffff";
  ctx.font = "900 32px 'Arial Black', Impact, sans-serif";
  ctx.fillText("NO DAYS OFF", 28, 86);

  ctx.fillStyle = "#d32f2f";
  ctx.font = "bold 16px 'Arial Black', Impact, sans-serif";
  ctx.fillText("SUPERHUMAN DISCIPLINE", 270, 86);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates heavy reinforced blast door texture for Scene 16 ("THE ELIMINATION GATEWAY").
 */
export function createLockedBlastDoorTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext("2d")!;

  // Dark graphite steel plate background
  ctx.fillStyle = "#1e222b";
  ctx.fillRect(0, 0, 512, 512);

  // Outer chamfered border
  ctx.strokeStyle = "#383f50";
  ctx.lineWidth = 12;
  ctx.strokeRect(10, 10, 492, 492);

  // Hazard diagonal caution bands at top and bottom
  const drawHazardStripes = (y: number, h: number) => {
    ctx.save();
    ctx.beginPath();
    ctx.rect(16, y, 480, h);
    ctx.clip();
    ctx.fillStyle = "#11141a";
    ctx.fillRect(16, y, 480, h);
    ctx.fillStyle = "#ff5533";
    for (let x = -50; x < 550; x += 36) {
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + 20, y);
      ctx.lineTo(x - 10, y + h);
      ctx.lineTo(x - 30, y + h);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();
  };
  drawHazardStripes(20, 36);
  drawHazardStripes(456, 36);

  // Central recessed lock vault panel
  ctx.fillStyle = "#12151b";
  ctx.fillRect(80, 100, 352, 312);
  ctx.strokeStyle = "#ff2a4d";
  ctx.lineWidth = 4;
  ctx.strokeRect(80, 100, 352, 312);

  // Big Glowing Red Lock Icon
  ctx.strokeStyle = "#ff2a4d";
  ctx.fillStyle = "#ff2a4d";
  ctx.lineWidth = 8;
  // Shackle
  ctx.beginPath();
  ctx.arc(256, 190, 44, Math.PI, 0, false);
  ctx.stroke();
  // Body
  ctx.fillRect(206, 190, 100, 80);
  // Keyhole
  ctx.fillStyle = "#12151b";
  ctx.beginPath();
  ctx.arc(256, 222, 10, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillRect(252, 222, 8, 22);

  // Warning text
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 20px 'Arial Black', Impact, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("CHOICE // ELIMINATED", 256, 320);

  ctx.fillStyle = "#ff2a4d";
  ctx.font = "bold 16px 'Arial Black', Impact, sans-serif";
  ctx.fillText("STATUS: PERMANENTLY SEALED", 256, 354);

  ctx.fillStyle = "#6b7c96";
  ctx.font = "bold 12px sans-serif";
  ctx.fillText("DISTRACTION CORRIDOR CLOSED", 256, 384);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates crisp 7:00 AM digital alarm clock display for Scene 17 ("NO NEGOTIATION AT 7 AM").
 */
export function createSevenAMClockTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 256;
  const ctx = canvas.getContext("2d")!;

  // Deep matte black beveled screen background
  ctx.fillStyle = "#0a0c10";
  ctx.fillRect(0, 0, 512, 256);

  // Subtle bezel frame
  ctx.strokeStyle = "#242a38";
  ctx.lineWidth = 8;
  ctx.strokeRect(6, 6, 500, 244);

  // Top header status row
  ctx.fillStyle = "#00f0ff";
  ctx.font = "bold 15px 'Arial Black', Impact, sans-serif";
  ctx.fillText("ALARM // WAKE CYCLE", 32, 42);

  ctx.fillStyle = "#55bb66";
  ctx.textAlign = "right";
  ctx.fillText("DISMISSED ON TIME", 480, 42);

  // Huge Glowing Amber Digital Numbers "07:00"
  ctx.textAlign = "center";
  ctx.fillStyle = "#ff9900";
  ctx.shadowColor = "#ff9900";
  ctx.shadowBlur = 18;
  ctx.font = "900 102px 'Arial Black', Impact, sans-serif";
  ctx.fillText("07:00", 240, 150);
  ctx.shadowBlur = 0; // Reset shadow

  // AM Badge
  ctx.fillStyle = "#ffaa22";
  ctx.font = "bold 26px 'Arial Black', Impact, sans-serif";
  ctx.fillText("AM", 420, 142);

  // Bottom rule status
  ctx.strokeStyle = "rgba(255, 153, 0, 0.3)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(32, 178);
  ctx.lineTo(480, 178);
  ctx.stroke();

  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 16px 'Arial Black', Impact, sans-serif";
  ctx.fillText("NEGOTIATION: ZERO // ACTION: IMMEDIATE", 256, 215);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates active dark-mode IDE / prose editor screen for Scene 18 ("NO MOOD WAITING").
 */
export function createLaptopIDETexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 340;
  const ctx = canvas.getContext("2d")!;

  // Dark slate code editor background
  ctx.fillStyle = "#12161f";
  ctx.fillRect(0, 0, 512, 340);

  // Top window header & tabs
  ctx.fillStyle = "#1c2230";
  ctx.fillRect(0, 0, 512, 36);

  // Window control dots
  ctx.fillStyle = "#ff5f56";
  ctx.beginPath();
  ctx.arc(18, 18, 5, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#ffbd2e";
  ctx.beginPath();
  ctx.arc(36, 18, 5, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#27c93f";
  ctx.beginPath();
  ctx.arc(54, 18, 5, 0, Math.PI * 2);
  ctx.fill();

  // Tab
  ctx.fillStyle = "#12161f";
  ctx.fillRect(80, 6, 170, 30);
  ctx.fillStyle = "#00f0ff";
  ctx.font = "bold 13px monospace";
  ctx.fillText("routine_execute.ts", 95, 26);

  // Line numbers gutter
  ctx.fillStyle = "#3a465c";
  ctx.font = "14px monospace";
  for (let i = 1; i <= 8; i++) {
    ctx.fillText(`0${i}`, 14, 46 + i * 28);
  }

  // Code lines
  ctx.font = "14px monospace";
  // Line 1: Comment
  ctx.fillStyle = "#5c6e8a";
  ctx.fillText("// Rule: Action precedes emotion", 50, 74);

  // Line 2: function declaration
  ctx.fillStyle = "#c792ea";
  ctx.fillText("async function ", 50, 102);
  ctx.fillStyle = "#82aaff";
  ctx.fillText("startWorkWithoutWaiting() {", 168, 102);

  // Line 3: mood check
  ctx.fillStyle = "#f78c6c";
  ctx.fillText("  const moodReady = ", 50, 130);
  ctx.fillStyle = "#ff5370";
  ctx.fillText("false;", 200, 130);
  ctx.fillStyle = "#5c6e8a";
  ctx.fillText(" // Irrelevant", 255, 130);

  // Line 4: execution
  ctx.fillStyle = "#89ddff";
  ctx.fillText("  await keyboard.strikeFirstWord();", 50, 158);

  // Line 5: flow state
  ctx.fillStyle = "#c3e88d";
  ctx.fillText("  return FlowState.IMMEDIATE;", 50, 186);

  // Line 6: closure
  ctx.fillStyle = "#82aaff";
  ctx.fillText("}", 50, 214);

  // Blinking cyan cursor
  ctx.fillStyle = "#00f0ff";
  ctx.fillRect(66, 226, 9, 18);

  // Bottom metric status banner
  ctx.fillStyle = "#090c12";
  ctx.fillRect(0, 296, 512, 44);

  ctx.fillStyle = "#00f0ff";
  ctx.font = "bold 13px 'Arial Black', Impact, sans-serif";
  ctx.fillText("STATUS: 100% EXECUTING", 18, 324);

  ctx.fillStyle = "#ffaa00";
  ctx.textAlign = "right";
  ctx.fillText("MOOD DEPENDENCY: 0%", 494, 324);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates architectural blueprint schematic for Scene 19 ("ENGINEER THE ENVIRONMENT").
 */
export function createBlueprintSchematicTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext("2d")!;

  // Blueprint navy background
  ctx.fillStyle = "#071b30";
  ctx.fillRect(0, 0, 512, 512);

  // Fine cyan grid lines
  ctx.strokeStyle = "rgba(0, 240, 255, 0.15)";
  ctx.lineWidth = 1;
  for (let p = 0; p <= 512; p += 32) {
    ctx.beginPath();
    ctx.moveTo(p, 0);
    ctx.lineTo(p, 512);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, p);
    ctx.lineTo(512, p);
    ctx.stroke();
  }

  // Outer blueprint border
  ctx.strokeStyle = "#00f0ff";
  ctx.lineWidth = 4;
  ctx.strokeRect(16, 16, 480, 480);

  // Title block
  ctx.fillStyle = "#00f0ff";
  ctx.font = "900 20px 'Arial Black', Impact, sans-serif";
  ctx.fillText("ENVIRONMENTAL ARCHITECTURE SPEC", 36, 54);

  ctx.fillStyle = "rgba(0, 240, 255, 0.7)";
  ctx.font = "bold 13px monospace";
  ctx.fillText("SCHEMATIC // MINIMAL ACTIVATION ENERGY", 36, 76);

  // Flow Pathway Schematics (Floorplan boxes)
  const drawModule = (x: number, y: number, w: number, h: number, title: string, subtitle: string) => {
    ctx.fillStyle = "#0d2b4a";
    ctx.fillRect(x, y, w, h);
    ctx.strokeStyle = "#00f0ff";
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, w, h);

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 14px 'Arial Black', Impact, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(title, x + w / 2, y + 26);

    ctx.fillStyle = "#00f0ff";
    ctx.font = "bold 11px monospace";
    ctx.fillText(subtitle, x + w / 2, y + 44);
  };

  drawModule(48, 120, 180, 60, "1. PHONE VAULT", "ANOTHER ROOM");
  drawModule(284, 120, 180, 60, "2. SNEAKERS", "DIRECTLY AT DOOR");
  drawModule(166, 240, 180, 60, "3. WORKSPACE", "BLANK DOC READY");

  // Glowing connector arrows
  ctx.strokeStyle = "#ffcc00";
  ctx.lineWidth = 3;
  // Arrow 1 to 2
  ctx.beginPath();
  ctx.moveTo(228, 150);
  ctx.lineTo(284, 150);
  ctx.stroke();
  // Arrow 2 to 3
  ctx.beginPath();
  ctx.moveTo(374, 180);
  ctx.lineTo(374, 270);
  ctx.lineTo(346, 270);
  ctx.stroke();

  // Metric Callouts
  ctx.textAlign = "left";
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 16px 'Arial Black', Impact, sans-serif";
  ctx.fillText("FRICTION COEFFICIENT: 0.02 (OPTIMAL)", 48, 360);

  ctx.fillStyle = "#55dd88";
  ctx.font = "bold 14px monospace";
  ctx.fillText("> INITIATION EFFORT < GUILT THRESHOLD", 48, 390);

  ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
  ctx.font = "12px monospace";
  ctx.fillText("DECISION POINTS ELIMINATED: 100%", 48, 418);
  ctx.fillText("MOMENTUM CONSERVATION: MAXIMUM", 48, 442);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates phone isolation vault screen for Scene 20 ("PHONE IN ANOTHER ROOM").
 */
export function createPhoneLockedTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 512;
  const ctx = canvas.getContext("2d")!;

  // OLED Deep black phone screen
  ctx.fillStyle = "#05070a";
  ctx.fillRect(0, 0, 256, 512);

  // Subtle rounded phone glass frame
  ctx.strokeStyle = "rgba(0, 240, 255, 0.4)";
  ctx.lineWidth = 4;
  ctx.strokeRect(6, 6, 244, 500);

  // Time header
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 20px 'Arial Black', Impact, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("07:15", 128, 54);

  // Big Glowing Padlock
  ctx.strokeStyle = "#00f0ff";
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.arc(128, 160, 32, Math.PI, 0, false);
  ctx.stroke();
  ctx.fillStyle = "#00f0ff";
  ctx.fillRect(92, 160, 72, 60);

  // Keyhole
  ctx.fillStyle = "#05070a";
  ctx.beginPath();
  ctx.arc(128, 185, 8, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillRect(125, 185, 6, 18);

  // Isolation Status
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 16px 'Arial Black', Impact, sans-serif";
  ctx.fillText("PHONE ISOLATED", 128, 270);

  ctx.fillStyle = "#ffaa00";
  ctx.font = "bold 13px 'Arial Black', Impact, sans-serif";
  ctx.fillText("LOCATION: LIVING ROOM", 128, 304);

  ctx.fillStyle = "#55bb66";
  ctx.font = "bold 12px monospace";
  ctx.fillText("NOTIFICATIONS: 0", 128, 340);
  ctx.fillText("DISTRACTION: ZERO", 128, 366);

  // Bottom bar
  ctx.fillStyle = "rgba(255, 255, 255, 0.3)";
  ctx.fillRect(80, 470, 96, 5);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates pristine blank document page for Scene 20 ("BLANK DOCUMENT OPEN BEFORE BED").
 */
export function createBlankDocTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 340;
  const ctx = canvas.getContext("2d")!;

  // Clean soft white paper background
  ctx.fillStyle = "#fafbfe";
  ctx.fillRect(0, 0, 512, 340);

  // Document window top chrome
  ctx.fillStyle = "#e8ecf4";
  ctx.fillRect(0, 0, 512, 32);

  ctx.fillStyle = "#2b3445";
  ctx.font = "bold 13px sans-serif";
  ctx.fillText("Untitled Document — Ready to Write", 20, 21);

  // Clean document page margins
  ctx.fillStyle = "#222634";
  ctx.font = "900 24px 'Arial Black', Impact, sans-serif";
  ctx.fillText("CHAPTER 1: THE CONSISTENCY PARADOX", 42, 86);

  ctx.fillStyle = "#55627a";
  ctx.font = "bold 15px sans-serif";
  ctx.fillText("The secret of momentum is lowering activation friction.", 42, 122);

  // Golden glowing cursor at beginning of next sentence
  ctx.fillStyle = "#ffaa00";
  ctx.fillRect(42, 146, 3, 24);

  // Ghost placeholder line indicating ready for thought
  ctx.fillStyle = "#c5cfde";
  ctx.font = "italic 15px sans-serif";
  ctx.fillText("Type one clean sentence to begin...", 50, 164);

  // Subtle bottom status bar
  ctx.fillStyle = "#e8ecf4";
  ctx.fillRect(0, 310, 512, 30);
  ctx.fillStyle = "#6b7a94";
  ctx.font = "bold 11px monospace";
  ctx.fillText("WORDS: 0 | CURSOR ACTIVE | ZERO FRICTION", 20, 329);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates etched brass plaque for Scene 22 ("STOP AIMING FOR EXHAUSTING DAYS").
 */
export function createBrokenTrophyPlaqueTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 128;
  const ctx = canvas.getContext("2d")!;

  // Scratched weathered brass base
  ctx.fillStyle = "#8a7332";
  ctx.fillRect(0, 0, 256, 128);

  ctx.strokeStyle = "#4a3c14";
  ctx.lineWidth = 4;
  ctx.strokeRect(6, 6, 244, 116);

  // Etched text with crack lines
  ctx.fillStyle = "#2a220a";
  ctx.font = "bold 15px 'Arial Black', Impact, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("HEROIC WEEK: FAILED", 128, 44);

  ctx.font = "bold 12px sans-serif";
  ctx.fillStyle = "#a82b2b";
  ctx.fillText("DIED OF BURNOUT — FRIDAY", 128, 72);

  ctx.font = "italic 10px sans-serif";
  ctx.fillStyle = "#3d3216";
  ctx.fillText("COST: 100% DISCIPLINE DEPLETED", 128, 98);

  // Fracture lines across plaque
  ctx.strokeStyle = "#1a1505";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(30, 10);
  ctx.lineTo(95, 65);
  ctx.lineTo(135, 60);
  ctx.lineTo(210, 120);
  ctx.stroke();

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates neon micro-meter sign for Scene 23 ("LOWER THE BARRIER").
 */
export function createTinyHurdleSignTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 384;
  canvas.height = 160;
  const ctx = canvas.getContext("2d")!;

  // Slate tech badge background
  ctx.fillStyle = "#0c121e";
  ctx.fillRect(0, 0, 384, 160);

  ctx.strokeStyle = "#00f0ff";
  ctx.lineWidth = 4;
  ctx.strokeRect(6, 6, 372, 148);

  ctx.fillStyle = "#00f0ff";
  ctx.font = "bold 20px 'Arial Black', Impact, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("BARRIER HEIGHT: 2 INCHES", 192, 45);

  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 15px sans-serif";
  ctx.fillText("RESISTANCE: RIDICULOUS", 192, 82);

  // Activation Energy Gauge
  ctx.fillStyle = "rgba(0, 240, 255, 0.2)";
  ctx.fillRect(40, 105, 304, 18);
  ctx.fillStyle = "#00ff88";
  ctx.fillRect(40, 105, 18, 18); // Barely 5% filled

  ctx.fillStyle = "#00ff88";
  ctx.font = "bold 12px monospace";
  ctx.fillText("ACTIVATION ENERGY: 0.1%", 192, 142);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates notebook page for Scene 24 ("WRITE ONE CLEAN PARAGRAPH").
 */
export function createTwoMinuteNotebookTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext("2d")!;

  // Cream linen paper
  ctx.fillStyle = "#fcf9f2";
  ctx.fillRect(0, 0, 512, 512);

  // Left margin red line
  ctx.strokeStyle = "#e8a0a0";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(70, 0);
  ctx.lineTo(70, 512);
  ctx.stroke();

  // Subtle ruled lines
  ctx.strokeStyle = "#e0e4ec";
  ctx.lineWidth = 1;
  for (let y = 60; y < 500; y += 34) {
    ctx.beginPath();
    ctx.moveTo(40, y);
    ctx.lineTo(490, y);
    ctx.stroke();
  }

  // Handwritten ink title
  ctx.fillStyle = "#1e2838";
  ctx.font = "bold 24px 'Arial Black', Impact, sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("THE TWO-MINUTE RULE", 85, 95);

  // The single clean paragraph
  ctx.fillStyle = "#2c3b52";
  ctx.font = "17px sans-serif";
  ctx.fillText("1. Sit in the chair for two minutes.", 85, 163);
  ctx.fillText("2. Write one clean paragraph.", 85, 197);
  ctx.fillText("3. Put on the sneakers and step outside.", 85, 231);

  ctx.fillStyle = "#0099ff";
  ctx.font = "bold 15px sans-serif";
  ctx.fillText("Action lowers friction. Momentum follows.", 85, 299);

  // Big gold completion stamp
  ctx.strokeStyle = "#d4af37";
  ctx.lineWidth = 4;
  ctx.strokeRect(280, 370, 190, 80);
  ctx.fillStyle = "#b89018";
  ctx.font = "bold 18px 'Arial Black', Impact, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("PARAGRAPH: DONE", 375, 405);
  ctx.font = "bold 12px sans-serif";
  ctx.fillText("MOMENTUM UNLOCKED", 375, 432);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}

/**
 * Generates golden coin face for Scene 25 ("CAST ONE SMALL VOTE").
 */
export function createGoldenScaleCoinTexture(): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 256;
  const ctx = canvas.getContext("2d")!;

  // Circular golden metallic relief
  const grad = ctx.createRadialGradient(128, 128, 10, 128, 128, 120);
  grad.addColorStop(0, "#fff2a8");
  grad.addColorStop(0.5, "#e6b800");
  grad.addColorStop(1, "#997300");
  ctx.fillStyle = grad;
  ctx.beginPath();
  ctx.arc(128, 128, 120, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = "#ffd700";
  ctx.lineWidth = 6;
  ctx.stroke();

  // Inner beveled rim
  ctx.strokeStyle = "#664d00";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(128, 128, 102, 0, Math.PI * 2);
  ctx.stroke();

  // Center Emblem: Winged Torch of Momentum
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.arc(128, 90, 18, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#3d2b00";
  ctx.font = "bold 20px 'Arial Black', Impact, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("ONE SMALL VOTE", 128, 150);

  ctx.font = "bold 12px sans-serif";
  ctx.fillText("NEW IDENTITY", 128, 178);
  ctx.fillText("MOMENTUM", 128, 198);

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.NearestFilter;
  return texture;
}
