import { ShotCameraConfig } from "../../../three/ThreeStage";

/**
 * 25-Shot Cinematic Camera Configurations
 * Synchronized with the 4765 frames (158.84s) master deep motivational voiceover.
 * Strict pause of 0.25s between shots.
 */
export const SHOT_CAMERA_PATHS: ShotCameraConfig[] = [
  // Shot 1: 5 AM Promise in Bedroom (Angular Top View)
  {
    shotId: 1,
    startFrame: 0,
    endFrame: 164,
    startPos: [2.7, 2.3, 2.3],
    endPos: [2.3, 2.0, 1.9],
    target: [-0.1, 0.95, -1.15],
    fov: 42,
  },
  // Shot 2: Dawn 5-Mile Run
  {
    shotId: 2,
    startFrame: 164,
    endFrame: 318,
    startPos: [-3.0, 1.6, 3.8],
    endPos: [1.8, 1.6, 3.8],
    target: [0, 1.2, 0],
    fov: 40,
  },
  // Shot 3: 8 Unbroken Hours in Office
  {
    shotId: 3,
    startFrame: 318,
    endFrame: 500,
    startPos: [2.8, 2.2, 2.5],
    endPos: [-1.8, 2.2, 2.5],
    target: [0, 1.1, -0.8],
    fov: 38,
  },
  // Shot 4: Two Days of Perfect Execution
  {
    shotId: 4,
    startFrame: 500,
    endFrame: 610,
    startPos: [0, 1.4, 2.2],
    endPos: [0, 1.3, 1.6],
    target: [0, 1.1, -0.6],
    fov: 35,
  },
  // Shot 5: Feeling Invincible on the Peak
  {
    shotId: 5,
    startFrame: 610,
    endFrame: 818,
    startPos: [0, 1.2, 4.5],
    endPos: [0, 2.2, 3.5],
    target: [0, 2.0, 0],
    fov: 42,
  },
  // Shot 6: THEN DAY FOUR ARRIVES
  {
    shotId: 6,
    startFrame: 818,
    endFrame: 904,
    startPos: [2.30, 2.05, 2.00],
    endPos: [2.00, 1.85, 1.65],
    target: [0.20, 1.10, -0.85],
    fov: 42,
  },
  // Shot 7: Cold Room, Warm Bed
  {
    shotId: 7,
    startFrame: 904,
    endFrame: 1103,
    startPos: [0, 4.8, 2.5],
    endPos: [0, 3.2, 1.8],
    target: [0.2, 0.4, -0.9],
    fov: 42,
  },
  // Shot 8: Vanished Tuesday Fire
  {
    shotId: 8,
    startFrame: 1103,
    endFrame: 1279,
    startPos: [0, 1.3, 2.4],
    endPos: [0, 1.3, 1.5],
    target: [0, 1.2, 0],
    fov: 32,
  },
  // Shot 9: 30-Second Negotiation
  {
    shotId: 9,
    startFrame: 1279,
    endFrame: 1473,
    startPos: [2.5, 1.3, 0.8],
    endPos: [1.8, 1.1, 0.2],
    target: [0.6, 0.85, -0.2],
    fov: 36,
  },
  // Shot 10: The Weight of Guilt
  {
    shotId: 10,
    startFrame: 1473,
    endFrame: 1766,
    startPos: [1.90, 1.50, 2.00],
    endPos: [1.70, 1.40, 1.70],
    target: [0.20, 1.05, -0.60],
    fov: 42,
  },
  // Shot 11: Senior Mentor Wisdom
  {
    shotId: 11,
    startFrame: 1766,
    endFrame: 1886,
    startPos: [0.0, 1.70, 5.00],
    endPos: [0.0, 1.65, 4.60],
    target: [0.0, 1.15, 0.10],
    fov: 42,
  },
  // Shot 12: The Wrong Job for Willpower
  {
    shotId: 12,
    startFrame: 1886,
    endFrame: 2143,
    startPos: [-2.2, 1.8, 3.2],
    endPos: [1.8, 1.6, 2.8],
    target: [-0.3, 1.0, 0],
    fov: 38,
  },
  // Shot 13: Survival Organ Not Inspiration Machine
  {
    shotId: 13,
    startFrame: 2143,
    endFrame: 2379,
    startPos: [-2.80, 2.00, 4.80],
    endPos: [-2.40, 1.80, 4.20],
    target: [0.15, 1.20, 0.0],
    fov: 42,
  },
  // Shot 14: Biology Sounds the Alarm
  {
    shotId: 14,
    startFrame: 2379,
    endFrame: 2688,
    startPos: [2.0, 1.6, 3.8],
    endPos: [-1.5, 1.2, 3.0],
    target: [0, 1.1, 0],
    fov: 40,
  },
  // Shot 15: IronForge Gym vs Tea Routine
  {
    shotId: 15,
    startFrame: 2688,
    endFrame: 2899,
    startPos: [0, 1.6, 5.8],
    endPos: [0, 1.5, 5.2],
    target: [0, 1.1, -0.6],
    fov: 46,
  },
  // Shot 16: Elimination of Choice
  // Shot 16: The Elimination Gateway
  {
    shotId: 16,
    startFrame: 2899,
    endFrame: 3069,
    startPos: [0.0, 1.85, 7.20],
    endPos: [0.0, 1.65, 3.60],
    target: [0.0, 1.25, -2.00],
    fov: 44,
  },
  // Shot 17: No Negotiation at 7 AM
  {
    shotId: 17,
    startFrame: 3069,
    endFrame: 3203,
    startPos: [-2.60, 1.65, 1.80],
    endPos: [-2.10, 1.50, 1.20],
    target: [0.10, 0.95, -0.60],
    fov: 44,
  },
  // Shot 18: Opening Laptop Without Mood
  {
    shotId: 18,
    startFrame: 3203,
    endFrame: 3346,
    startPos: [1.35, 1.35, 0.6],
    endPos: [1.15, 1.25, 0.4],
    target: [-0.15, 1.05, -0.5],
    fov: 42,
  },
  // Shot 19: Engineer the Environment
  {
    shotId: 19,
    startFrame: 3346,
    endFrame: 3539,
    startPos: [-0.3, 2.2, 4.2],
    endPos: [0.1, 2.0, 3.6],
    target: [0.1, 1.05, 0.0],
    fov: 40,
  },
  // Shot 20: Phone Away, Shoes Ready, Blank Doc
  {
    shotId: 20,
    startFrame: 3539,
    endFrame: 3781,
    startPos: [-2.7, 1.40, 1.1],
    endPos: [0.0, 2.4, 4.8],
    target: [-2.7, 1.05, 0.0],
    endTarget: [0.0, 1.1, 0.0],
    fov: 40,
  },
  // Shot 21: Carve Riverbed Not Push Boulder
  {
    shotId: 21,
    startFrame: 3781,
    endFrame: 4007,
    startPos: [2.6, 1.8, 3.8],
    endPos: [0.0, 2.5, 6.0],
    target: [3.0, 0.8, 0.0],
    endTarget: [0.0, 1.2, 0.0],
    fov: 44,
  },
  // Shot 22: Stop Aiming for Exhausting Days
  {
    shotId: 22,
    startFrame: 4007,
    endFrame: 4177,
    startPos: [0.3, 1.45, 3.2],
    endPos: [0.15, 1.25, 2.6],
    target: [0.15, 0.65, 0.1],
    fov: 42,
  },
  // Shot 23: Make Resistance Ridiculous
  {
    shotId: 23,
    startFrame: 4177,
    endFrame: 4310,
    startPos: [0.1, 1.65, 3.8],
    endPos: [0.25, 1.55, 3.2],
    target: [0.1, 1.25, 0.0],
    fov: 42,
  },
  // Shot 24: Two Minutes in Chair, One Paragraph
  {
    shotId: 24,
    startFrame: 4310,
    endFrame: 4580,
    startPos: [-3.0, 1.45, 2.6],
    endPos: [3.0, 1.45, 2.2],
    target: [-3.0, 0.95, 0.0],
    endTarget: [3.0, 1.15, 0.0],
    fov: 40,
  },
  // Shot 25: Cast Small Vote & Let Momentum Lift
  {
    shotId: 25,
    startFrame: 4580,
    endFrame: 4764,
    startPos: [0.6, 1.85, 2.6],
    endPos: [0.0, 2.6, 5.4],
    target: [0.6, 1.5, 0.0],
    endTarget: [0.0, 1.35, 0.0],
    fov: 44,
  },
];
