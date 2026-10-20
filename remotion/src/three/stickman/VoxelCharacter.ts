import * as THREE from "three";
import {
  createVoxelArmTexture,
  createVoxelFaceTexture,
  createVoxelHairTexture,
  createVoxelLegTexture,
  createVoxelTorsoTexture,
} from "../textures/VoxelTextures";

/**
 * Authentic Minecraft Voxel Character (Alex / Marcus / Elena)
 * Features 3D layered micro-voxel geometry:
 * - 3D Hair layer with volumetric fringe bangs and sideburns
 * - Detailed 8x8 pixel face with expressive eyes & mouth
 * - 3D Shirt / Tunic with collar overlay and hem
 * - Articulated arms with distinct 3D sleeve cuffs, bare skin hands, and thumbs
 * - Denim jeans legs with 3D boot cuffs and micro-pixel soles
 */
export class VoxelCharacter {
  public name: string;
  public root: THREE.Group;
  public headGroup: THREE.Group;
  public head: THREE.Mesh;
  public hairGroup: THREE.Group;
  public torsoGroup: THREE.Group;
  public torso: THREE.Mesh;
  public armLeft: THREE.Group;
  public armRight: THREE.Group;
  public legLeft: THREE.Group;
  public legRight: THREE.Group;

  constructor(name: string = "Alex") {
    this.name = name;
    this.root = new THREE.Group();
    this.root.name = `Character_${name}`;

    // Common skin & hair materials
    const skinColor = name === "Marcus" ? 0x8d5524 : 0xf6d7b0;
    const skinMat = new THREE.MeshToonMaterial({ color: skinColor });
    const hairTex = createVoxelHairTexture();
    const hairMat = new THREE.MeshToonMaterial({ map: hairTex });

    // =========================================================================
    // 1. HEAD & 3D HAIR LAYER
    // =========================================================================
    this.headGroup = new THREE.Group();
    this.headGroup.position.set(0, 1.4, 0);

    // Inner Head with 8x8 Face Texture
    const faceTex = createVoxelFaceTexture(false);
    const faceMat = new THREE.MeshToonMaterial({ map: faceTex });
    const headMaterials = [
      hairMat, // right
      hairMat, // left
      hairMat, // top
      skinMat, // neck bottom
      faceMat, // front face
      hairMat, // back
    ];
    const headGeo = new THREE.BoxGeometry(0.48, 0.48, 0.48);
    this.head = new THREE.Mesh(headGeo, headMaterials);
    this.headGroup.add(this.head);

    // 3D Outer Hair Helmet (Micro-voxel 3D layers)
    this.hairGroup = new THREE.Group();
    
    // Top & sides hair cap
    const hairCapGeo = new THREE.BoxGeometry(0.52, 0.28, 0.52);
    const hairCap = new THREE.Mesh(hairCapGeo, hairMat);
    hairCap.position.set(0, 0.12, -0.01);
    this.hairGroup.add(hairCap);

    // 3D Front Bangs (Micro-voxels over forehead)
    const bangLeft = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.12, 0.05), hairMat);
    bangLeft.position.set(-0.14, 0.14, 0.245);
    this.hairGroup.add(bangLeft);

    const bangMid = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.08, 0.05), hairMat);
    bangMid.position.set(0.01, 0.16, 0.245);
    this.hairGroup.add(bangMid);

    const bangRight = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.14, 0.05), hairMat);
    bangRight.position.set(0.16, 0.13, 0.245);
    this.hairGroup.add(bangRight);

    // 3D Sideburns
    const sideburnL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.18, 0.14), hairMat);
    sideburnL.position.set(-0.245, 0.05, 0.06);
    this.hairGroup.add(sideburnL);

    const sideburnR = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.18, 0.14), hairMat);
    sideburnR.position.set(0.245, 0.05, 0.06);
    this.hairGroup.add(sideburnR);

    this.headGroup.add(this.hairGroup);
    this.root.add(this.headGroup);

    // =========================================================================
    // 2. TORSO & 3D SHIRT OVERLAY
    // =========================================================================
    this.torsoGroup = new THREE.Group();
    this.torsoGroup.position.set(0, 0.85, 0);

    const charType = this.name === "Marcus" ? "Marcus" : "Alex";
    const torsoTex = createVoxelTorsoTexture(charType);
    const torsoMat = new THREE.MeshToonMaterial({ map: torsoTex });
    const torsoGeo = new THREE.BoxGeometry(0.5, 0.72, 0.28);
    this.torso = new THREE.Mesh(torsoGeo, torsoMat);
    this.torsoGroup.add(this.torso);

    // 3D Shirt Collar Rim
    const collar = new THREE.Mesh(
      new THREE.BoxGeometry(0.44, 0.06, 0.22),
      new THREE.MeshToonMaterial({ color: this.name === "Marcus" ? 0xd4af37 : 0x008a94 })
    );
    collar.position.set(0, 0.34, 0);
    this.torsoGroup.add(collar);

    this.root.add(this.torsoGroup);

    // =========================================================================
    // 3. ARMS WITH 3D SLEEVE CUFFS & BARE SKIN HANDS
    // =========================================================================
    this.armLeft = this.createArm(0.2, 0.72, 0.22, skinMat, true, this.name);
    this.armLeft.position.set(0.36, 1.15, 0);
    this.root.add(this.armLeft);

    this.armRight = this.createArm(0.2, 0.72, 0.22, skinMat, false, this.name);
    this.armRight.position.set(-0.36, 1.15, 0);
    this.root.add(this.armRight);

    // =========================================================================
    // 4. LEGS (Adjacent Seamless Blocks - Zero Gap, Zero Overlap, Zero Z-Fighting)
    // =========================================================================
    // Torso width is 0.50. Each leg is width 0.248, depth 0.28.
    // They meet right in the center at x = 0 with zero gap and no clipping!
    this.legLeft = this.createLeg(0.248, 0.75, 0.28, true);
    this.legLeft.position.set(0.125, 0.49, 0);
    this.root.add(this.legLeft);

    this.legRight = this.createLeg(0.248, 0.75, 0.28, false);
    this.legRight.position.set(-0.125, 0.49, 0);
    this.root.add(this.legRight);
  }

  /**
   * Builds an articulated arm with:
   * - Upper sleeve block (with textured fabric)
   * - 3D sleeve cuff overhang
   * - Lower bare skin hand block
   * - 3D micro-voxel thumb
   */
  private createArm(
    w: number,
    h: number,
    d: number,
    skinMat: THREE.Material,
    isLeft: boolean,
    charName: string = "Alex"
  ): THREE.Group {
    const pivot = new THREE.Group();

    const sleeveH = h * 0.65;
    const handH = h * 0.35;

    // 1. Sleeve
    const armTex = createVoxelArmTexture(charName === "Marcus" ? "Marcus" : "Alex");
    const sleeveMat = new THREE.MeshToonMaterial({ map: armTex });
    const sleeve = new THREE.Mesh(new THREE.BoxGeometry(w, sleeveH, d), sleeveMat);
    sleeve.position.y = -sleeveH / 2;
    pivot.add(sleeve);

    // 3D Sleeve Cuff Overhang
    const cuffGeo = new THREE.BoxGeometry(w + 0.025, 0.05, d + 0.025);
    const cuffColor = charName === "Marcus" ? 0xd4af37 : 0x007882;
    const cuffMat = new THREE.MeshToonMaterial({ color: cuffColor });
    const cuff = new THREE.Mesh(cuffGeo, cuffMat);
    cuff.position.y = -sleeveH + 0.025;
    pivot.add(cuff);

    // 2. Hand (Bare Skin)
    const hand = new THREE.Mesh(new THREE.BoxGeometry(w - 0.015, handH, d - 0.015), skinMat);
    hand.position.y = -sleeveH - handH / 2;
    pivot.add(hand);

    // 3. Thumb Micro-voxel
    const thumb = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.09, 0.06), skinMat);
    const thumbX = isLeft ? -(w / 2 - 0.01) : (w / 2 - 0.01);
    thumb.position.set(thumbX, -sleeveH - handH / 2 + 0.02, 0.02);
    pivot.add(thumb);

    return pivot;
  }

  /**
   * Builds an articulated leg with denim pants and 3D boot cuffs
   */
  private createLeg(w: number, h: number, d: number, isLeft: boolean): THREE.Group {
    const pivot = new THREE.Group();

    const pantsH = h * 0.72;
    const bootH = h * 0.28;

    // 1. Denim Pants (Upper leg)
    const legTex = createVoxelLegTexture();
    const legMat = new THREE.MeshToonMaterial({ map: legTex });
    const pants = new THREE.Mesh(new THREE.BoxGeometry(w, pantsH, d), legMat);
    pants.position.y = -pantsH / 2;
    pivot.add(pants);

    // 2. 3D Boot Cuff (Dark sturdy shoe)
    const bootGeo = new THREE.BoxGeometry(w + 0.02, bootH, d + 0.03);
    const bootMat = new THREE.MeshToonMaterial({ color: 0x222222 });
    const boot = new THREE.Mesh(bootGeo, bootMat);
    boot.position.set(0, -pantsH - bootH / 2, 0.01);
    pivot.add(boot);

    // 3. Boot Sole Micro-voxel
    const soleGeo = new THREE.BoxGeometry(w + 0.025, 0.04, d + 0.035);
    const soleMat = new THREE.MeshToonMaterial({ color: 0x111111 });
    const sole = new THREE.Mesh(soleGeo, soleMat);
    sole.position.set(0, -pantsH - bootH + 0.02, 0.01);
    pivot.add(sole);

    return pivot;
  }

  public resetJoints(): void {
    // Retain root position and root rotation so scene placement & orientation are preserved
    this.headGroup.rotation.set(0, 0, 0);
    this.torsoGroup.rotation.set(0, 0, 0);
    this.armLeft.rotation.set(0, 0, 0);
    this.armRight.rotation.set(0, 0, 0);
    this.legLeft.rotation.set(0, 0, 0);
    this.legRight.rotation.set(0, 0, 0);
  }

  public setLyingInBed(time: number): void {
    this.resetJoints();
    const breath = Math.sin(time * 2.2) * 0.012;
    this.root.position.y = 0.62 + breath;
    this.root.rotation.set(-Math.PI / 2, 0, 0);
    this.headGroup.rotation.set(0.08, Math.sin(time * 0.6) * 0.04, 0);
    this.armLeft.rotation.set(0, 0, -0.12);
    this.armRight.rotation.set(0, 0, 0.12);
  }

  /**
   * Natural cinematic wakeup sequence:
   * Smoothly transitions from lying down into sitting upright in bed,
   * turning head towards the morning window light.
   */
  public setWakingUp(time: number, progress: number = 0): void {
    this.resetJoints();
    const clamped = Math.max(0, Math.min(1, progress));
    // Smooth cubic ease-in-out for natural human awakening
    const ease = clamped * clamped * (3 - 2 * clamped);
    const breath = Math.sin(time * 2.5) * (0.012 * (1 - ease * 0.7));

    // Base lying down to seated transition:
    // Natural human seated posture has a gentle forward lean (+0.20 rad) over lap
    const angleX = (-Math.PI / 2) * (1 - ease) + 0.20 * ease;
    this.root.rotation.set(angleX, 0, 0);

    // Root height smoothly moves from lying height (0.62) to seated hip height (0.19)
    this.root.position.y = 0.62 * (1 - ease) + 0.19 * ease + breath;

    // Torso has subtle organic spine curvature forward
    this.torsoGroup.rotation.x = 0.08 * ease;

    // Legs rest relaxed on mattress with soft, natural knee bend
    this.legLeft.rotation.x = (-Math.PI / 2 + 0.24) * ease;
    this.legRight.rotation.x = (-Math.PI / 2 + 0.14) * ease;

    // Head turns towards the morning window light and camera (negative Y) with sleepy morning eyes
    this.headGroup.rotation.set(
      0.16 * ease,
      -0.55 * ease + Math.sin(time * 1.5) * 0.02,
      -0.08 * ease
    );

    // Left arm rests casually on left thigh towards the camera
    this.armLeft.position.set(-0.36, 1.15, 0.04 * ease);
    this.armLeft.rotation.set(0.32 * ease, 0.12 * ease, -0.22 * ease);

    // Right arm braces back on mattress to support rising torso
    this.armRight.position.set(0.38, 1.15, -0.04 * ease);
    this.armRight.rotation.set(0.24 * ease, -0.08 * ease, 0.22 * ease);
  }

  public setRunning(time: number): void {
    this.resetJoints();
    const cycle = time * 9.0;
    this.root.position.y = 0.5 + Math.abs(Math.sin(cycle)) * 0.15;
    this.root.rotation.x = 0.22; // Forward lean
    this.headGroup.rotation.x = -0.1;
    this.armLeft.rotation.x = Math.sin(cycle) * 0.95;
    this.armRight.rotation.x = -Math.sin(cycle) * 0.95;
    this.legLeft.rotation.x = -Math.sin(cycle) * 0.9;
    this.legRight.rotation.x = Math.sin(cycle) * 0.9;
  }


  public setSittingFoldedArms(time: number): void {
    this.resetJoints();
    const nod = Math.sin(time * 2.0) * 0.05;
    this.root.position.y = 0.22;
    this.headGroup.rotation.set(-0.1 + nod, 0, 0);
    this.armLeft.rotation.set(-0.55, 0.55, -0.18); // Arms folded across chest
    this.armRight.rotation.set(-0.55, -0.55, 0.18);
    this.legLeft.rotation.x = -Math.PI / 2 + 0.12;
    this.legRight.rotation.x = -Math.PI / 2 + 0.12;
  }

  public setSlumpHeadInHands(time: number, yaw: number = 0): void {
    this.resetJoints();
    const breath = Math.sin(time * 1.6) * 0.015;
    this.root.position.y = 0.10;
    this.root.rotation.set(0, yaw, 0);

    // Torso curled forward in deep shame & guilt
    this.torsoGroup.rotation.set(0.44 + breath, 0, 0);

    // Head bowed forward, looking down at lap in heavy remorse
    this.headGroup.rotation.set(0.56 + breath * 0.6, 0, 0);

    // Arms resting forward along the thighs, hands resting on knees in dejection
    this.armLeft.rotation.set(-0.75, 0.08, 0.16);
    this.armRight.rotation.set(-0.75, -0.08, -0.16);

    // Legs angled forward and down, feet resting firmly on the floor
    this.legLeft.rotation.set(-0.68, 0.06, 0);
    this.legRight.rotation.set(-0.68, -0.06, 0);
  }

  public setAlarmSlap(time: number): void {
    this.resetJoints();
    this.root.position.y = 0.58;
    this.root.rotation.set(-Math.PI / 2, 0, 0);
    const slapPhase = Math.sin(time * 5.0);
    this.armRight.rotation.set(slapPhase > 0 ? 0.8 : 0.1, 0, 0.6);
  }

  public setStandingHero(time: number): void {
    this.resetJoints();
    const sway = Math.sin(time * 1.5) * 0.02;
    this.root.position.y = 0.75;
    this.headGroup.rotation.set(-0.15, sway, 0);
    this.armLeft.rotation.set(0, 0, -0.15);
    this.armRight.rotation.set(0, 0, 0.15);
  }

  public setMentorSpeak(time: number): void {
    this.resetJoints();
    const handGesture = Math.sin(time * 3.0) * 0.25;
    this.root.position.y = 0.75;
    this.headGroup.rotation.set(0.05, Math.sin(time * 1.2) * 0.08, 0);
    this.armRight.rotation.set(0.6 + handGesture, -0.2, 0.2);
    this.armLeft.rotation.set(0.1, 0, -0.1);
  }

  public setHeavySquatStruggle(time: number): void {
    this.resetJoints();
    const shake = (Math.random() - 0.5) * 0.03;
    // Grounded heavy squat stance
    this.root.position.y = 0.38 + shake;
    this.torsoGroup.rotation.x = 0.24; // Torso angled forward under heavy load
    this.headGroup.rotation.set(-0.16, shake * 2, 0); // Straining upward
    // Hands reaching up and gripping the barbell on shoulders
    this.armLeft.rotation.set(-0.25, 0.3, -2.35);
    this.armRight.rotation.set(-0.25, -0.3, 2.35);
    // Squatting knees bent outward, feet flat
    this.legLeft.rotation.set(-0.45, 0.15, -0.22);
    this.legRight.rotation.set(-0.45, -0.15, 0.22);
  }

  public setBracingWind(time: number): void {
    this.resetJoints();
    const gust = Math.sin(time * 8.0) * 0.04;
    // Grounded athletic staggered brace stance
    this.root.position.y = 0.48;
    this.root.rotation.x = -0.22 + gust; // Leaning forward into the wind
    this.headGroup.rotation.set(0.28, Math.sin(time * 4.0) * 0.05, 0); // Head lowered against blast
    // Arms raised in front of face to shield
    this.armLeft.rotation.set(1.2, 0.5, -0.3);
    this.armRight.rotation.set(1.4, -0.4, 0.2);
    // Staggered brace legs
    this.legLeft.rotation.set(-0.35, 0.1, 0);
    this.legRight.rotation.set(0.40, -0.1, 0);
  }

  public setWalkForward(time: number): void {
    this.resetJoints();
    const cycle = time * 5.0;
    this.root.position.y = 0.75 + Math.abs(Math.sin(cycle)) * 0.04;
    this.armLeft.rotation.x = Math.sin(cycle) * 0.5;
    this.armRight.rotation.x = -Math.sin(cycle) * 0.5;
    this.legLeft.rotation.x = -Math.sin(cycle) * 0.45;
    this.legRight.rotation.x = Math.sin(cycle) * 0.45;
  }

  public setStandUpSmooth(time: number): void {
    this.resetJoints();
    const rise = Math.min(1.0, time * 0.6);
    this.root.position.y = 0.35 + rise * 0.4;
    this.headGroup.rotation.set(0.2 - rise * 0.3, 0, 0);
  }

  public setDecisiveRise(time: number): void {
    this.resetJoints();
    if (time < 0.6) {
      // Seated on bed edge, poised and awake
      this.root.position.set(0, 0.58, 0);
      this.torsoGroup.rotation.set(0.05, 0, 0);
      this.headGroup.rotation.set(-0.04, 0, 0);
      this.armLeft.rotation.set(0.5, 0.1, 0);
      this.armRight.rotation.set(0.5, -0.1, 0);
      this.legLeft.rotation.set(-0.4, 0.05, 0);
      this.legRight.rotation.set(-0.4, -0.05, 0);
    } else if (time < 1.6) {
      // Decisive smooth standing motion onto feet
      const p = (time - 0.6) / 1.0;
      const ease = p * p * (3 - 2 * p);
      this.root.position.set(0, 0.58 + 0.17 * ease, 0.2 * ease);
      this.torsoGroup.rotation.set(0.05 * (1 - ease), 0, 0);
      this.headGroup.rotation.set(-0.04, 0, 0);
      this.armLeft.rotation.set(0.5 * (1 - ease), 0, 0);
      this.armRight.rotation.set(0.5 * (1 - ease), 0, 0);
      this.legLeft.rotation.set(-0.4 * (1 - ease), 0, 0);
      this.legRight.rotation.set(-0.4 * (1 - ease), 0, 0);
    } else {
      // Standing confident, taking first purposeful step into the morning
      const stepPhase = (time - 1.6) * 3.5;
      this.root.position.set(0, 0.75 + Math.abs(Math.sin(stepPhase)) * 0.03, 0.2 + (time - 1.6) * 0.2);
      this.headGroup.rotation.set(-0.02, 0, 0);
      this.armLeft.rotation.x = Math.sin(stepPhase) * 0.4;
      this.armRight.rotation.x = -Math.sin(stepPhase) * 0.4;
      this.legLeft.rotation.x = -Math.sin(stepPhase) * 0.35;
      this.legRight.rotation.x = Math.sin(stepPhase) * 0.35;
    }
  }

  public setTyping(time: number): void {
    this.resetJoints();
    // Pelvis seated at desk height
    this.root.position.y = 0.58;
    this.torsoGroup.rotation.x = 0.10; // Slightly angled forward toward screen
    this.headGroup.rotation.x = 0.20; // Focused down on keys / screen

    // Alternate rapid keystroke micro-jitter
    const keystrokeL = Math.sin(time * 18.0) * 0.05;
    const keystrokeR = Math.cos(time * 20.0) * 0.05;

    // Arms extended forward over desk resting on keys
    this.armLeft.rotation.set(0.85 + keystrokeL, 0.22, -0.15);
    this.armRight.rotation.set(0.85 + keystrokeR, -0.22, 0.15);

    // Legs hanging comfortably beneath desk
    this.legLeft.rotation.set(-0.15, 0.05, 0);
    this.legRight.rotation.set(-0.15, -0.05, 0);
  }

  public setMarchForward(time: number): void {
    this.resetJoints();
    const cycle = time * 4.6;
    this.root.position.y = 0.75 + Math.abs(Math.sin(cycle)) * 0.04;
    this.headGroup.rotation.set(-0.02, 0, 0); // Steady head looking straight forward
    this.torsoGroup.rotation.y = Math.sin(cycle) * 0.06;
    this.armLeft.rotation.x = Math.sin(cycle) * 0.55;
    this.armRight.rotation.x = -Math.sin(cycle) * 0.55;
    this.legLeft.rotation.x = -Math.sin(cycle) * 0.5;
    this.legRight.rotation.x = Math.sin(cycle) * 0.5;
  }

  public setPresentingMaster(time: number): void {
    this.resetJoints();
    const gesture = Math.sin(time * 2.2) * 0.18;
    this.root.position.y = 0.75;
    this.headGroup.rotation.set(0.04, Math.sin(time * 1.0) * 0.06, 0);
    // Right arm broad orator gesture sweeping across the exhibit
    this.armRight.rotation.set(0.75 + gesture, -0.35, 0.35);
    // Left arm resting casually at side/hip
    this.armLeft.rotation.set(0.12, 0.08, -0.12);
  }

  public setBoulderPush(time: number): void {
    this.resetJoints();
    const strain = Math.sin(time * 6.0) * 0.03;
    this.root.position.y = 0.65;
    this.root.rotation.x = 0.45 + strain; // Hard forward lean
    this.armLeft.rotation.set(1.3, 0.2, 0);
    this.armRight.rotation.set(1.3, -0.2, 0);
    this.legLeft.rotation.x = 0.6;
    this.legRight.rotation.x = -0.4;
  }

  public setStepOverHurdle(time: number): void {
    this.resetJoints();
    const step = Math.sin(time * 3.5);
    this.root.position.y = 0.75 + Math.max(0, step) * 0.12;
    this.legRight.rotation.x = step * 0.8;
    this.armLeft.rotation.x = -step * 0.5;
  }

  // Convenient aliases for storyboard animations
  public setStandingMentor(time: number): void {
    this.setMentorSpeak(time);

  }

  public setPushingBoulder(time: number): void {
    this.setBoulderPush(time);
  }

  public setSteppingHurdle(time: number): void {
    this.setStepOverHurdle(time);
  }

  public setLookingAtHands(time: number): void {
    this.resetJoints();
    this.root.position.y = 0.75;
    this.headGroup.rotation.set(0.35, 0, 0); // Head tilted down looking at hands
    this.armLeft.rotation.set(1.1, 0.35, -0.2); // Open hands in front of chest
    this.armRight.rotation.set(1.1, -0.35, 0.2);
  }

  public setSittingProud(time: number): void {
    this.resetJoints();
    const breath = Math.sin(time * 1.5) * 0.01;
    // Seated proudly on chair: pelvis at 0.58m
    this.root.position.y = 0.58;
    this.torsoGroup.rotation.x = -0.04 + breath; // Upright confident posture
    this.headGroup.rotation.set(-0.05, Math.sin(time * 0.8) * 0.04, 0); // Dignified, calm gaze
    // Arms bent forward resting hands naturally on desk
    this.armLeft.rotation.set(0.65, 0.25, -0.2);
    this.armRight.rotation.set(0.65, -0.25, 0.2);
    // Legs tucked naturally down under the desk to floor
    this.legLeft.rotation.set(-0.15, 0.05, 0);
    this.legRight.rotation.set(-0.15, -0.05, 0);
  }

  /**
   * Scene 9 Choreography:
   * Alex wakes up in bed, reaches right arm across towards the nightstand,
   * presses/slaps the clock button to snooze, then goes limp and falls back
   * onto the pillow into deep sleep.
   */
  public setNegotiateAlarmAndSleep(time: number): void {
    this.resetJoints();
    this.root.rotation.set(-Math.PI / 2, 0, 0);
    this.root.position.y = 0.62;

    if (time < 1.5) {
      // Phase 1: Groggily stirring in bed
      const breath = Math.sin(time * 2.2) * 0.01;
      this.root.position.y = 0.62 + breath;
      this.headGroup.rotation.set(0.08, Math.sin(time * 1.8) * 0.06, 0);
      this.armLeft.rotation.set(0, 0, -0.12);
      this.armRight.rotation.set(0, 0, 0.12);
    } else if (time < 3.2) {
      // Phase 2: Natural human body roll towards nightstand & reaching arm out to clock
      const p = (time - 1.5) / 1.7;
      const ease = p * p * (3 - 2 * p);
      this.root.rotation.set(-Math.PI / 2 + 0.12 * ease, 0, -0.16 * ease);
      this.torsoGroup.rotation.set(0.08 * ease, 0.16 * ease, 0);
      this.headGroup.rotation.set(0.12 * ease, 0.35 * ease, -0.05 * ease);

      // Left arm lifts up off bed and reaches directly toward the clock button
      this.armLeft.position.set(0.36, 1.15, -0.04);
      this.armLeft.rotation.set(-1.05 * ease, 0, 0.65 * ease);
      this.armRight.rotation.set(0, 0, 0.12);
    } else if (time < 4.0) {
      // Phase 3: Pressing / slapping down firmly on the clock snooze button
      const pressPhase = (time - 3.2) / 0.8;
      const press = Math.sin(pressPhase * Math.PI);
      this.root.rotation.set(-Math.PI / 2 + 0.12, 0, -0.16);
      this.torsoGroup.rotation.set(0.08, 0.16, 0);
      this.headGroup.rotation.set(0.12 + press * 0.05, 0.35, -0.05);

      // Hand strikes down on snooze button (downward deflection along world Y)
      this.armLeft.position.set(0.36, 1.15, -0.04);
      this.armLeft.rotation.set(-1.05 + press * 0.15, 0, 0.65);
      this.armRight.rotation.set(0, 0, 0.12);
    } else {
      // Phase 4: Collapsing and falling back asleep onto pillow
      const fallP = Math.min(1.0, (time - 4.0) / 1.6);
      const fallEase = fallP * fallP * (3 - 2 * fallP);
      // Body rolls back flat onto back
      this.root.rotation.set(
        (-Math.PI / 2 + 0.12) * (1 - fallEase) - (Math.PI / 2) * fallEase,
        0,
        -0.16 * (1 - fallEase)
      );
      this.torsoGroup.rotation.set(0.08 * (1 - fallEase), 0.16 * (1 - fallEase), 0);
      // Left arm goes limp, falls off the clock, and drops back to the mattress
      this.armLeft.position.set(0.36, 1.15, -0.04 * (1 - fallEase));
      this.armLeft.rotation.set(
        -1.05 * (1 - fallEase),
        0,
        0.65 * (1 - fallEase) - 0.12 * fallEase
      );
      this.armRight.rotation.set(0, 0, 0.12);
      // Head drops sideways into the soft pillow
      this.headGroup.rotation.set(
        0.08 * fallEase,
        -0.45 * fallEase,
        -0.18 * fallEase
      );
      const deepBreath = Math.sin((time - 4.0) * 1.5) * 0.009;
      this.root.position.y = 0.62 + deepBreath;
    }
  }

  public setSlapAlarm(time: number): void {
    this.setNegotiateAlarmAndSleep(time);
  }


  // --- MOUNTAIN SUMMIT & CLIMBER POSES (SCENE 5) ---
  public setTriumphantSummit(time: number): void {
    this.resetJoints();
    // Torso perfectly upright, proud posture
    this.torsoGroup.rotation.set(0, 0, 0);
    // Head looking straight forward over the horizon with quiet confidence
    this.headGroup.rotation.set(-0.02, 0, 0);
    // Arms straight downward alongside torso (authentic Minecraft standing pose)
    this.armLeft.rotation.set(0, 0, 0);
    this.armRight.rotation.set(0, 0, 0);
    // Legs straight downward firmly planted
    this.legLeft.rotation.set(0, 0, 0);
    this.legRight.rotation.set(0, 0, 0);
  }

  public setClimbingStairs(time: number, speed: number = 3.2): void {
    const cycle = time * speed;
    const legPhase = Math.sin(cycle);
    this.torsoGroup.rotation.set(0.24, 0, 0); // Leaning into the steep mountain slope
    this.headGroup.rotation.set(-0.25, 0, 0); // Looking up at the steps ahead
    this.legLeft.rotation.x = -legPhase * 0.75;
    this.legRight.rotation.x = legPhase * 0.75;
    this.armLeft.rotation.x = legPhase * 0.65;
    this.armRight.rotation.x = -legPhase * 0.65;
  }

  public setFatiguedOnKnees(time: number): void {
    const pant = Math.sin(time * 3.2) * 0.025;
    this.torsoGroup.rotation.set(0.48 + pant, 0, 0); // Heavily bent forward
    this.headGroup.rotation.set(0.22, 0, 0); // Head drooping / panting
    // Arms braced down on knees
    this.armLeft.rotation.set(0.68, 0.22, -0.16);
    this.armRight.rotation.set(0.68, -0.22, 0.16);
    this.legLeft.rotation.set(0.32, 0, -0.10);
    this.legRight.rotation.set(0.32, 0, 0.10);
  }

  public setLookingUpFromBase(time: number): void {
    const sway = Math.sin(time * 1.0) * 0.02;
    this.torsoGroup.rotation.set(-0.12, sway, 0); // Leaning back slightly
    this.headGroup.rotation.set(-0.55, 0.10, 0); // Head tilted far back gazing at high peak
    // Right hand up to forehead shading eyes
    this.armRight.rotation.set(1.45, -0.65, 0.35);
    // Left arm hanging slightly back
    this.armLeft.rotation.set(-0.15, 0, -0.15);
    this.legLeft.rotation.set(0, 0, -0.10);
    this.legRight.rotation.set(0, 0, 0.10);
  }

  public setSittingDejected(time: number): void {
    this.torsoGroup.rotation.set(0.35, 0, 0); // Slumped forward
    this.headGroup.rotation.set(0.35, 0, 0); // Looking down at ground
    this.legLeft.rotation.set(-Math.PI / 2 + 0.1, 0, -0.15); // Legs sitting flat
    this.legRight.rotation.set(-Math.PI / 2 + 0.1, 0, 0.15);
    this.armLeft.rotation.set(0.4, 0.2, 0.1); // Hands on ground / knees
    this.armRight.rotation.set(0.4, -0.2, -0.1);
  }

  public setStumblingFirstStep(time: number): void {
    const struggle = Math.sin(time * 2.5) * 0.05;
    this.torsoGroup.rotation.set(0.30 + struggle, 0, 0);
    this.headGroup.rotation.set(-0.20, 0, 0);
    this.legRight.rotation.set(-0.65, 0, 0); // Foot lifted onto step 1
    this.legLeft.rotation.set(0.15, 0, 0); // Supporting foot on ground
    this.armLeft.rotation.set(0.70, 0.3, 0); // Arms reaching forward for balance
    this.armRight.rotation.set(0.50, -0.3, 0);
  }

  public setCollapsedBurnout(time: number): void {
    this.resetJoints();
    const heave = Math.sin(time * 3.2) * 0.04;
    // Dropped low to ground on knees beside the shattered trophy
    this.root.position.y = 0.36 + heave * 0.3;
    this.torsoGroup.rotation.set(0.48 + heave, 0, 0); // Slumped heavily forward
    this.headGroup.rotation.set(0.42, 0, 0); // Head hung in complete exhaustion
    // Limp arms resting on knees/floor
    this.armLeft.rotation.set(0.55, 0.25, 0.15);
    this.armRight.rotation.set(0.55, -0.25, -0.15);
    // Legs bent underneath
    this.legLeft.rotation.set(-1.2, 0.1, 0);
    this.legRight.rotation.set(-1.2, -0.1, 0);
  }

  public setDroppingCoin(time: number): void {
    this.resetJoints();
    this.root.position.y = 0.75;

    if (time < 1.8) {
      // Phase 1: Poised at scale, holding golden vote coin poised above right pan
      this.torsoGroup.rotation.set(-0.02, 0.08, 0);
      this.headGroup.rotation.set(0.10, -0.12, 0); // Looking at scale pan
      this.armRight.rotation.set(0.95, -0.25, 0.20); // Right arm extended over pan
      this.armLeft.rotation.set(0.15, 0.10, -0.10);
    } else if (time < 2.6) {
      // Phase 2: Gentle release / drop of coin
      const dropP = (time - 1.8) / 0.8;
      this.torsoGroup.rotation.set(-0.02, 0.08, 0);
      this.headGroup.rotation.set(0.15, -0.10, 0);
      this.armRight.rotation.set(0.95 - dropP * 0.25, -0.20, 0.15);
      this.armLeft.rotation.set(0.15, 0.10, -0.10);
    } else {
      // Phase 3: Scale tips! Alex stands triumphant, chest expanded, looking into golden dawn
      const triumphP = Math.min(1.0, (time - 2.6) / 1.0);
      const breath = Math.sin(time * 1.8) * 0.015;
      this.torsoGroup.rotation.set(-0.08 * triumphP + breath, 0, 0); // Chest up
      this.headGroup.rotation.set(-0.16 * triumphP, 0.05, 0); // Gaze toward endless sunrise
      // Confident stance
      this.armRight.rotation.set(0.20, -0.12, 0.18);
      this.armLeft.rotation.set(0.20, 0.12, -0.18);
      this.legLeft.rotation.set(0, 0, -0.12);
      this.legRight.rotation.set(0, 0, 0.12);
    }
  }

  public setSittingGuiltHeadDown(time: number): void {
    this.resetJoints();
    const breath = Math.sin(time * 1.5) * 0.012;

    // Torso curled forward in heavy remorse & guilt
    this.torsoGroup.rotation.set(0.32 + breath, 0, 0);

    // Head bowed downward in shame, keeping tired face expression visible
    this.headGroup.rotation.set(0.38 + breath * 0.3, -0.10, 0.05);

    // Arms resting forward on knees with hands hanging down in defeat
    this.armLeft.rotation.set(0.85, 0.22, -0.12);
    this.armRight.rotation.set(0.85, -0.22, 0.12);

    // Legs sitting flat on the bed
    this.legLeft.rotation.set(-Math.PI / 2 + 0.04, 0, -0.06);
    this.legRight.rotation.set(-Math.PI / 2 + 0.04, 0, 0.06);
  }

  public setExplainingToHero(time: number): void {
    this.resetJoints();
    const cycle = time * 2.2;
    const breath = Math.sin(time * 1.6) * 0.015;

    // Confident, upright, warm mentor posture
    this.torsoGroup.rotation.set(-0.04 + breath, 0, 0);
    this.headGroup.rotation.set(0.02, -0.15 + Math.sin(cycle * 0.5) * 0.05, 0);

    // Left arm (facing Alex) actively gestures forward in smooth explanatory arc toward him
    const gesture = Math.sin(cycle);
    this.armLeft.rotation.set(
      0.72 + gesture * 0.22,
      0.35 + Math.cos(cycle) * 0.12,
      -0.22
    );

    // Right arm in relaxed conversational cadence
    this.armRight.rotation.set(
      0.28 + Math.cos(cycle * 0.8) * 0.12,
      -0.18,
      0.15
    );

    // Stable, grounded mentor stance
    this.legLeft.rotation.set(0, 0, -0.06);
    this.legRight.rotation.set(0, 0, 0.06);
  }

  public setListeningHero(time: number): void {
    this.resetJoints();
    const nod = Math.sin(time * 1.8) * 0.04;
    const breath = Math.sin(time * 1.5) * 0.012;

    // Attentive posture facing mentor
    this.torsoGroup.rotation.set(0.04 + breath, 0, 0);
    // Subtle attentive nod of understanding
    this.headGroup.rotation.set(0.08 + nod, 0.12, 0);

    // Hands resting naturally in front of waist
    this.armLeft.rotation.set(0.28, 0.20, -0.10);
    this.armRight.rotation.set(0.28, -0.20, 0.10);

    // Grounded stance
    this.legLeft.rotation.set(0, 0, -0.05);
    this.legRight.rotation.set(0, 0, 0.05);
  }

  public setDumbbellCurls(time: number): void {
    this.resetJoints();
    const cycle = time * 3.5;

    // Athletic posture: chest high, slight athletic knee flexion
    this.torsoGroup.rotation.set(0.06, 0, 0);
    this.headGroup.rotation.set(-0.04, 0, 0);

    // Alternating smooth bicep curls with dumbbells
    // Right arm curling up to chest then lowering
    const curlR = Math.max(0, Math.sin(cycle));
    this.armRight.rotation.set(
      0.15 + curlR * 1.35, // Curls from side up to shoulder
      -0.10,
      0.12
    );

    // Left arm curling on opposite half-cycle
    const curlL = Math.max(0, Math.sin(cycle + Math.PI));
    this.armLeft.rotation.set(
      0.15 + curlL * 1.35,
      0.10,
      -0.12
    );

    // Strong athletic stance
    this.legLeft.rotation.set(0.08, 0, -0.08);
    this.legRight.rotation.set(0.08, 0, 0.08);
  }

  public setSittingReadingBook(time: number): void {
    this.resetJoints();
    const breath = Math.sin(time * 1.4) * 0.012;

    // Relaxed, dignified sitting posture
    this.torsoGroup.rotation.set(0.08 + breath, 0, 0);
    // Head angled down looking directly at the book in hands
    this.headGroup.rotation.set(0.38, 0, 0);

    // Both arms raised forward holding book open at chest level
    this.armLeft.rotation.set(0.72, 0.35, -0.22);
    this.armRight.rotation.set(0.72, -0.35, 0.22);

    // Legs seated forward under desk
    this.legLeft.rotation.set(-Math.PI / 2 + 0.12, 0, 0);
    this.legRight.rotation.set(-Math.PI / 2 + 0.12, 0, 0);
  }

  public setShirtColor(hexColor: number): void {
    const shirtMat = new THREE.MeshToonMaterial({ color: hexColor });
    this.torso.material = shirtMat;
    if (this.armLeft.children[0] instanceof THREE.Mesh) {
      this.armLeft.children[0].material = shirtMat;
    }
    if (this.armRight.children[0] instanceof THREE.Mesh) {
      this.armRight.children[0].material = shirtMat;
    }
  }
}


