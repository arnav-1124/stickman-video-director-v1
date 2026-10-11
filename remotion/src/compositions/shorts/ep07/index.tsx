import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/**
 * High-End 2D Motion Graphics Affine Camera Rig
 * 
 * Mathematically transforms the 1080x1920 canvas so that the composition remains
 * fully visible without cropping out critical artwork elements, titles, or characters.
 * Zooms are tuned conservatively (1.00x - 1.08x) with subtle, organic camera glides.
 */
function getCameraMatrix(camX: number, camY: number, zoom: number) {
  return `translate(540px, 960px) scale(${zoom}) translate(${-camX}px, ${-camY}px)`;
}

export const Ep07FullComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // =========================================================================
  // TIMELINE BEATS (Total: 1575 frames = 52.50s @ 30fps)
  // Shot 01: Frames    0 -   35 (0.00s -  1.15s) -> Bed Hook: "Before you scroll,"
  // Shot 02: Frames   35 -  125 (1.15s -  4.15s) -> Brain & Flask: "dopamine is not the pleasure chemical..."
  // Shot 03: Frames  125 -  189 (4.15s -  6.31s) -> Smiley & Deadpan: "You think it makes you feel happy..."
  // Shot 04: Frames  189 -  303 (6.31s - 10.10s) -> Spinning Clock & Slumped Couch: "If dopamine was pleasure..."
  // Shot 05: Frames  303 -  417 (10.10s - 13.91s) -> 1% Battery & Exhausted Sticky: "Instead, you feel completely empty..."
  // Shot 06: Frames  417 -  486 (13.91s - 16.20s) -> Einstein & Blackboard: "Neuroscientists proved this..."
  // Shot 07: Frames  486 -  555 (16.20s - 18.50s) -> Reward Box & Flatline: "dopamine doesn't spike when you get a reward."
  // Shot 08: Frames  555 -  632 (18.50s - 21.06s) -> Hand & Anticipation Spike: "It spikes right before—anticipation."
  // Shot 09: Frames  632 -  702 (21.06s - 23.40s) -> "THE ITCH" & Temple Clutch: "It is an itch."
  // Shot 10: Frames  702 -  753 (23.40s - 25.10s) -> Sticky & Whispering Demon: "A biological itch that whispers:"
  // Shot 11: Frames  753 -  846 (25.10s - 28.21s) -> Treadmill & Golden Play Button: "just one more video..."
  // Shot 12: Frames  846 -  963 (28.21s - 32.10s) -> Dials & Pull-Refresh: "floods with craving, not fulfillment."
  // Shot 13: Frames  963 - 1032 (32.10s - 34.40s) -> Split Screen Caveman vs Modern: "hijacked this ancient hunting reflex..."
  // Shot 14: Frames 1032 - 1110 (34.40s - 37.00s) -> Hypnotized Sticky & Slot Machine: "slot machine in your pocket."
  // Shot 15: Frames 1110 - 1158 (37.00s - 38.60s) -> Phone on Desk & Crossed Arms: "Here’s how you take control."
  // Shot 16: Frames 1158 - 1245 (38.60s - 41.50s) -> Banner & Green 20s Shield: "twenty seconds of friction..."
  // Shot 17: Frames 1245 - 1293 (41.50s - 43.10s) -> Desk Phone & Doorway Departure: "phone in another room,"
  // Shot 18: Frames 1293 - 1397 (43.10s - 46.56s) -> Open Window & Dissolving Flame: "craving burn out."
  // Shot 19: Frames 1397 - 1479 (46.56s - 49.30s) -> Phone Zombies & Calm Sticky: "Real power isn't feeding the itch..."
  // Shot 20: Frames 1479 - 1575 (49.30s - 52.50s) -> Meditating Bench & Halo: "sit in stillness..."
  // =========================================================================

  // Seamless 4-frame crossfade
  const getCrossfade = (start: number, end: number) => {
    const fadeIn = interpolate(frame, [start, start + 4], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    const fadeOut = interpolate(frame, [end - 4, end], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    return Math.min(fadeIn, fadeOut);
  };

  // --- SHOT 01: BED HOOK (Frames 0 - 35) ---
  // Subtle push to phone while keeping full room and stop hand in frame
  const s01Prog = interpolate(frame, [0, 35], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const s01CamX = interpolate(s01Prog, [0, 1], [540, 560]);
  const s01CamY = interpolate(s01Prog, [0, 1], [960, 920]);
  const s01Zoom = interpolate(s01Prog, [0, 1], [1.00, 1.06]);

  // --- SHOT 02: BRAIN & FLASK "FALSE!" (Frames 35 - 125) ---
  // Both brain and flask remain 100% visible on screen; subtle drift rightward toward flask
  const s02Local = frame - 35;
  const s02Glide = interpolate(s02Local, [15, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s02CamX = interpolate(s02Glide, [0, 1], [520, 565]);
  const s02CamY = interpolate(s02Glide, [0, 1], [960, 975]);
  const s02Zoom = interpolate(s02Glide, [0, 1], [1.02, 1.07]);

  // --- SHOT 03: SMILEY & DEADPAN EYES (Frames 125 - 189) ---
  // Keeps both Sticky's head and the crossed-out smiley bubble completely in frame
  const s03Local = frame - 125;
  const s03Glide = interpolate(s03Local, [10, 55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.22, 1.0, 0.36, 1.0),
  });
  const s03CamX = interpolate(s03Glide, [0, 1], [550, 520]);
  const s03CamY = interpolate(s03Glide, [0, 1], [960, 920]);
  const s03Zoom = interpolate(s03Glide, [0, 1], [1.02, 1.08]);

  // --- SHOT 04: CLOCK & SLUMPED COUCH (Frames 189 - 303) ---
  // Full view: Spinning clock at top, floating cards in middle, Sticky slumped at bottom
  const s04Local = frame - 189;
  const s04Pan = interpolate(s04Local, [20, 90], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s04CamX = interpolate(s04Pan, [0, 1], [530, 550]);
  const s04CamY = interpolate(s04Pan, [0, 1], [900, 980]);
  const s04Zoom = interpolate(s04Pan, [0, 1], [1.02, 1.06]);

  // --- SHOT 05: 1% BATTERY & EXHAUSTED STICKY (Frames 303 - 417) ---
  // Battery overhead and Sticky's exhausted body on mattress remain completely in frame
  const s05Local = frame - 303;
  const s05Tilt = interpolate(s05Local, [20, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.25, 1.0, 0.5, 1.0),
  });
  const s05CamX = 540;
  const s05CamY = interpolate(s05Tilt, [0, 1], [910, 960]);
  const s05Zoom = interpolate(s05Tilt, [0, 1], [1.02, 1.07]);

  // --- SHOT 06: EINSTEIN & BLACKBOARD BRAIN (Frames 417 - 486) ---
  // Full lecture scene: Einstein with pointer on left and brain chalkboard on right both in view
  const s06Local = frame - 417;
  const s06Follow = interpolate(s06Local, [10, 55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.quad),
  });
  const s06CamX = interpolate(s06Follow, [0, 1], [510, 555]);
  const s06CamY = interpolate(s06Follow, [0, 1], [960, 935]);
  const s06Zoom = interpolate(s06Follow, [0, 1], [1.02, 1.06]);

  // --- SHOT 07: REWARD BOX & FLATLINE GRAPH (Frames 486 - 555) ---
  // Keeps both the open gift box and the flatline graph below in clear view
  const s07Local = frame - 486;
  const s07Drop = interpolate(s07Local, [15, 55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s07CamX = 540;
  const s07CamY = interpolate(s07Drop, [0, 1], [920, 975]);
  const s07Zoom = interpolate(s07Drop, [0, 1], [1.02, 1.07]);

  // --- SHOT 08: HAND & ANTICIPATION SPIKE (Frames 555 - 632) ---
  // Hand hovering at bottom and soaring red anticipation spike at top are both visible
  const s08Local = frame - 555;
  const s08Surge = interpolate(s08Local, [15, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.12, 0.9, 0.25, 1.0),
  });
  const s08CamX = interpolate(s08Surge, [0, 1], [520, 555]);
  const s08CamY = interpolate(s08Surge, [0, 1], [990, 920]);
  const s08Zoom = interpolate(s08Surge, [0, 1], [1.02, 1.07]);

  // --- SHOT 09: "THE ITCH" & TEMPLE CLUTCH (Frames 632 - 702) ---
  // Heading "THE ITCH", Sticky's head, and rash bubble remain fully visible
  const s09Local = frame - 632;
  const s09Punch = interpolate(s09Local, [10, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const s09CamX = 540;
  const s09CamY = interpolate(s09Punch, [0, 1], [910, 955]);
  const s09Zoom = interpolate(s09Punch, [0, 1], [1.02, 1.07]);

  // --- SHOT 10: STICKY & WHISPERING DEMON (Frames 702 - 753) ---
  // Both Sticky and the shadowy demon whispering in his ear remain completely in frame
  const s10Local = frame - 702;
  const s10Glide = interpolate(s10Local, [0, 51], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.quad),
  });
  const s10CamX = interpolate(s10Glide, [0, 1], [560, 520]);
  const s10CamY = interpolate(s10Glide, [0, 1], [960, 940]);
  const s10Zoom = interpolate(s10Glide, [0, 1], [1.02, 1.07]);

  // --- SHOT 11: TREADMILL & GOLDEN PLAY BUTTON (Frames 753 - 846) ---
  // Running Sticky, circular hamster treadmill, and dangling golden button all visible
  const s11Local = frame - 753;
  const s11Track = interpolate(s11Local, [15, 75], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s11CamX = interpolate(s11Track, [0, 1], [520, 560]);
  const s11CamY = 960;
  const s11Zoom = interpolate(s11Track, [0, 1], [1.02, 1.07]);

  // --- SHOT 12: DIALS & PULL-REFRESH (Frames 846 - 963) ---
  // Craving dial at top, 0% Fulfillment bar, and pulling thumb at bottom are all visible
  const s12Local = frame - 846;
  const s12Glide = interpolate(s12Local, [20, 90], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s12CamX = 540;
  const s12CamY = interpolate(s12Glide, [0, 1], [910, 970]);
  const s12Zoom = interpolate(s12Glide, [0, 1], [1.02, 1.07]);

  // --- SHOT 13: SPLIT SCREEN (CAVEMAN vs MODERN) (Frames 963 - 1032) ---
  // FULL SPLIT-SCREEN VISIBILITY: Both Caveman on left and Modern scroller on right stay visible!
  const s13Local = frame - 963;
  const s13Glide = interpolate(s13Local, [15, 55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s13CamX = interpolate(s13Glide, [0, 1], [510, 570]);
  const s13CamY = 960;
  const s13Zoom = 1.03; // Conservative zoom so split-screen contrast is 100% clear!

  // --- SHOT 14: HYPNOTIZED STICKY & SLOT MACHINE (Frames 1032 - 1110) ---
  // Sticky on left and giant slot machine smartphone on right both remain in view
  const s14Local = frame - 1032;
  const s14Pan = interpolate(s14Local, [15, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s14CamX = interpolate(s14Pan, [0, 1], [510, 560]);
  const s14CamY = interpolate(s14Pan, [0, 1], [960, 940]);
  const s14Zoom = interpolate(s14Pan, [0, 1], [1.02, 1.07]);

  // --- SHOT 15: PHONE ON DESK & CROSSED ARMS (Frames 1110 - 1158) ---
  // Desk phone, morning sunlight, and Sticky standing tall all in frame
  const s15Local = frame - 1110;
  const s15Tilt = interpolate(s15Local, [10, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const s15CamX = interpolate(s15Tilt, [0, 1], [560, 530]);
  const s15CamY = interpolate(s15Tilt, [0, 1], [980, 930]);
  const s15Zoom = interpolate(s15Tilt, [0, 1], [1.02, 1.06]);

  // --- SHOT 16: BANNER & GREEN 20s SHIELD (Frames 1158 - 1245) ---
  // Heading banner, green stopwatch shield, Sticky, and phone all framed cleanly
  const s16Local = frame - 1158;
  const s16Glide = interpolate(s16Local, [15, 70], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s16CamX = 540;
  const s16CamY = interpolate(s16Glide, [0, 1], [910, 955]);
  const s16Zoom = interpolate(s16Glide, [0, 1], [1.02, 1.07]);

  // --- SHOT 17: DESK PHONE & DOORWAY EXIT (Frames 1245 - 1293) ---
  // Phone on desk and Sticky walking through doorway both clearly visible
  const s17Local = frame - 1245;
  const s17Glide = interpolate(s17Local, [10, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s17CamX = interpolate(s17Glide, [0, 1], [510, 560]);
  const s17CamY = interpolate(s17Glide, [0, 1], [980, 930]);
  const s17Zoom = interpolate(s17Glide, [0, 1], [1.02, 1.06]);

  // --- SHOT 18: OPEN WINDOW & DISSOLVING FLAME (Frames 1293 - 1397) ---
  // Sticky breathing at window and rising white smoke both completely visible
  const s18Local = frame - 1293;
  const s18Ascend = interpolate(s18Local, [20, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const s18CamX = 540;
  const s18CamY = interpolate(s18Ascend, [0, 1], [980, 920]);
  const s18Zoom = interpolate(s18Ascend, [0, 1], [1.02, 1.07]);

  // --- SHOT 19: ZOMBIE CROWD & CALM STICKY (Frames 1397 - 1479) ---
  // Full crowd of phone zombies walking past Sticky in center remains 100% visible
  const s19Local = frame - 1397;
  const s19Push = interpolate(s19Local, [10, 65], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const s19CamX = 540;
  const s19CamY = interpolate(s19Push, [0, 1], [960, 930]);
  const s19Zoom = interpolate(s19Push, [0, 1], [1.00, 1.06]);

  // --- SHOT 20: BENCH MEDITATION WITH HALO (Frames 1479 - 1575) ---
  // Full park bench, Sticky seated with folded hands, and glowing halo all in view
  const s20Prog = interpolate(frame - 1479, [0, 96], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  const s20CamX = 540;
  const s20CamY = interpolate(s20Prog, [0, 1], [960, 930]);
  const s20Zoom = interpolate(s20Prog, [0, 1], [1.00, 1.05]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#FAF9F6",
        overflow: "hidden",
      }}
    >
      {/* Master Voiceover Audio Track */}
      <Audio src={staticFile("audio/ep07_voiceover.wav")} />

      {/* SHOT 01: Bed Hook (Frames 0 - 35) */}
      {frame < 38 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s01CamX, s01CamY, s01Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(0, 35),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_01.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 02: Brain & Flask "FALSE!" (Frames 35 - 125) */}
      {frame >= 32 && frame < 128 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s02CamX, s02CamY, s02Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(35, 125),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_02.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 03: Smiley & Deadpan Eyes (Frames 125 - 189) */}
      {frame >= 122 && frame < 192 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s03CamX, s03CamY, s03Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(125, 189),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_03.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 04: Spinning Clock & Slumped Couch (Frames 189 - 303) */}
      {frame >= 186 && frame < 306 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s04CamX, s04CamY, s04Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(189, 303),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_04.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 05: 1% Battery & Exhausted Sticky (Frames 303 - 417) */}
      {frame >= 300 && frame < 420 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s05CamX, s05CamY, s05Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(303, 417),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_05.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 06: Einstein & Blackboard Brain (Frames 417 - 486) */}
      {frame >= 414 && frame < 489 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s06CamX, s06CamY, s06Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(417, 486),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_06.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 07: Reward Box & Flatline Graph (Frames 486 - 555) */}
      {frame >= 483 && frame < 558 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s07CamX, s07CamY, s07Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(486, 555),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_07.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 08: Hand & Anticipation Spike (Frames 555 - 632) */}
      {frame >= 552 && frame < 635 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s08CamX, s08CamY, s08Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(555, 632),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_08.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 09: "THE ITCH" & Temple Clutch (Frames 632 - 702) */}
      {frame >= 629 && frame < 705 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s09CamX, s09CamY, s09Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(632, 702),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_09.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 10: Sticky & Whispering Demon (Frames 702 - 753) */}
      {frame >= 699 && frame < 756 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s10CamX, s10CamY, s10Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(702, 753),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_10.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 11: Treadmill & Golden Play Button (Frames 753 - 846) */}
      {frame >= 750 && frame < 849 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s11CamX, s11CamY, s11Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(753, 846),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_11.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 12: Dials & Pull-Refresh (Frames 846 - 963) */}
      {frame >= 843 && frame < 966 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s12CamX, s12CamY, s12Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(846, 963),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_12.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 13: Split Screen (Caveman vs Modern) (Frames 963 - 1032) */}
      {frame >= 960 && frame < 1035 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s13CamX, s13CamY, s13Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(963, 1032),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_13.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 14: Hypnotized Sticky & Slot Machine (Frames 1032 - 1110) */}
      {frame >= 1029 && frame < 1113 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s14CamX, s14CamY, s14Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(1032, 1110),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_14.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 15: Phone on Desk & Crossed Arms (Frames 1110 - 1158) */}
      {frame >= 1107 && frame < 1161 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s15CamX, s15CamY, s15Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(1110, 1158),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_15.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 16: Banner & Green 20s Shield (Frames 1158 - 1245) */}
      {frame >= 1155 && frame < 1248 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s16CamX, s16CamY, s16Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(1158, 1245),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_16.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 17: Desk Phone & Doorway Departure (Frames 1245 - 1293) */}
      {frame >= 1242 && frame < 1296 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s17CamX, s17CamY, s17Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(1245, 1293),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_17.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 18: Open Window & Dissolving Flame (Frames 1293 - 1397) */}
      {frame >= 1290 && frame < 1400 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s18CamX, s18CamY, s18Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(1293, 1397),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_18.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 19: Zombie Crowd & Calm Sticky (Frames 1397 - 1479) */}
      {frame >= 1394 && frame < 1482 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s19CamX, s19CamY, s19Zoom),
            transformOrigin: "0px 0px",
            opacity: getCrossfade(1397, 1479),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_19.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* SHOT 20: Bench Meditation with Halo (Frames 1479 - 1575) */}
      {frame >= 1476 && (
        <AbsoluteFill
          style={{
            transform: getCameraMatrix(s20CamX, s20CamY, s20Zoom),
            transformOrigin: "0px 0px",
            opacity: interpolate(frame, [1476, 1480], [0, 1], { extrapolateRight: "clamp" }),
          }}
        >
          <Img
            src={staticFile("slides/ep07/slide_20.jpg")}
            style={{ width: 1080, height: 1920, objectFit: "cover" }}
          />
        </AbsoluteFill>
      )}

      {/* Subtle Studio Paper Vignette */}
      <AbsoluteFill
        style={{
          boxShadow: "inset 0 0 80px rgba(0, 0, 0, 0.05)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
