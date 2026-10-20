import * as THREE from "three";
import { PALETTE, createInkMaterial, createOutlineMesh } from "../materials/CelInkMaterial";

export type StickmanPose =
  | "idle"
  | "lying_in_bed"
  | "running"
  | "typing_at_desk"
  | "proud"
  | "exhausted_slump"
  | "mentor_calm"
  | "pushing_boulder"
  | "stepping_over_hurdle"
  | "dropping_coin";

export class StickmanRig {
  public root: THREE.Group;
  public head: THREE.Mesh;
  public eyeLeft: THREE.Mesh;
  public eyeRight: THREE.Mesh;
  public torso: THREE.Mesh;
  public armLeft: THREE.Group;
  public armRight: THREE.Group;
  public legLeft: THREE.Group;
  public legRight: THREE.Group;

  constructor() {
    this.root = new THREE.Group();

    const whiteMaterial = new THREE.MeshToonMaterial({ color: 0xffffff });
    const inkMaterial = createInkMaterial(PALETTE.ink);

    // 1. Head: Smooth clean white sphere with bold ink outline
    const headGeo = new THREE.SphereGeometry(0.38, 32, 32);
    this.head = new THREE.Mesh(headGeo, whiteMaterial);
    this.head.position.set(0, 1.85, 0);
    this.head.add(createOutlineMesh(headGeo, 0.05, PALETTE.ink));
    this.root.add(this.head);

    // Eyes: Stylized black ink beads
    const eyeGeo = new THREE.SphereGeometry(0.045, 16, 16);
    this.eyeLeft = new THREE.Mesh(eyeGeo, inkMaterial);
    this.eyeLeft.position.set(0.12, 0.05, 0.35);
    this.head.add(this.eyeLeft);

    this.eyeRight = new THREE.Mesh(eyeGeo, inkMaterial);
    this.eyeRight.position.set(-0.12, 0.05, 0.35);
    this.head.add(this.eyeRight);

    // 2. Torso: Tapered capsule spine
    const torsoGeo = new THREE.CylinderGeometry(0.09, 0.08, 0.75, 16);
    this.torso = new THREE.Mesh(torsoGeo, inkMaterial);
    this.torso.position.set(0, 1.25, 0);
    this.root.add(this.torso);

    // 3. Arms with shoulder pivots
    this.armLeft = this.createLimbGroup(0.65, inkMaterial);
    this.armLeft.position.set(0.24, 1.55, 0);
    this.root.add(this.armLeft);

    this.armRight = this.createLimbGroup(0.65, inkMaterial);
    this.armRight.position.set(-0.24, 1.55, 0);
    this.root.add(this.armRight);

    // 4. Legs with hip pivots
    this.legLeft = this.createLimbGroup(0.85, inkMaterial);
    this.legLeft.position.set(0.14, 0.88, 0);
    this.root.add(this.legLeft);

    this.legRight = this.createLimbGroup(0.85, inkMaterial);
    this.legRight.position.set(-0.14, 0.88, 0);
    this.root.add(this.legRight);
  }

  private createLimbGroup(length: number, mat: THREE.Material): THREE.Group {
    const pivot = new THREE.Group();
    const geo = new THREE.CylinderGeometry(0.065, 0.055, length, 12);
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.y = -length / 2;
    pivot.add(mesh);
    return pivot;
  }

  /**
   * Applies biomechanical pose and procedural micro-motion
   */
  public applyPose(pose: StickmanPose, time: number): void {
    const breath = Math.sin(time * 3.0) * 0.02;
    const microSway = Math.sin(time * 1.5) * 0.015;

    // Default reset
    this.root.position.set(0, 0, 0);
    this.root.rotation.set(0, 0, 0);
    this.head.rotation.set(0, 0, 0);
    this.torso.position.y = 1.25 + breath;
    this.armLeft.rotation.set(0, 0, -0.2);
    this.armRight.rotation.set(0, 0, 0.2);
    this.legLeft.rotation.set(0, 0, 0);
    this.legRight.rotation.set(0, 0, 0);

    switch (pose) {
      case "lying_in_bed":
        this.root.position.set(0, 0.45, 0);
        this.root.rotation.x = -Math.PI / 2;
        this.head.rotation.x = Math.PI / 8; // Staring up toward ceiling
        this.armLeft.rotation.z = -0.5;
        this.armRight.rotation.z = 0.5;
        break;

      case "running": {
        const cycle = time * 8.0;
        this.root.position.y = Math.abs(Math.sin(cycle)) * 0.12;
        this.root.rotation.x = 0.25; // Forward athletic lean
        this.armLeft.rotation.x = Math.sin(cycle) * 0.9;
        this.armRight.rotation.x = -Math.sin(cycle) * 0.9;
        this.legLeft.rotation.x = -Math.sin(cycle) * 0.85;
        this.legRight.rotation.x = Math.sin(cycle) * 0.85;
        break;
      }

      case "typing_at_desk":
        this.root.position.y = -0.15;
        this.head.rotation.x = 0.28; // Tilted toward laptop screen
        this.armLeft.rotation.set(0.65, 0.2, -0.3 + Math.sin(time * 12.0) * 0.06);
        this.armRight.rotation.set(0.65, -0.2, 0.3 + Math.cos(time * 14.0) * 0.06);
        this.legLeft.rotation.x = 0.7;
        this.legRight.rotation.x = 0.7;
        break;

      case "proud":
        this.torso.rotation.x = -0.1; // Chest puffed out
        this.head.rotation.x = -0.15; // Chin raised
        this.armLeft.rotation.set(0, 0, -0.65);
        this.armRight.rotation.set(0, 0, 0.65);
        break;

      case "exhausted_slump":
        this.root.position.y = -0.25;
        this.torso.rotation.x = 0.45; // Curved spine slumping
        this.head.rotation.x = 0.55;  // Head hanging low
        this.armLeft.rotation.set(0.3, 0, -0.1);
        this.armRight.rotation.set(0.3, 0, 0.1);
        this.legLeft.rotation.x = 0.5;
        this.legRight.rotation.x = 0.5;
        break;

      case "mentor_calm":
        this.head.rotation.set(microSway, 0, microSway);
        this.armLeft.rotation.set(0.15, 0, -0.15);
        this.armRight.rotation.set(0.15, 0, 0.15);
        break;

      case "pushing_boulder":
        this.root.rotation.x = 0.45; // Deep lunge
        this.armLeft.rotation.set(1.2, 0, -0.2);
        this.armRight.rotation.set(1.2, 0, 0.2);
        this.legLeft.rotation.x = -0.6;
        this.legRight.rotation.x = 0.7;
        break;

      case "stepping_over_hurdle":
        this.legLeft.rotation.x = -0.8; // High step over tiny hurdle
        this.legRight.rotation.x = 0.2;
        this.armLeft.rotation.z = -0.4;
        this.armRight.rotation.z = 0.4;
        break;

      case "dropping_coin":
        this.armRight.rotation.set(0.9, 0, 0.3); // Outstretched arm dropping coin
        this.head.rotation.set(0.2, -0.15, 0);  // Watching coin drop
        break;

      case "idle":
      default:
        this.head.rotation.set(microSway, 0, 0);
        break;
    }
  }
}
