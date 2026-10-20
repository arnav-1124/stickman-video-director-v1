import * as THREE from "three";
import {
  createBookshelfTexture,
  createDayFourTexture,
  createDigitalClockTexture,
  createFramedArtTexture,
  createBedSheetTexture,
  createDawnSkyTexture,
  createMidnightSkyTexture,
  createMinecraftDirtTexture,
  createMinecraftGrassSideTexture,
  createMinecraftGrassTopTexture,
  createMinecraftLeavesTexture,
  createMinecraftOakLogSideTexture,
  createMinecraftOakLogTopTexture,
  createMinecraftRedWoolTexture,
  createMinecraftStoneTexture,
  createMinecraftWhiteWoolTexture,
  createOakPlanksTexture,
  createParkGravelPathTexture,
  createPlasterWallTexture,
  createSpruceFloorTexture,
  createWallCalendarTexture,
  createPhoneScreenTexture,
  createLaptopScreenTexture,
  createNotePaperTexture,
  createVoxelFaceTexture,
  createBrainTelemetryTexture,
  createEmergencyAlarmTexture,
  createGymBannerTexture,
  createLockedBlastDoorTexture,
  createSevenAMClockTexture,
  createLaptopIDETexture,
  createBlueprintSchematicTexture,
  createPhoneLockedTexture,
  createBlankDocTexture,
  createBrokenTrophyPlaqueTexture,
  createTinyHurdleSignTexture,
  createTwoMinuteNotebookTexture,
  createGoldenScaleCoinTexture,
} from "../textures/VoxelTextures";
import { VoxelCharacter } from "../character";

export interface SceneBundle {
  scene: THREE.Scene;
  character: VoxelCharacter;
  update: (time: number, camera?: THREE.PerspectiveCamera) => void;
}

export interface BedroomElements {
  clockFaceMat: THREE.MeshBasicMaterial;
  clockTexOn: THREE.CanvasTexture;
  clockTexOff: THREE.CanvasTexture;
  clockLight: THREE.PointLight;
  buttonTop: THREE.Mesh;
  nightstand: THREE.Mesh;
}

export interface BedroomOptions {
  timeOfDay: "midnight" | "predawn" | "dawn" | "noon" | "morning";
  clockTime: string;
  clockPeriod?: "AM" | "PM";
  clockColor?: "red" | "cyan" | "amber";
  phoneFaceDown?: boolean;
  phonePresent?: boolean;
  shoesPresent?: boolean;
  duvet?: "duvet" | "folded" | "none";
}

export function buildStandardBedroom(
  scene: THREE.Scene,
  floorMat: THREE.Material,
  darkOakTrimMat: THREE.Material,
  whiteWoolMat: THREE.Material,
  oakWallMat: THREE.Material,
  options: BedroomOptions
): BedroomElements {
  // 1. Scene Background based on time of day
  if (options.timeOfDay === "midnight") {
    scene.background = new THREE.Color(0x020409);
  } else if (options.timeOfDay === "predawn") {
    scene.background = new THREE.Color(0x060c18);
  } else if (options.timeOfDay === "dawn") {
    scene.background = new THREE.Color(0x0e1828);
  } else if (options.timeOfDay === "morning") {
    scene.background = new THREE.Color(0xf6ede2);
  } else {
    scene.background = new THREE.Color(0xdbeafe);
  }

  // 2. Hardwood Floor
  const floor = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.2, 6.4), floorMat);
  floor.position.set(0, -0.1, 0);
  scene.add(floor);

  // 3. Plaster Walls
  const plasterTex = createPlasterWallTexture();
  plasterTex.repeat.set(4, 3);
  const plasterWallMat = new THREE.MeshToonMaterial({ map: plasterTex });

  const backWall = new THREE.Mesh(new THREE.BoxGeometry(6.4, 4.0, 0.25), plasterWallMat);
  backWall.position.set(0, 1.9, -2.85);
  scene.add(backWall);

  const leftWallBottom = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.85, 6.4), plasterWallMat);
  leftWallBottom.position.set(-2.85, 0.425, 0);
  scene.add(leftWallBottom);

  const leftWallTop = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.55, 6.4), plasterWallMat);
  leftWallTop.position.set(-2.85, 3.225, 0);
  scene.add(leftWallTop);

  const leftWallBack = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.60, 1.50), plasterWallMat);
  leftWallBack.position.set(-2.85, 1.65, -2.45);
  scene.add(leftWallBack);

  const leftWallFront = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.60, 3.10), plasterWallMat);
  leftWallFront.position.set(-2.85, 1.65, 1.65);
  scene.add(leftWallFront);

  const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.25, 4.0, 6.4), plasterWallMat);
  rightWall.position.set(2.85, 1.9, 0);
  scene.add(rightWall);


  // Baseboards
  const baseboardLeft = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 6.4), darkOakTrimMat);
  baseboardLeft.position.set(-2.71, 0.09, 0);
  scene.add(baseboardLeft);

  const baseboardBack = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.18, 0.08), darkOakTrimMat);
  baseboardBack.position.set(0, 0.09, -2.71);
  scene.add(baseboardBack);

  const baseboardRight = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 6.4), darkOakTrimMat);
  baseboardRight.position.set(2.71, 0.09, 0);
  scene.add(baseboardRight);

  const baseboardFront = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.18, 0.08), darkOakTrimMat);
  baseboardFront.position.set(0, 0.09, 2.71);
  scene.add(baseboardFront);

  // 4. Picture on Back Wall
  const pictureGroup = new THREE.Group();
  pictureGroup.position.set(0.2, 1.65, -2.71);
  const artTex = createFramedArtTexture();
  const artCanvasMat = new THREE.MeshToonMaterial({ map: artTex });
  const artFrameMat = new THREE.MeshToonMaterial({ color: 0x24160e });
  const pictureFrame = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.15, 0.06), artFrameMat);
  pictureGroup.add(pictureFrame);
  const pictureCanvas = new THREE.Mesh(new THREE.BoxGeometry(1.48, 1.03, 0.02), artCanvasMat);
  pictureCanvas.position.set(0, 0, 0.025);
  pictureGroup.add(pictureCanvas);
  scene.add(pictureGroup);

  // 5. Calendar on Back Wall
  const calendarGroup = new THREE.Group();
  calendarGroup.position.set(-1.45, 1.52, -2.71);
  const calTex = createWallCalendarTexture();
  const calMat = new THREE.MeshToonMaterial({ map: calTex });
  const calBackMat = new THREE.MeshToonMaterial({ color: 0xeeeeee });
  const calendarMesh = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.2, 0.03), [
    calBackMat, calBackMat, calBackMat, calBackMat, calMat, calBackMat
  ]);
  calendarGroup.add(calendarMesh);
  const pushpin = new THREE.Mesh(
    new THREE.CylinderGeometry(0.03, 0.03, 0.05, 8),
    new THREE.MeshToonMaterial({ color: 0xcc2222 })
  );
  pushpin.rotation.x = Math.PI / 2;
  pushpin.position.set(0, 0.63, 0.02);
  calendarGroup.add(pushpin);
  scene.add(calendarGroup);

  // 6. Window on Left Wall
  const windowGroup = new THREE.Group();
  windowGroup.position.set(-2.85, 1.65, -0.80);
  const windowCasingMat = new THREE.MeshToonMaterial({ color: 0xefede8 });
  const windowGlassMat = new THREE.MeshBasicMaterial({
    color: options.timeOfDay === "midnight" ? 0xddeeff : 0xffffff,
    transparent: true,
    opacity: 0.12,
    depthWrite: false,
  });
  const winCasingL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.64, 0.08), windowCasingMat);
  winCasingL.position.set(0.06, 0, -0.90);
  windowGroup.add(winCasingL);
  const winCasingR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.64, 0.08), windowCasingMat);
  winCasingR.position.set(0.06, 0, 0.90);
  windowGroup.add(winCasingR);
  const winCasingTop = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.08, 1.88), windowCasingMat);
  winCasingTop.position.set(0.06, 0.82, 0);
  windowGroup.add(winCasingTop);
  const winSill = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.08, 2.06), windowCasingMat);
  winSill.position.set(0.12, -0.82, 0);
  windowGroup.add(winSill);
  const mullionH = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.05, 1.76), windowCasingMat);
  mullionH.position.set(0.06, 0, 0);
  windowGroup.add(mullionH);
  const mullionV = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.56, 0.05), windowCasingMat);
  mullionV.position.set(0.06, 0, 0);
  windowGroup.add(mullionV);
  const winGlass = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.56, 1.76), windowGlassMat);
  winGlass.position.set(0.04, 0, 0);
  windowGroup.add(winGlass);
  scene.add(windowGroup);

  // Outdoor Sky & Distant Pine Trees
  const outdoorGroup = new THREE.Group();
  let outdoorSkyTex: THREE.Texture;
  if (options.timeOfDay === "midnight") {
    outdoorSkyTex = createMidnightSkyTexture();
  } else if (options.timeOfDay === "predawn" || options.timeOfDay === "dawn") {
    outdoorSkyTex = createDawnSkyTexture();
  } else {
    outdoorSkyTex = createDawnSkyTexture();
  }
  const skyMat = new THREE.MeshBasicMaterial({
    map: outdoorSkyTex,
    color: options.timeOfDay === "noon" ? 0x7dd3fc : (options.timeOfDay === "morning" ? 0xfff5e6 : 0xffffff),
  });
  const skyPlane = new THREE.Mesh(new THREE.PlaneGeometry(24, 18), skyMat);
  skyPlane.position.set(-15.0, 1.15, -6.30);
  skyPlane.rotation.y = Math.PI / 2 + 0.44;
  outdoorGroup.add(skyPlane);

  const treeTrunkMat = new THREE.MeshBasicMaterial({ color: 0x05070a });
  const pineFoliageMat1 = new THREE.MeshBasicMaterial({ color: 0x040a08 });
  const pineFoliageMat2 = new THREE.MeshBasicMaterial({ color: 0x030806 });
  const pineFoliageMat3 = new THREE.MeshBasicMaterial({ color: 0x050e0a });
  const createPineTree = (x: number, y: number, z: number, scale: number) => {
    const tree = new THREE.Group();
    tree.position.set(x, y, z);
    tree.scale.set(scale, scale, scale);
    const trunk = new THREE.Mesh(new THREE.BoxGeometry(0.24, 6.0, 0.24), treeTrunkMat);
    trunk.position.y = -1.5;
    tree.add(trunk);
    const tier1 = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.75, 1.4), pineFoliageMat1);
    tier1.position.y = 1.35;
    tree.add(tier1);
    const tier2 = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.70, 1.0), pineFoliageMat2);
    tier2.position.y = 1.90;
    tree.add(tier2);
    const tier3 = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.65, 0.6), pineFoliageMat3);
    tier3.position.y = 2.40;
    tree.add(tier3);
    return tree;
  };
  outdoorGroup.add(createPineTree(-12.0, -0.4, -2.2, 0.60));
  outdoorGroup.add(createPineTree(-13.0, -0.4, -3.2, 0.68));
  outdoorGroup.add(createPineTree(-11.0, -0.4, -4.2, 0.58));
  outdoorGroup.add(createPineTree(-14.0, -0.4, -1.6, 0.52));
  outdoorGroup.add(createPineTree(-14.5, -0.4, -4.8, 0.72));
  scene.add(outdoorGroup);

  // 7. House Bed
  const bedGroup = new THREE.Group();
  bedGroup.position.set(0.2, 0, -0.85);

  const bedFrame = new THREE.Mesh(new THREE.BoxGeometry(1.54, 0.28, 2.66), darkOakTrimMat);
  bedFrame.position.set(0, 0.14, 0);
  bedGroup.add(bedFrame);

  const legGeo = new THREE.BoxGeometry(0.12, 0.28, 0.12);
  for (const [lx, lz] of [[-0.70, -1.26], [0.70, -1.26], [-0.70, 1.26], [0.70, 1.26]]) {
    const leg = new THREE.Mesh(legGeo, darkOakTrimMat);
    leg.position.set(lx, 0.14, lz);
    bedGroup.add(leg);
  }

  const bedSheetTex = createBedSheetTexture();
  bedSheetTex.repeat.set(3, 4);
  const bedSheetMat = new THREE.MeshToonMaterial({ map: bedSheetTex });
  const mattress = new THREE.Mesh(new THREE.BoxGeometry(1.46, 0.38, 2.58), bedSheetMat);
  mattress.position.set(0, 0.40, 0);
  bedGroup.add(mattress);

  const headboard = new THREE.Mesh(new THREE.BoxGeometry(1.56, 1.05, 0.12), darkOakTrimMat);
  headboard.position.set(0, 0.55, -1.33);
  bedGroup.add(headboard);

  const pillow = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.18, 0.60), whiteWoolMat);
  pillow.position.set(0, 0.63, -0.90);
  bedGroup.add(pillow);

  if (options.duvet === "duvet") {
    const duvet = new THREE.Mesh(
      new THREE.BoxGeometry(1.48, 0.20, 1.42),
      new THREE.MeshToonMaterial({ color: 0x334155 })
    );
    duvet.position.set(0, 0.48, -0.15);
    bedGroup.add(duvet);
  } else if (options.duvet === "folded") {
    const foldedDuvet = new THREE.Mesh(
      new THREE.BoxGeometry(1.48, 0.14, 0.8),
      new THREE.MeshToonMaterial({ color: 0x1f2e46 })
    );
    foldedDuvet.position.set(0, 0.48, 0.25);
    bedGroup.add(foldedDuvet);
  }

  scene.add(bedGroup);

  // 8. Nightstand
  const nightstand = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.7, 0.8), darkOakTrimMat);
  nightstand.position.set(1.45, 0.35, -1.3);
  scene.add(nightstand);

  const drawerFront = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.26, 0.04), oakWallMat);
  drawerFront.position.set(1.45, 0.45, -0.88);
  scene.add(drawerFront);

  const drawerKnob = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.05, 0.05), new THREE.MeshToonMaterial({ color: 0xd4af37 }));
  drawerKnob.position.set(1.45, 0.45, -0.85);
  scene.add(drawerKnob);

  // 9. Digital Clock
  const clockColor = options.clockColor || "cyan";
  const clockTexOn = createDigitalClockTexture(options.clockTime, true, clockColor, options.clockPeriod);
  const clockTexOff = createDigitalClockTexture(options.clockTime, false, clockColor, options.clockPeriod);
  const clockFaceMat = new THREE.MeshBasicMaterial({ map: clockTexOn });
  const clockCaseMat = new THREE.MeshBasicMaterial({ color: 0x111115 });
  const clockMesh = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.22, 0.2), [
    clockCaseMat, clockCaseMat, clockCaseMat, clockCaseMat, clockFaceMat, clockCaseMat
  ]);
  clockMesh.position.set(1.45, 0.82, -1.2);
  clockMesh.rotation.y = -0.28;

  const buttonBezel = new THREE.Mesh(
    new THREE.BoxGeometry(0.18, 0.02, 0.08),
    new THREE.MeshBasicMaterial({ color: 0x220509 })
  );
  buttonBezel.position.set(0, 0.115, 0);
  clockMesh.add(buttonBezel);

  const btnColor = clockColor === "red" ? 0xff1a40 : (clockColor === "amber" ? 0xf59e0b : 0x00f0ff);
  const buttonTop = new THREE.Mesh(
    new THREE.BoxGeometry(0.15, 0.03, 0.06),
    new THREE.MeshBasicMaterial({ color: btnColor })
  );
  buttonTop.position.set(0, 0.128, 0);
  clockMesh.add(buttonTop);
  scene.add(clockMesh);

  const clockLight = new THREE.PointLight(btnColor, 1.8, 2.5);
  clockLight.position.set(1.45, 0.9, -1.0);
  scene.add(clockLight);

  // 10. Smartphone
  if (options.phonePresent !== false) {
    const phoneGroup = new THREE.Group();
    phoneGroup.position.set(1.24, 0.708, -0.98);
    phoneGroup.rotation.y = 0.48;

    const phoneBody = new THREE.Mesh(
      new THREE.BoxGeometry(0.16, 0.012, 0.30),
      new THREE.MeshToonMaterial({ color: 0x16181d })
    );
    phoneGroup.add(phoneBody);

    if (options.phoneFaceDown) {
      const cameraBump = new THREE.Mesh(
        new THREE.BoxGeometry(0.045, 0.008, 0.045),
        new THREE.MeshBasicMaterial({ color: 0x0c0e12 })
      );
      cameraBump.position.set(-0.045, 0.008, -0.11);
      phoneGroup.add(cameraBump);
    } else {
      const phoneScreenTex = createPhoneScreenTexture();
      const phoneScreenMat = new THREE.MeshBasicMaterial({ map: phoneScreenTex });
      const phoneScreen = new THREE.Mesh(new THREE.PlaneGeometry(0.145, 0.285), phoneScreenMat);
      phoneScreen.rotation.x = -Math.PI / 2;
      phoneScreen.position.y = 0.007;
      phoneGroup.add(phoneScreen);
    }
    scene.add(phoneGroup);
  }

  // 11. Running shoes
  if (options.shoesPresent) {
    const gearGroup = new THREE.Group();
    gearGroup.position.set(1.30, 0.0, -0.55);
    const sneakerMat = new THREE.MeshToonMaterial({ color: 0x0284c7 });
    const soleMat = new THREE.MeshToonMaterial({ color: 0xf8fafc });
    const makeShoe = (sx: number, rotY: number = 0) => {
      const g = new THREE.Group();
      g.position.set(sx, 0, 0);
      g.rotation.y = rotY;
      const sole = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.05, 0.40), soleMat);
      sole.position.set(0, 0.025, 0);
      g.add(sole);
      const upper = new THREE.Mesh(new THREE.BoxGeometry(0.17, 0.12, 0.38), sneakerMat);
      upper.position.set(0, 0.10, -0.01);
      g.add(upper);
      return g;
    };
    gearGroup.add(makeShoe(-0.16));
    gearGroup.add(makeShoe(0.16, 0.22));
    scene.add(gearGroup);
  }

  // 12. Lighting matching timeOfDay
  if (options.timeOfDay === "midnight") {
    const moonlight = new THREE.DirectionalLight(0x406095, 1.4);
    moonlight.position.set(-5.5, 3.8, -0.9);
    scene.add(moonlight);
    scene.add(new THREE.AmbientLight(0x0e1726, 0.85));
  } else if (options.timeOfDay === "predawn") {
    const coldWindow = new THREE.DirectionalLight(0x527a9e, 1.35);
    coldWindow.position.set(-4.5, 3.5, 0.5);
    scene.add(coldWindow);
    scene.add(new THREE.AmbientLight(0x283850, 1.25));
  } else if (options.timeOfDay === "dawn") {
    const dawnSun = new THREE.DirectionalLight(0xffb74d, 2.2);
    dawnSun.position.set(-5.0, 3.8, 0.5);
    scene.add(dawnSun);
    scene.add(new THREE.AmbientLight(0x384860, 1.10));
  } else if (options.timeOfDay === "morning") {
    const morningSun = new THREE.DirectionalLight(0xffeedd, 2.4);
    morningSun.position.set(-5.0, 4.0, 0.5);
    scene.add(morningSun);
    scene.add(new THREE.AmbientLight(0xfff3e0, 1.15));
  } else {
    // noon
    const noonSun = new THREE.DirectionalLight(0xfffaed, 2.8);
    noonSun.position.set(-6.0, 5.0, -0.2);
    scene.add(noonSun);
    scene.add(new THREE.AmbientLight(0xdbeafe, 1.20));
  }

  return { clockFaceMat, clockTexOn, clockTexOff, clockLight, buttonTop, nightstand };
}

export function createThoughtBubbleWithFire(): {
  group: THREE.Group;
  update: (t: number) => void;
} {
  const group = new THREE.Group();
  group.position.set(0.2, 1.1, -0.85); // Positioned above Alex's head in bed

  const bubbleMat = new THREE.MeshToonMaterial({
    color: 0xf8fafc,
    transparent: true,
    opacity: 0.45,
  });

  // 3 ascending connector puffs
  const p1 = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 12), bubbleMat);
  p1.position.set(0.10, 0.15, 0.05);
  group.add(p1);

  const p2 = new THREE.Mesh(new THREE.SphereGeometry(0.09, 12, 12), bubbleMat);
  p2.position.set(0.20, 0.32, 0.08);
  group.add(p2);

  const p3 = new THREE.Mesh(new THREE.SphereGeometry(0.14, 12, 12), bubbleMat);
  p3.position.set(0.32, 0.52, 0.12);
  group.add(p3);

  // Main Thought Cloud Container
  const cloudGroup = new THREE.Group();
  cloudGroup.position.set(0.55, 0.88, 0.18);

  const cloudOffsets = [
    [0, 0, 0, 0.36],
    [-0.22, -0.05, 0.02, 0.26],
    [0.22, -0.04, 0.02, 0.28],
    [-0.12, 0.16, -0.02, 0.26],
    [0.14, 0.14, -0.02, 0.27],
    [0, -0.12, 0.04, 0.24],
  ];
  cloudOffsets.forEach(([cx, cy, cz, cr]) => {
    const s = new THREE.Mesh(new THREE.SphereGeometry(cr, 14, 14), bubbleMat);
    s.position.set(cx, cy, cz);
    cloudGroup.add(s);
  });

  // Voxel Flame cluster INSIDE the thought cloud
  const flameGroup = new THREE.Group();
  const flameColors = [0xff2200, 0xff5500, 0xffaa00, 0xffdd00, 0xff4411];
  const flameMeshes: { mesh: THREE.Mesh; basePos: THREE.Vector3; seed: number }[] = [];
  for (let i = 0; i < 16; i++) {
    const col = flameColors[i % flameColors.length];
    const mat = new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.95 });
    const size = 0.06 + (i % 3) * 0.025;
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(size, size * 1.35, size), mat);
    const bx = (Math.random() - 0.5) * 0.24;
    const by = (Math.random() - 0.5) * 0.20;
    const bz = (Math.random() - 0.5) * 0.15;
    mesh.position.set(bx, by, bz);
    flameGroup.add(mesh);
    flameMeshes.push({ mesh, basePos: new THREE.Vector3(bx, by, bz), seed: i * 1.5 });
  }
  cloudGroup.add(flameGroup);

  const fireGlow = new THREE.PointLight(0xff7700, 2.2, 2.0);
  fireGlow.position.set(0, 0, 0.1);
  cloudGroup.add(fireGlow);

  group.add(cloudGroup);

  const update = (t: number) => {
    cloudGroup.position.y = 0.88 + Math.sin(t * 2.5) * 0.025;
    cloudGroup.position.x = 0.55 + Math.cos(t * 2.0) * 0.02;

    flameMeshes.forEach(({ mesh, basePos, seed }) => {
      const flickY = Math.sin(t * 14.0 + seed) * 0.025;
      mesh.position.y = basePos.y + flickY;
      mesh.scale.y = 1.0 + Math.sin(t * 10.0 + seed) * 0.2;
    });
    fireGlow.intensity = 2.0 + Math.sin(t * 12.0) * 0.5;
  };

  return { group, update };
}

export function buildSceneByShotId(shotId: number): SceneBundle {
  const scene = new THREE.Scene();
  const character = new VoxelCharacter();
  scene.add(character.root);

  // Common textures
  const oakTex = createOakPlanksTexture();
  const floorTex = createSpruceFloorTexture();
  const bookshelfTex = createBookshelfTexture();
  oakTex.repeat.set(4, 2);
  floorTex.repeat.set(3, 3);

  const oakWallMat = new THREE.MeshToonMaterial({ map: oakTex });
  const floorMat = new THREE.MeshToonMaterial({ map: floorTex });
  const bookshelfMat = new THREE.MeshToonMaterial({ map: bookshelfTex });
  const darkOakTrimMat = new THREE.MeshToonMaterial({ color: 0x3d2714 });

  // Authentic Minecraft Block Materials
  const grassSideMat = new THREE.MeshToonMaterial({ map: createMinecraftGrassSideTexture() });
  const grassTopMat = new THREE.MeshToonMaterial({ map: createMinecraftGrassTopTexture() });
  const dirtMat = new THREE.MeshToonMaterial({ map: createMinecraftDirtTexture() });
  const stoneMat = new THREE.MeshToonMaterial({ map: createMinecraftStoneTexture() });
  const oakLogSideMat = new THREE.MeshToonMaterial({ map: createMinecraftOakLogSideTexture() });
  const oakLogTopMat = new THREE.MeshToonMaterial({ map: createMinecraftOakLogTopTexture() });
  const leavesMat = new THREE.MeshToonMaterial({ map: createMinecraftLeavesTexture() });
  const redWoolMat = new THREE.MeshToonMaterial({ map: createMinecraftRedWoolTexture() });
  const whiteWoolMat = new THREE.MeshToonMaterial({ map: createMinecraftWhiteWoolTexture() });

  const grassBlockMats = [
    grassSideMat, grassSideMat, grassTopMat, dirtMat, grassSideMat, grassSideMat
  ];
  const oakLogMats = [
    oakLogSideMat, oakLogSideMat, oakLogTopMat, oakLogTopMat, oakLogSideMat, oakLogSideMat
  ];

  let customUpdate = (time: number, camera?: THREE.PerspectiveCamera) => {};

  // =========================================================================
  // SCENE 1: THE 2:00 AM MIDNIGHT BEDROOM (Shot 1)
  // Real house bedroom walls, hanging picture, calendar, window with deep midnight sky,
  // luminous far moon painted in celestial background, distant trees, 02:00 AM clock,
  // fitted bed-sheet, and character lying in bed with head on pillow.
  // =========================================================================
  if (shotId === 1) {
    scene.background = new THREE.Color(0x020409); // 2:00 AM deep midnight void

    // 1. Hardwood Floor
    const floor = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.2, 6.4), floorMat);
    floor.position.set(0, -0.1, 0);
    scene.add(floor);

    // 2. Real House Drywall / Plaster Walls
    const plasterTex = createPlasterWallTexture();
    plasterTex.repeat.set(4, 3);
    const plasterWallMat = new THREE.MeshToonMaterial({ map: plasterTex });

    // Back Wall
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(6.4, 4.0, 0.25), plasterWallMat);
    backWall.position.set(0, 1.9, -2.85);
    scene.add(backWall);

    // Left Wall with True Open Window Aperture (z: -1.7 to 0.1, y: 0.85 to 2.45)
    // 2a. Bottom section below window sill
    const leftWallBottom = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.85, 6.4), plasterWallMat);
    leftWallBottom.position.set(-2.85, 0.425, 0);
    scene.add(leftWallBottom);

    // 2b. Top section above window
    const leftWallTop = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.55, 6.4), plasterWallMat);
    leftWallTop.position.set(-2.85, 3.225, 0);
    scene.add(leftWallTop);

    // 2c. Back section behind window (towards headboard)
    const leftWallBack = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.60, 1.50), plasterWallMat);
    leftWallBack.position.set(-2.85, 1.65, -2.45);
    scene.add(leftWallBack);

    // 2d. Front section in front of window (towards foot of room)
    const leftWallFront = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.60, 3.10), plasterWallMat);
    leftWallFront.position.set(-2.85, 1.65, 1.65);
    scene.add(leftWallFront);

    // Baseboard along left wall
    const baseboardLeft = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 6.4), darkOakTrimMat);
    baseboardLeft.position.set(-2.71, 0.09, 0);
    scene.add(baseboardLeft);

    // Realistic Baseboard Skirting
    const baseboardBack = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.18, 0.08), darkOakTrimMat);
    baseboardBack.position.set(0, 0.09, -2.71);
    scene.add(baseboardBack);

    // Right Wall (Closes bedroom on the right - eliminates blue background void)
    const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.25, 4.0, 6.4), plasterWallMat);
    rightWall.position.set(2.85, 1.9, 0);
    scene.add(rightWall);

    const baseboardRight = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 6.4), darkOakTrimMat);
    baseboardRight.position.set(2.71, 0.09, 0);
    scene.add(baseboardRight);

    // Front Wall (Closes bedroom on the foot side)
    const frontWall = new THREE.Mesh(new THREE.BoxGeometry(6.4, 4.0, 0.25), plasterWallMat);
    frontWall.position.set(0, 1.9, 2.85);
    scene.add(frontWall);

    const baseboardFront = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.18, 0.08), darkOakTrimMat);
    baseboardFront.position.set(0, 0.09, 2.71);
    scene.add(baseboardFront);

    // 3. Picture Hanging Behind the Bed Wall (Lowered to clear view)
    const pictureGroup = new THREE.Group();
    pictureGroup.position.set(0.2, 1.65, -2.71);

    const artTex = createFramedArtTexture();
    const artCanvasMat = new THREE.MeshToonMaterial({ map: artTex });
    const artFrameMat = new THREE.MeshToonMaterial({ color: 0x24160e });

    const pictureFrame = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.15, 0.06), artFrameMat);
    pictureGroup.add(pictureFrame);

    const pictureCanvas = new THREE.Mesh(new THREE.BoxGeometry(1.48, 1.03, 0.02), artCanvasMat);
    pictureCanvas.position.set(0, 0, 0.025);
    pictureGroup.add(pictureCanvas);

    // Small nail / bracket at top
    const pictureBracket = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 0.04), darkOakTrimMat);
    pictureBracket.position.set(0, 0.62, 0.01);
    pictureGroup.add(pictureBracket);
    scene.add(pictureGroup);

    // 4. Calendar Hanging on the Left Side of the Same Wall (Lowered to clear view)
    const calendarGroup = new THREE.Group();
    calendarGroup.position.set(-1.45, 1.52, -2.71);

    const calTex = createWallCalendarTexture();
    const calMat = new THREE.MeshToonMaterial({ map: calTex });
    const calBackMat = new THREE.MeshToonMaterial({ color: 0xeeeeee });

    const calendarMesh = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.2, 0.03), [
      calBackMat, calBackMat, calBackMat, calBackMat, calMat, calBackMat
    ]);
    calendarGroup.add(calendarMesh);

    // Red pushpin at top
    const pushpin = new THREE.Mesh(
      new THREE.CylinderGeometry(0.03, 0.03, 0.05, 8),
      new THREE.MeshToonMaterial({ color: 0xcc2222 })
    );
    pushpin.rotation.x = Math.PI / 2;
    pushpin.position.set(0, 0.63, 0.02);
    calendarGroup.add(pushpin);
    scene.add(calendarGroup);

    // 5. Transparent Window on the Left Wall with Outside Sky, Small Moon, and Distant Trees
    const windowGroup = new THREE.Group();
    windowGroup.position.set(-2.85, 1.65, -0.80);

    const windowCasingMat = new THREE.MeshToonMaterial({ color: 0xefede8 });
    const windowGlassMat = new THREE.MeshBasicMaterial({
      color: 0xddeeff,
      transparent: true,
      opacity: 0.10,
      depthWrite: false,
    });

    // Outer Window Frame / Casing around opening
    const winCasingL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.64, 0.08), windowCasingMat);
    winCasingL.position.set(0.06, 0, -0.90);
    windowGroup.add(winCasingL);

    const winCasingR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.64, 0.08), windowCasingMat);
    winCasingR.position.set(0.06, 0, 0.90);
    windowGroup.add(winCasingR);

    const winCasingTop = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.08, 1.88), windowCasingMat);
    winCasingTop.position.set(0.06, 0.82, 0);
    windowGroup.add(winCasingTop);

    // Protruding Window Sill
    const winSill = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.08, 2.06), windowCasingMat);
    winSill.position.set(0.12, -0.82, 0);
    windowGroup.add(winSill);

    // 4-Pane Cross Mullions
    const mullionH = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.05, 1.76), windowCasingMat);
    mullionH.position.set(0.06, 0, 0);
    windowGroup.add(mullionH);

    const mullionV = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.56, 0.05), windowCasingMat);
    mullionV.position.set(0.06, 0, 0);
    windowGroup.add(mullionV);

    // Truly Transparent Glass Pane
    const winGlass = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.56, 1.76), windowGlassMat);
    winGlass.position.set(0.04, 0, 0);
    windowGroup.add(winGlass);
    scene.add(windowGroup);

    // =========================================================================
    // OUTDOOR WORLD (Visible through the transparent window)
    // 2:00 AM dark midnight sky with luminous moon painted directly into the celestial
    // background at distance (NO separate geometric hard decal), and distant pine trees.
    // =========================================================================
    const outdoorGroup = new THREE.Group();

    // 5a. Sky Backdrop Plane (Positioned at distance in camera sightline)
    const skyTex = createMidnightSkyTexture();
    const skyMat = new THREE.MeshBasicMaterial({ map: skyTex });
    const skyPlane = new THREE.Mesh(new THREE.PlaneGeometry(24, 18), skyMat);
    skyPlane.position.set(-15.0, 1.15, -6.30);
    skyPlane.rotation.y = Math.PI / 2 + 0.44;
    outdoorGroup.add(skyPlane);

    // 5b. Distant Silhouette Pine Trees (Very far distant, rooted deeply below window frame)
    const treeTrunkMat = new THREE.MeshBasicMaterial({ color: 0x05070a });
    const pineFoliageMat1 = new THREE.MeshBasicMaterial({ color: 0x040a08 });
    const pineFoliageMat2 = new THREE.MeshBasicMaterial({ color: 0x030806 });
    const pineFoliageMat3 = new THREE.MeshBasicMaterial({ color: 0x050e0a });

    const createPineTree = (x: number, y: number, z: number, scale: number) => {
      const tree = new THREE.Group();
      tree.position.set(x, y, z);
      tree.scale.set(scale, scale, scale);

      // Deep Trunk extending far down into ground so it never floats
      const trunk = new THREE.Mesh(new THREE.BoxGeometry(0.24, 6.0, 0.24), treeTrunkMat);
      trunk.position.y = -1.5;
      tree.add(trunk);

      // Tiered Voxel Pine Needles
      const tier1 = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.75, 1.4), pineFoliageMat1);
      tier1.position.y = 1.35;
      tree.add(tier1);

      const tier2 = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.70, 1.0), pineFoliageMat2);
      tier2.position.y = 1.90;
      tree.add(tier2);

      const tier3 = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.65, 0.6), pineFoliageMat3);
      tier3.position.y = 2.40;
      tree.add(tier3);

      return tree;
    };

    // Solid dark forest ground layer extending deep down below window sill
    const outdoorGround = new THREE.Mesh(
      new THREE.BoxGeometry(20, 4.0, 20),
      new THREE.MeshBasicMaterial({ color: 0x020407 })
    );
    outdoorGround.position.set(-13.0, -2.1, -4.0);
    outdoorGroup.add(outdoorGround);

    // Trees at far distance standing in lower half of window view
    outdoorGroup.add(createPineTree(-12.0, -0.4, -2.2, 0.60));
    outdoorGroup.add(createPineTree(-13.0, -0.4, -3.2, 0.68));
    outdoorGroup.add(createPineTree(-11.0, -0.4, -4.2, 0.58));
    outdoorGroup.add(createPineTree(-14.0, -0.4, -1.6, 0.52));
    outdoorGroup.add(createPineTree(-14.5, -0.4, -4.8, 0.72));

    scene.add(outdoorGroup);

    // 6. Real House Bed with Crisp Linen Bed-Sheet, Headboard, and Plush Pillow
    // (Blanket on top of character completely removed as requested)
    const bedGroup = new THREE.Group();
    bedGroup.position.set(0.2, 0, -0.85);

    // Sturdy Wooden Bed Frame (Dark oak)
    const bedFrame = new THREE.Mesh(new THREE.BoxGeometry(1.54, 0.28, 2.66), darkOakTrimMat);
    bedFrame.position.set(0, 0.14, 0);
    bedGroup.add(bedFrame);

    // 4 Corner Wooden Bed Legs
    const legGeo = new THREE.BoxGeometry(0.12, 0.28, 0.12);
    for (const [lx, lz] of [[-0.70, -1.26], [0.70, -1.26], [-0.70, 1.26], [0.70, 1.26]]) {
      const leg = new THREE.Mesh(legGeo, darkOakTrimMat);
      leg.position.set(lx, 0.14, lz);
      bedGroup.add(leg);
    }

    // Fitted Mattress with Crisp Warm-Ivory Linen Bed-Sheet
    const bedSheetTex = createBedSheetTexture();
    bedSheetTex.repeat.set(3, 4);
    const bedSheetMat = new THREE.MeshToonMaterial({ map: bedSheetTex });
    const mattress = new THREE.Mesh(new THREE.BoxGeometry(1.46, 0.38, 2.58), bedSheetMat);
    mattress.position.set(0, 0.40, 0);
    bedGroup.add(mattress);

    // Dark Oak Headboard (against back wall)
    const headboard = new THREE.Mesh(new THREE.BoxGeometry(1.56, 1.05, 0.12), darkOakTrimMat);
    headboard.position.set(0, 0.55, -1.33);
    bedGroup.add(headboard);

    // Plush White Pillow at the head of the bed (z = -0.90 in bedGroup -> world z = -1.75)
    const pillow = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.18, 0.60), whiteWoolMat);
    pillow.position.set(0, 0.63, -0.90);
    bedGroup.add(pillow);

    scene.add(bedGroup);

    // 7. Nightstand with glowing 02:00 AM Digital Alarm Clock (Dark Oak Frame)
    const nightstand = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.7, 0.8), darkOakTrimMat);
    nightstand.position.set(1.45, 0.35, -1.3);
    scene.add(nightstand);

    // Drawer Front Panel
    const drawerFront = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.26, 0.04), oakWallMat);
    drawerFront.position.set(1.45, 0.45, -0.88);
    scene.add(drawerFront);

    // Drawer Brass Knob
    const drawerKnob = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.05, 0.05), new THREE.MeshToonMaterial({ color: 0xd4af37 }));
    drawerKnob.position.set(1.45, 0.45, -0.85);
    scene.add(drawerKnob);

    const clockTexOn = createDigitalClockTexture("02:00", true);
    const clockTexOff = createDigitalClockTexture("02:00", false);
    const clockFaceMat = new THREE.MeshBasicMaterial({ map: clockTexOn });
    const clockCaseMat = new THREE.MeshBasicMaterial({ color: 0x111115 });
    const clockMesh = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.22, 0.2), [
      clockCaseMat, clockCaseMat, clockCaseMat, clockCaseMat, clockFaceMat, clockCaseMat
    ]);
    clockMesh.position.set(1.45, 0.82, -1.2);
    clockMesh.rotation.y = -0.28;

    // Glowing Red Snooze / Alarm Button on Top of the Clock
    const buttonBezel = new THREE.Mesh(
      new THREE.BoxGeometry(0.18, 0.02, 0.08),
      new THREE.MeshBasicMaterial({ color: 0x220509 })
    );
    buttonBezel.position.set(0, 0.115, 0);
    clockMesh.add(buttonBezel);

    const buttonTop = new THREE.Mesh(
      new THREE.BoxGeometry(0.15, 0.03, 0.06),
      new THREE.MeshBasicMaterial({ color: 0xff1a40 })
    );
    buttonTop.position.set(0, 0.128, 0);
    clockMesh.add(buttonTop);

    // Glowing halo on the button
    const buttonGlow = new THREE.PointLight(0xff1a40, 1.2, 0.5);
    buttonGlow.position.set(0, 0.16, 0);
    clockMesh.add(buttonGlow);

    scene.add(clockMesh);

    // Red LED light glow from alarm clock face
    const clockLight = new THREE.PointLight(0xff1a40, 2.2, 2.8);
    clockLight.position.set(1.45, 0.9, -1.0);
    scene.add(clockLight);

    // Modern Smartphone placed organically/casually on nightstand away from clock
    const phoneGroup = new THREE.Group();
    phoneGroup.position.set(1.24, 0.708, -0.98);
    phoneGroup.rotation.y = 0.48; // Casually tossed at an organic diagonal angle

    // Phone body (matte obsidian aluminum)
    const phoneBody = new THREE.Mesh(
      new THREE.BoxGeometry(0.16, 0.012, 0.30),
      new THREE.MeshToonMaterial({ color: 0x16181d })
    );
    phoneGroup.add(phoneBody);

    // Glossy OLED lockscreen face
    const phoneScreenTex = createPhoneScreenTexture();
    const phoneScreenMat = new THREE.MeshBasicMaterial({ map: phoneScreenTex });
    const phoneScreen = new THREE.Mesh(
      new THREE.PlaneGeometry(0.145, 0.285),
      phoneScreenMat
    );
    phoneScreen.rotation.x = -Math.PI / 2;
    phoneScreen.position.y = 0.007;
    phoneGroup.add(phoneScreen);

    scene.add(phoneGroup);

    // 2:00 AM Cool Moonlight through window
    const moonlight = new THREE.DirectionalLight(0x406095, 1.4);
    moonlight.position.set(-5.5, 3.8, -0.9);
    scene.add(moonlight);

    // Deep midnight ambient fill for room visibility
    scene.add(new THREE.AmbientLight(0x0e1726, 0.85));

    // 8. Place Alex so his head is resting squarely on the pillow
    // Pillow world center: x = 0.2, y = 0.62, z = -1.75
    // Character root at z = -0.35 means head (offset -1.4 in Z) is at z = -1.75!
    character.root.position.set(0.2, 0, -0.35);

    customUpdate = (t) => {
      character.setLyingInBed(t);
      const blinkState = Math.floor(t * 1.8) % 2 === 0;
      clockFaceMat.map = blinkState ? clockTexOn : clockTexOff;
      clockFaceMat.needsUpdate = true;
    };
  }

  // =========================================================================
  // SCENE 201: THE 5:00 AM DAWN BEDROOM (Clip 02 - Phase 1 Wakeup)
  // Character sitting up as morning dawn light pours through the window,
  // digital clock reads 05:00 AM, phone turned face-down on nightstand.
  // =========================================================================
  else if (shotId === 201) {
    scene.background = new THREE.Color(0x0e1828); // 5:00 AM dawn blue-hour sky

    // 1. Hardwood Floor
    const floor = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.2, 6.4), floorMat);
    floor.position.set(0, -0.1, 0);
    scene.add(floor);

    // 2. Real House Plaster Walls
    const plasterTex = createPlasterWallTexture();
    plasterTex.repeat.set(4, 3);
    const plasterWallMat = new THREE.MeshToonMaterial({ map: plasterTex });

    // Back Wall
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(6.4, 4.0, 0.25), plasterWallMat);
    backWall.position.set(0, 1.9, -2.85);
    scene.add(backWall);

    // Left Wall with True Open Window Aperture
    const leftWallBottom = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.85, 6.4), plasterWallMat);
    leftWallBottom.position.set(-2.85, 0.425, 0);
    scene.add(leftWallBottom);

    const leftWallTop = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.55, 6.4), plasterWallMat);
    leftWallTop.position.set(-2.85, 3.225, 0);
    scene.add(leftWallTop);

    const leftWallBack = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.60, 1.50), plasterWallMat);
    leftWallBack.position.set(-2.85, 1.65, -2.45);
    scene.add(leftWallBack);

    const leftWallFront = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.60, 3.10), plasterWallMat);
    leftWallFront.position.set(-2.85, 1.65, 1.65);
    scene.add(leftWallFront);

    // Dark Oak Baseboards
    const baseboardLeft = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 6.4), darkOakTrimMat);
    baseboardLeft.position.set(-2.71, 0.09, 0);
    scene.add(baseboardLeft);

    const baseboardBack = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.18, 0.08), darkOakTrimMat);
    baseboardBack.position.set(0, 0.09, -2.71);
    scene.add(baseboardBack);

    // Right Wall (Closes bedroom on the right - eliminates blue void completely)
    const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.25, 4.0, 6.4), plasterWallMat);
    rightWall.position.set(2.85, 1.9, 0);
    scene.add(rightWall);

    const baseboardRight = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 6.4), darkOakTrimMat);
    baseboardRight.position.set(2.71, 0.09, 0);
    scene.add(baseboardRight);

    // Front Wall (Closes bedroom on the foot side)
    const frontWall = new THREE.Mesh(new THREE.BoxGeometry(6.4, 4.0, 0.25), plasterWallMat);
    frontWall.position.set(0, 1.9, 2.85);
    scene.add(frontWall);

    const baseboardFront = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.18, 0.08), darkOakTrimMat);
    baseboardFront.position.set(0, 0.09, 2.71);
    scene.add(baseboardFront);

    // 3. Picture Hanging Behind the Bed Wall
    const pictureGroup = new THREE.Group();
    pictureGroup.position.set(0.2, 1.65, -2.71);
    const artTex = createFramedArtTexture();
    const artCanvasMat = new THREE.MeshToonMaterial({ map: artTex });
    const artFrameMat = new THREE.MeshToonMaterial({ color: 0x24160e });
    const pictureFrame = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.15, 0.06), artFrameMat);
    pictureGroup.add(pictureFrame);
    const pictureCanvas = new THREE.Mesh(new THREE.BoxGeometry(1.48, 1.03, 0.02), artCanvasMat);
    pictureCanvas.position.set(0, 0, 0.025);
    pictureGroup.add(pictureCanvas);
    const pictureBracket = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 0.04), darkOakTrimMat);
    pictureBracket.position.set(0, 0.62, 0.01);
    pictureGroup.add(pictureBracket);
    scene.add(pictureGroup);

    // 4. Calendar Hanging on the Left Side
    const calendarGroup = new THREE.Group();
    calendarGroup.position.set(-1.45, 1.52, -2.71);
    const calTex = createWallCalendarTexture();
    const calMat = new THREE.MeshToonMaterial({ map: calTex });
    const calBackMat = new THREE.MeshToonMaterial({ color: 0xeeeeee });
    const calendarMesh = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.2, 0.03), [
      calBackMat, calBackMat, calBackMat, calBackMat, calMat, calBackMat
    ]);
    calendarGroup.add(calendarMesh);
    const pushpin = new THREE.Mesh(
      new THREE.CylinderGeometry(0.03, 0.03, 0.05, 8),
      new THREE.MeshToonMaterial({ color: 0xcc2222 })
    );
    pushpin.rotation.x = Math.PI / 2;
    pushpin.position.set(0, 0.63, 0.02);
    calendarGroup.add(pushpin);
    scene.add(calendarGroup);

    // 5. Window Frame & Glass
    const windowGroup = new THREE.Group();
    windowGroup.position.set(-2.85, 1.65, -0.80);
    const windowCasingMat = new THREE.MeshToonMaterial({ color: 0xefede8 });
    const windowGlassMat = new THREE.MeshBasicMaterial({
      color: 0xffeedd,
      transparent: true,
      opacity: 0.12,
      depthWrite: false,
    });
    const winCasingL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.64, 0.08), windowCasingMat);
    winCasingL.position.set(0.06, 0, -0.90);
    windowGroup.add(winCasingL);
    const winCasingR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.64, 0.08), windowCasingMat);
    winCasingR.position.set(0.06, 0, 0.90);
    windowGroup.add(winCasingR);
    const winCasingTop = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.08, 1.88), windowCasingMat);
    winCasingTop.position.set(0.06, 0.82, 0);
    windowGroup.add(winCasingTop);
    const winSill = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.08, 2.06), windowCasingMat);
    winSill.position.set(0.12, -0.82, 0);
    windowGroup.add(winSill);
    const mullionH = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.05, 1.76), windowCasingMat);
    mullionH.position.set(0.06, 0, 0);
    windowGroup.add(mullionH);
    const mullionV = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.56, 0.05), windowCasingMat);
    mullionV.position.set(0.06, 0, 0);
    windowGroup.add(mullionV);
    const winGlass = new THREE.Mesh(new THREE.BoxGeometry(0.02, 1.56, 1.76), windowGlassMat);
    winGlass.position.set(0.04, 0, 0);
    windowGroup.add(winGlass);
    scene.add(windowGroup);

    // 5a. Outdoor Dawn Backdrop (5:00 AM Sky + Horizon Amber)
    const outdoorGroup = new THREE.Group();
    const skyTex = createDawnSkyTexture();
    const skyMat = new THREE.MeshBasicMaterial({ map: skyTex });
    const skyPlane = new THREE.Mesh(new THREE.PlaneGeometry(24, 18), skyMat);
    skyPlane.position.set(-15.0, 1.15, -6.30);
    skyPlane.rotation.y = Math.PI / 2 + 0.44;
    outdoorGroup.add(skyPlane);

    // Distant trees
    const treeTrunkMat = new THREE.MeshBasicMaterial({ color: 0x0c1015 });
    const pineFoliageMat1 = new THREE.MeshBasicMaterial({ color: 0x11241a });
    const createPineTree = (x: number, y: number, z: number, scale: number) => {
      const tree = new THREE.Group();
      tree.position.set(x, y, z);
      tree.scale.set(scale, scale, scale);
      const trunk = new THREE.Mesh(new THREE.BoxGeometry(0.24, 6.0, 0.24), treeTrunkMat);
      trunk.position.y = -1.5;
      tree.add(trunk);
      const t1 = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.75, 1.4), pineFoliageMat1);
      t1.position.y = 1.35;
      tree.add(t1);
      const t2 = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.70, 1.0), pineFoliageMat1);
      t2.position.y = 1.90;
      tree.add(t2);
      const t3 = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.65, 0.6), pineFoliageMat1);
      t3.position.y = 2.40;
      tree.add(t3);
      return tree;
    };
    outdoorGroup.add(createPineTree(-12.0, -0.4, -2.2, 0.60));
    outdoorGroup.add(createPineTree(-13.0, -0.4, -3.2, 0.68));
    outdoorGroup.add(createPineTree(-11.0, -0.4, -4.2, 0.58));
    outdoorGroup.add(createPineTree(-14.0, -0.4, -1.6, 0.52));
    scene.add(outdoorGroup);

    // 5b. Volumetric Morning Sunbeam Shafts Streaming Through Window
    const sunbeamGroup = new THREE.Group();
    sunbeamGroup.position.set(-2.8, 1.75, -0.80);
    sunbeamGroup.rotation.z = -0.42; // Diagonally pouring down into bedroom
    sunbeamGroup.rotation.y = 0.24;

    const sunbeamMat = new THREE.MeshBasicMaterial({
      color: 0xfff0b8,
      transparent: true,
      opacity: 0.16,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      side: THREE.DoubleSide,
    });

    for (let i = 0; i < 3; i++) {
      const beam = new THREE.Mesh(new THREE.PlaneGeometry(0.48, 4.4), sunbeamMat);
      beam.position.set(0.12 * i, 0, (i - 1) * 0.42);
      beam.rotation.x = Math.PI / 2;
      sunbeamGroup.add(beam);
    }
    scene.add(sunbeamGroup);

    // 6. Real House Bed with Crisp Linen Bed-Sheet
    const bedGroup = new THREE.Group();
    bedGroup.position.set(0.2, 0, -0.85);

    const bedFrame = new THREE.Mesh(new THREE.BoxGeometry(1.54, 0.28, 2.66), darkOakTrimMat);
    bedFrame.position.set(0, 0.14, 0);
    bedGroup.add(bedFrame);

    const legGeo = new THREE.BoxGeometry(0.12, 0.28, 0.12);
    for (const [lx, lz] of [[-0.70, -1.26], [0.70, -1.26], [-0.70, 1.26], [0.70, 1.26]]) {
      const leg = new THREE.Mesh(legGeo, darkOakTrimMat);
      leg.position.set(lx, 0.14, lz);
      bedGroup.add(leg);
    }

    const bedSheetTex = createBedSheetTexture();
    bedSheetTex.repeat.set(3, 4);
    const bedSheetMat = new THREE.MeshToonMaterial({ map: bedSheetTex });
    const mattress = new THREE.Mesh(new THREE.BoxGeometry(1.46, 0.38, 2.58), bedSheetMat);
    mattress.position.set(0, 0.40, 0);
    bedGroup.add(mattress);

    const headboard = new THREE.Mesh(new THREE.BoxGeometry(1.56, 1.05, 0.12), darkOakTrimMat);
    headboard.position.set(0, 0.55, -1.33);
    bedGroup.add(headboard);

    const pillow = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.18, 0.60), whiteWoolMat);
    pillow.position.set(0, 0.63, -0.90);
    bedGroup.add(pillow);
    scene.add(bedGroup);

    // 7. Nightstand with 05:00 AM Digital Alarm Clock & Face-Down Phone
    // Positioned cleanly beside bed so both Alex and the nightstand are framed side-by-side
    const nightstand = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.7, 0.8), darkOakTrimMat);
    nightstand.position.set(1.50, 0.35, -1.05);
    scene.add(nightstand);

    const drawerFront = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.26, 0.04), oakWallMat);
    drawerFront.position.set(1.50, 0.45, -0.63);
    scene.add(drawerFront);

    const drawerKnob = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.05, 0.05), new THREE.MeshToonMaterial({ color: 0xd4af37 }));
    drawerKnob.position.set(1.50, 0.45, -0.60);
    scene.add(drawerKnob);

    // 05:00 AM Glowing Clock
    const clockTexOn = createDigitalClockTexture("05:00", true);
    const clockTexOff = createDigitalClockTexture("05:00", false);
    const clockFaceMat = new THREE.MeshBasicMaterial({ map: clockTexOn });
    const clockCaseMat = new THREE.MeshBasicMaterial({ color: 0x111115 });
    const clockMesh = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.22, 0.2), [
      clockCaseMat, clockCaseMat, clockCaseMat, clockCaseMat, clockFaceMat, clockCaseMat
    ]);
    clockMesh.position.set(1.50, 0.82, -1.05);
    clockMesh.rotation.y = -0.92; // Angled cleanly towards the window wall camera

    // Red Glowing Snooze Button on top
    const buttonBezel = new THREE.Mesh(
      new THREE.BoxGeometry(0.18, 0.02, 0.08),
      new THREE.MeshBasicMaterial({ color: 0x220509 })
    );
    buttonBezel.position.set(0, 0.115, 0);
    clockMesh.add(buttonBezel);

    const buttonTop = new THREE.Mesh(
      new THREE.BoxGeometry(0.15, 0.03, 0.06),
      new THREE.MeshBasicMaterial({ color: 0xff1a40 })
    );
    buttonTop.position.set(0, 0.128, 0);
    clockMesh.add(buttonTop);

    const buttonGlow = new THREE.PointLight(0xff1a40, 1.2, 0.5);
    buttonGlow.position.set(0, 0.16, 0);
    clockMesh.add(buttonGlow);
    scene.add(clockMesh);

    const clockLight = new THREE.PointLight(0xff1a40, 2.0, 2.6);
    clockLight.position.set(1.50, 0.9, -0.85);
    scene.add(clockLight);

    // Smartphone TURNED FACE-DOWN on the nightstand table
    const phoneGroup = new THREE.Group();
    phoneGroup.position.set(1.30, 0.708, -0.82);
    phoneGroup.rotation.y = 0.35; // Casually angled

    // Phone body (matte obsidian aluminum back facing UP)
    const phoneBody = new THREE.Mesh(
      new THREE.BoxGeometry(0.16, 0.012, 0.30),
      new THREE.MeshToonMaterial({ color: 0x16181d })
    );
    phoneGroup.add(phoneBody);

    // Screen face is turned DOWN against the table
    const phoneScreenTex = createPhoneScreenTexture();
    const phoneScreenMat = new THREE.MeshBasicMaterial({ map: phoneScreenTex });
    const phoneScreen = new THREE.Mesh(
      new THREE.PlaneGeometry(0.145, 0.285),
      phoneScreenMat
    );
    phoneScreen.rotation.x = Math.PI / 2; // Screen facing down
    phoneScreen.position.y = -0.007;
    phoneGroup.add(phoneScreen);

    // Raised Camera Island on the back facing UP towards the ceiling
    const cameraBump = new THREE.Mesh(
      new THREE.BoxGeometry(0.045, 0.008, 0.045),
      new THREE.MeshBasicMaterial({ color: 0x0c0e12 })
    );
    cameraBump.position.set(-0.045, 0.008, -0.11);
    phoneGroup.add(cameraBump);
    scene.add(phoneGroup);

    // 8. 5:00 AM Morning Sunlight & Ambient Light
    const dawnSun = new THREE.DirectionalLight(0xffdf99, 3.0);
    dawnSun.position.set(-5.5, 4.0, -0.8);
    scene.add(dawnSun);

    scene.add(new THREE.AmbientLight(0x283446, 1.15));

    // 9. Character sitting up in bed
    character.root.position.set(0.2, 0, -0.35);

    customUpdate = (t) => {
      // Alex wakes up smoothly as voice speaks "You will wake up at dawn" (between t = 0.3s and 1.8s)
      const progress = Math.max(0, Math.min(1, (t - 0.3) / 1.5));
      character.setWakingUp(t, progress);
      const blinkState = Math.floor(t * 1.8) % 2 === 0;
      clockFaceMat.map = blinkState ? clockTexOn : clockTexOff;
      clockFaceMat.needsUpdate = true;
    };
  }

  // =========================================================================
  // SCENE 2: THE SUNRISE RUN (Shot 2)
  // =========================================================================
  else if (shotId === 2) {
    scene.background = new THREE.Color(0xffcba4); // Warm golden sunrise sky

    // Expansive Minecraft multi-face Grass Block park terrain
    const ground = new THREE.Mesh(new THREE.BoxGeometry(32, 0.8, 32), grassBlockMats);
    ground.position.y = -0.4;
    scene.add(ground);

    // =========================================================================
    // GRAVEL RUNNING PATH WITH A RIGHT-HAND TURN AHEAD
    // Straight path from Z = -10 to 0, sweeping curve into rightward path along +X
    // Raised to Y = 0.08 with solid skirts dropping into ground (zero z-fighting)
    // =========================================================================
    const pathMat = new THREE.MeshToonMaterial({
      map: createParkGravelPathTexture(),
    });
    
    // 1. Straight approach path (along Z axis, from Z = -10.0 to Z = 0.0, width 2.4, height 0.08)
    const straightPath1 = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.28, 10.0), pathMat);
    straightPath1.position.set(0, -0.06, -5.0);
    scene.add(straightPath1);

    // 2. Mathematically Continuous 3D Curved Road Ribbon (Center: [3.0, 0.0], Inner R: 1.8, Outer R: 4.2)
    // Seamlessly connects straight approach at Z = 0.0 with exit path at X = 3.0, Z = 3.0
    const curveSegments = 32;
    const curveGroup = new THREE.Group();

    // Top road surface (height 0.08)
    const topGeom = new THREE.BufferGeometry();
    const cPositions: number[] = [];
    const cUvs: number[] = [];
    const cIndices: number[] = [];

    for (let i = 0; i <= curveSegments; i++) {
      const frac = i / curveSegments;
      const ang = Math.PI - frac * (Math.PI / 2);
      const cosA = Math.cos(ang);
      const sinA = Math.sin(ang);

      // Inner edge vertex (R = 1.8)
      const xIn = 3.0 + 1.8 * cosA;
      const zIn = 1.8 * sinA;
      cPositions.push(xIn, 0.08, zIn);
      cUvs.push(0, frac * 5);

      // Outer edge vertex (R = 4.2)
      const xOut = 3.0 + 4.2 * cosA;
      const zOut = 4.2 * sinA;
      cPositions.push(xOut, 0.08, zOut);
      cUvs.push(1, frac * 5);

      if (i < curveSegments) {
        const base = i * 2;
        cIndices.push(base, base + 1, base + 2);
        cIndices.push(base + 1, base + 3, base + 2);
      }
    }
    topGeom.setAttribute("position", new THREE.Float32BufferAttribute(cPositions, 3));
    topGeom.setAttribute("uv", new THREE.Float32BufferAttribute(cUvs, 2));
    topGeom.setIndex(cIndices);
    topGeom.computeVertexNormals();
    curveGroup.add(new THREE.Mesh(topGeom, pathMat));

    // Outer side skirt extending down to ground (Y = -0.20)
    const oSkirtGeom = new THREE.BufferGeometry();
    const oPos: number[] = [];
    const oIndices: number[] = [];
    for (let i = 0; i <= curveSegments; i++) {
      const frac = i / curveSegments;
      const ang = Math.PI - frac * (Math.PI / 2);
      const x = 3.0 + 4.2 * Math.cos(ang);
      const z = 4.2 * Math.sin(ang);
      oPos.push(x, 0.08, z);
      oPos.push(x, -0.20, z);
      if (i < curveSegments) {
        const b = i * 2;
        oIndices.push(b, b + 2, b + 1);
        oIndices.push(b + 1, b + 2, b + 3);
      }
    }
    oSkirtGeom.setAttribute("position", new THREE.Float32BufferAttribute(oPos, 3));
    oSkirtGeom.setIndex(oIndices);
    oSkirtGeom.computeVertexNormals();
    curveGroup.add(new THREE.Mesh(oSkirtGeom, pathMat));

    // Inner side skirt extending down to ground
    const iSkirtGeom = new THREE.BufferGeometry();
    const iPos: number[] = [];
    const iIndices: number[] = [];
    for (let i = 0; i <= curveSegments; i++) {
      const frac = i / curveSegments;
      const ang = Math.PI - frac * (Math.PI / 2);
      const x = 3.0 + 1.8 * Math.cos(ang);
      const z = 1.8 * Math.sin(ang);
      iPos.push(x, 0.08, z);
      iPos.push(x, -0.20, z);
      if (i < curveSegments) {
        const b = i * 2;
        iIndices.push(b, b + 1, b + 2);
        iIndices.push(b + 1, b + 3, b + 2);
      }
    }
    iSkirtGeom.setAttribute("position", new THREE.Float32BufferAttribute(iPos, 3));
    iSkirtGeom.setIndex(iIndices);
    iSkirtGeom.computeVertexNormals();
    curveGroup.add(new THREE.Mesh(iSkirtGeom, pathMat));

    scene.add(curveGroup);

    // 3. Exit Path after the turn (heading towards +X, from X = 3.0 to X = 15.0 at Z = 3.0, width 2.4, height 0.08)
    const straightPath2 = new THREE.Mesh(new THREE.BoxGeometry(12.0, 0.28, 2.4), pathMat);
    straightPath2.position.set(9.0, -0.06, 3.0);
    scene.add(straightPath2);

    // Low wooden boundary blocks / rustic path curb
    const borderMat = new THREE.MeshToonMaterial({ map: createMinecraftOakLogSideTexture() });
    for (let bz = -9; bz <= -0.5; bz += 1.5) {
      const bL = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.22, 1.3), borderMat);
      bL.position.set(-1.35, 0.11, bz);
      scene.add(bL);
      const bR = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.22, 1.3), borderMat);
      bR.position.set(1.35, 0.11, bz);
      scene.add(bR);
    }
    // Rustic outer curb posts framing the turn
    for (let i = 0; i <= 6; i++) {
      const frac = i / 6;
      const ang = Math.PI - frac * (Math.PI / 2);
      const post = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.32, 0.3), borderMat);
      post.position.set(3.0 + 4.45 * Math.cos(ang), 0.16, 4.45 * Math.sin(ang));
      scene.add(post);
    }
    // Exit path curbs
    for (let bx = 3.5; bx <= 11.5; bx += 1.5) {
      const bIn = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.22, 0.25), borderMat);
      bIn.position.set(bx, 0.11, 1.65);
      scene.add(bIn);
      const bOut = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.22, 0.25), borderMat);
      bOut.position.set(bx, 0.11, 4.35);
      scene.add(bOut);
    }

    // =========================================================================
    // MINECRAFT TREES & PARK ENVIRONMENT
    // Trees along approach, framing the turn, and down the exit path
    // =========================================================================
    const addParkTree = (x: number, z: number, scale: number = 1.0) => {
      const tree = new THREE.Group();
      tree.position.set(x, 0, z);
      tree.scale.set(scale, scale, scale);

      const trunk = new THREE.Mesh(new THREE.BoxGeometry(0.5, 3.0, 0.5), oakLogMats);
      trunk.position.y = 1.5;
      tree.add(trunk);

      const leaves1 = new THREE.Mesh(new THREE.BoxGeometry(2.0, 1.6, 2.0), leavesMat);
      leaves1.position.y = 3.2;
      tree.add(leaves1);

      const leaves2 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), leavesMat);
      leaves2.position.y = 4.2;
      tree.add(leaves2);

      scene.add(tree);
    };

    // Trees on left of straight approach path
    addParkTree(-3.5, -7.0, 1.05);
    addParkTree(-3.8, -3.5, 0.95);
    addParkTree(-3.5, 0.0, 1.10);

    // Trees on right of straight approach path
    addParkTree(3.5, -6.0, 1.0);
    addParkTree(3.6, -2.5, 0.9);

    // Trees along outside of the turn (framing the bend)
    addParkTree(-3.0, 3.5, 1.15);
    addParkTree(-0.5, 5.0, 1.05);
    addParkTree(2.5, 5.8, 1.10);
    addParkTree(5.5, 5.5, 0.95);
    addParkTree(9.0, 5.2, 1.0);

    // Trees along inside of the turn & exit path
    addParkTree(2.2, -1.2, 0.85);
    addParkTree(6.5, 0.5, 1.05);

    // Glowing Morning Sunrise
    const sun = new THREE.Mesh(
      new THREE.PlaneGeometry(2.6, 2.6),
      new THREE.MeshBasicMaterial({ color: 0xffea88 })
    );
    sun.position.set(10.0, 4.2, 3.0);
    sun.rotation.y = -Math.PI / 2;
    scene.add(sun);

    const sunLight = new THREE.DirectionalLight(0xffa233, 2.6);
    sunLight.position.set(12, 6, 3.0);
    scene.add(sunLight);
    scene.add(new THREE.AmbientLight(0xffecd8, 0.95));

    // =========================================================================
    // DYNAMIC RUNNING & CORNER TURNING ANIMATION
    // Alex runs along the centerline of the approach path (+Z), sweeps smoothly
    // through the turn, banks biomechanically into the bend, and sprints
    // straight down the exit path (+X) as the clip finishes.
    // The low-angle follow camera is locked directly behind his back at all frames!
    // =========================================================================
    customUpdate = (t, camera) => {
      character.setRunning(t);
      character.root.rotation.order = "YXZ";

      // Running phase starts at t ~ 2.25s and lasts until t ~ 5.15s (Clip 2 duration)
      // Total running duration = 2.90s
      const runProg = Math.max(0, Math.min(1, (t - 2.25) / 2.90));

      let px = 0;
      let pz = 0;
      let heading = 0;
      let bankLean = 0;

      if (runProg < 0.42) {
        // Phase A: Straight sprint towards the turn entrance (frames ~68 to 105)
        const subP = runProg / 0.42;
        pz = -4.5 + subP * 4.5; // from Z = -4.5 to 0.0 along X = 0
        px = 0;
        heading = 0;
        bankLean = 0;
        character.root.position.set(px, 0.08, pz);
        character.root.rotation.set(0.18, 0, 0); // facing +Z, running forward lean
      } else if (runProg < 0.82) {
        // Phase B: Sweeping smoothly through the curved turn (frames ~105 to 138)
        const turnP = (runProg - 0.42) / 0.40;
        const theta = turnP * (Math.PI / 2); // 0 to 90 degrees turn
        px = 3.0 * (1 - Math.cos(theta)); // from X = 0.0 to 3.0
        pz = 3.0 * Math.sin(theta); // from Z = 0.0 to 3.0
        heading = theta; // turn smoothly towards +X
        bankLean = -0.14 * Math.sin(turnP * Math.PI); // biomechanical bank lean into corner

        character.root.position.set(px, 0.08, pz);
        character.root.rotation.set(0.18, heading, bankLean);
      } else {
        // Phase C: Exits turn and sprints straight along +X (frames ~138 to 154)
        const exitP = (runProg - 0.82) / 0.18;
        px = 3.0 + exitP * 3.2; // sprints from X = 3.0 to 6.2
        pz = 3.0;
        heading = Math.PI / 2;
        bankLean = 0;
        character.root.position.set(px, 0.08, pz);
        character.root.rotation.set(0.18, heading, 0); // facing +X down the path
      }

      // Dynamic low-angle follow camera: locked directly behind Alex's back
      if (camera) {
        const followDist = 2.8;
        const camX = px - followDist * Math.sin(heading);
        const camY = 0.50; // low camera height looking up
        const camZ = pz - followDist * Math.cos(heading);

        const tarX = px + 0.6 * Math.sin(heading);
        const tarY = 1.05; // looking up at shoulders / head
        const tarZ = pz + 0.6 * Math.cos(heading);

        camera.position.set(camX, camY, camZ);
        camera.lookAt(tarX, tarY, tarZ);
        camera.updateProjectionMatrix();
      }
    };
  }

  // =========================================================================
  // SCENE 3 & 4: THE EXECUTIVE HOME OFFICE (Shots 3, 4, 18)
  // Perfectly matches the house architecture:
  // - Warm plaster walls with dark oak baseboards
  // - Hardwood spruce floor
  // - Left side wall with open doorway and dark oak casing (camera enters here)
  // - Back wall: framed picture & floating shelf with 3D Golden Trophy
  // - Right wall: improved 3D executive cupboard & multi-tier shelving rack
  //   with books, bookends, succulent plant, and storage cabinet
  // - Executive oak desk with warm task lamp, sleek open laptop with code editor,
  //   lined notepad with pen, empty ceramic coffee cup, and meal prep box
  // - Alex seated in ergonomic chair typing diligently on the laptop keys
  // =========================================================================
  else if (shotId === 3 || shotId === 4) {
    scene.background = new THREE.Color(0x0c1017);

    // 1. Hardwood Spruce Floor
    const floor = new THREE.Mesh(new THREE.BoxGeometry(7.2, 0.2, 7.2), floorMat);
    floor.position.set(0, -0.1, 0);
    scene.add(floor);

    // Outside Hallway Floor (visible through the open doorway)
    const hallwayFloor = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.2, 3.2), floorMat);
    hallwayFloor.position.set(-4.0, -0.1, 0.95);
    scene.add(hallwayFloor);

    // 2. Real House Drywall / Plaster Walls (matches bedroom)
    const plasterTex = createPlasterWallTexture();
    plasterTex.repeat.set(4, 3);
    const plasterWallMat = new THREE.MeshToonMaterial({ map: plasterTex });

    // 2a. Back Wall (Behind Alex)
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(7.2, 4.0, 0.25), plasterWallMat);
    backWall.position.set(0, 1.9, -2.85);
    scene.add(backWall);

    const baseboardBack = new THREE.Mesh(new THREE.BoxGeometry(7.2, 0.18, 0.08), darkOakTrimMat);
    baseboardBack.position.set(0, 0.09, -2.71);
    scene.add(baseboardBack);

    // 2b. Right Wall (Holding the executive cupboard)
    const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.25, 4.0, 7.2), plasterWallMat);
    rightWall.position.set(2.85, 1.9, 0);
    scene.add(rightWall);

    const baseboardRight = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 7.2), darkOakTrimMat);
    baseboardRight.position.set(2.71, 0.09, 0);
    scene.add(baseboardRight);

    // 2c. Front Wall (Closes room behind camera)
    const frontWall = new THREE.Mesh(new THREE.BoxGeometry(7.2, 4.0, 0.25), plasterWallMat);
    frontWall.position.set(0, 1.9, 2.85);
    scene.add(frontWall);

    // 2d. Left Wall with True Open Doorway Aperture (Door opening from Z = 0.35 to 1.55)
    // Left Wall Back Section (from Z = -2.85 to 0.35, length 3.2m)
    const leftWallBack = new THREE.Mesh(new THREE.BoxGeometry(0.25, 4.0, 3.2), plasterWallMat);
    leftWallBack.position.set(-2.85, 1.9, -1.25);
    scene.add(leftWallBack);

    const baseboardLeftBack = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 3.2), darkOakTrimMat);
    baseboardLeftBack.position.set(-2.71, 0.09, -1.25);
    scene.add(baseboardLeftBack);

    // Left Wall Front Section (from Z = 1.55 to 2.85, length 1.3m)
    const leftWallFront = new THREE.Mesh(new THREE.BoxGeometry(0.25, 4.0, 1.3), plasterWallMat);
    leftWallFront.position.set(-2.85, 1.9, 2.2);
    scene.add(leftWallFront);

    const baseboardLeftFront = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.18, 1.3), darkOakTrimMat);
    baseboardLeftFront.position.set(-2.71, 0.09, 2.2);
    scene.add(baseboardLeftFront);

    // Left Wall Top Header above doorway (Y = 2.4 to 4.0, length 1.2m)
    const leftWallTop = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.6, 1.2), plasterWallMat);
    leftWallTop.position.set(-2.85, 3.2, 0.95);
    scene.add(leftWallTop);

    // Doorway Frame / Casing (Dark Oak)
    const doorJambL = new THREE.Mesh(new THREE.BoxGeometry(0.30, 2.42, 0.08), darkOakTrimMat);
    doorJambL.position.set(-2.85, 1.2, 0.35);
    scene.add(doorJambL);

    const doorJambR = new THREE.Mesh(new THREE.BoxGeometry(0.30, 2.42, 0.08), darkOakTrimMat);
    doorJambR.position.set(-2.85, 1.2, 1.55);
    scene.add(doorJambR);

    const doorHeader = new THREE.Mesh(new THREE.BoxGeometry(0.30, 0.08, 1.28), darkOakTrimMat);
    doorHeader.position.set(-2.85, 2.42, 0.95);
    scene.add(doorHeader);

    // Open Door Panel (Swung open into room against the left wall at an angle)
    const openDoorGroup = new THREE.Group();
    openDoorGroup.position.set(-2.75, 0, 0.38);
    openDoorGroup.rotation.y = -1.25; // swung open into room
    const doorSlab = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.36, 1.05), darkOakTrimMat);
    doorSlab.position.set(0, 1.18, 0.525);
    openDoorGroup.add(doorSlab);
    // Brass door handle
    const handleMat = new THREE.MeshToonMaterial({ color: 0xd4af37 });
    const doorHandle = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.04, 0.14), handleMat);
    doorHandle.position.set(0.04, 1.05, 0.95);
    openDoorGroup.add(doorHandle);
    scene.add(openDoorGroup);

    // Hallway Wall opposite doorway
    const hallwayBackWall = new THREE.Mesh(new THREE.BoxGeometry(0.25, 4.0, 3.6), plasterWallMat);
    hallwayBackWall.position.set(-4.85, 1.9, 0.95);
    scene.add(hallwayBackWall);

    // Warm Hallway Sconce Light
    const hallwayLight = new THREE.PointLight(0xffdfa0, 1.4, 4.0);
    hallwayLight.position.set(-4.6, 2.1, 0.95);
    scene.add(hallwayLight);

    // 3. Wall Behind Alex: Framed Picture & Floating Shelf with 3D Golden Trophy
    // 3a. Framed Picture (Hanging on back wall at X = -0.85, Y = 2.15, Z = -2.71, framed cleanly on left)
    const pictureGroup = new THREE.Group();
    pictureGroup.position.set(-0.85, 2.15, -2.71);
    const artTex = createFramedArtTexture();
    const artCanvasMat = new THREE.MeshToonMaterial({ map: artTex });
    const artFrameMat = new THREE.MeshToonMaterial({ color: 0x24160e });
    const pictureFrame = new THREE.Mesh(new THREE.BoxGeometry(1.25, 0.85, 0.05), artFrameMat);
    pictureGroup.add(pictureFrame);
    const pictureCanvas = new THREE.Mesh(new THREE.BoxGeometry(1.15, 0.75, 0.02), artCanvasMat);
    pictureCanvas.position.set(0, 0, 0.02);
    pictureGroup.add(pictureCanvas);
    // Subtle gallery picture spotlight
    const pictureSpot = new THREE.PointLight(0xfff0dd, 1.1, 2.8);
    pictureSpot.position.set(0, 0.2, 0.35);
    pictureGroup.add(pictureSpot);
    scene.add(pictureGroup);

    // 3b. Floating Shelf with 3D Golden Trophy (Mounted on back wall at X = 0.35, Y = 2.05, Z = -2.68, fully unoccluded between picture and Alex)
    const shelfGroup = new THREE.Group();
    shelfGroup.position.set(0.35, 2.05, -2.68);
    const shelfBoard = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.06, 0.32), darkOakTrimMat);
    shelfGroup.add(shelfBoard);
    // Brass support brackets
    const bracketMat = new THREE.MeshToonMaterial({ color: 0xb48c36 });
    for (const bx of [-0.30, 0.30]) {
      const br = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.16, 0.26), bracketMat);
      br.position.set(bx, -0.08, -0.01);
      shelfGroup.add(br);
    }

    // 3c. Gleaming 3D Golden Trophy (Mahogany base with plaque, fluted gold stem, gold cup & twin handles)
    const trophyGroup = new THREE.Group();
    trophyGroup.position.set(0, 0.03, 0);

    // Dark polished mahogany trophy base
    const trophyBase = new THREE.Mesh(
      new THREE.CylinderGeometry(0.12, 0.14, 0.08, 14),
      new THREE.MeshToonMaterial({ color: 0x1a0f0a })
    );
    trophyBase.position.y = 0.04;
    trophyGroup.add(trophyBase);

    // Gold brass plaque with engraved achievement
    const trophyPlaque = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.035, 0.01), handleMat);
    trophyPlaque.position.set(0, 0.04, 0.135);
    trophyGroup.add(trophyPlaque);

    // Fluted Gold Stem / Pedestal
    const goldMat = new THREE.MeshToonMaterial({ color: 0xffd700 });
    const trophyStem = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.075, 0.13, 14), goldMat);
    trophyStem.position.y = 0.145;
    trophyGroup.add(trophyStem);

    // Gold Chalice / Cup Body
    const trophyCup = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.065, 0.24, 16), goldMat);
    trophyCup.position.y = 0.32;
    trophyGroup.add(trophyCup);

    // Gold Handles (Twin arched handles)
    const handleGeo = new THREE.TorusGeometry(0.08, 0.018, 8, 16, Math.PI);
    const handleL = new THREE.Mesh(handleGeo, goldMat);
    handleL.rotation.z = Math.PI / 2;
    handleL.position.set(-0.17, 0.33, 0);
    trophyGroup.add(handleL);

    const handleR = new THREE.Mesh(handleGeo, goldMat);
    handleR.rotation.z = -Math.PI / 2;
    handleR.position.set(0.17, 0.33, 0);
    trophyGroup.add(handleR);

    // Dedicated Warm Golden Trophy Accent Light
    const trophyGlow = new THREE.PointLight(0xffd700, 2.4, 2.6);
    trophyGlow.position.set(0, 0.40, 0.28);
    trophyGroup.add(trophyGlow);

    shelfGroup.add(trophyGroup);
    scene.add(shelfGroup);

    // 4. Improved 3D Executive Side Cupboard & Shelving Rack (along Right Wall)
    const cupboardGroup = new THREE.Group();
    cupboardGroup.position.set(2.45, 0, -0.95);
    cupboardGroup.rotation.y = -Math.PI / 2; // facing into room towards desk

    const rackW = 1.70;
    const rackH = 2.85;
    const rackD = 0.44;

    const cupboardBackMat = new THREE.MeshToonMaterial({ color: 0x22150b });
    const rackBack = new THREE.Mesh(new THREE.BoxGeometry(rackW, rackH, 0.04), cupboardBackMat);
    rackBack.position.set(0, rackH / 2, -rackD / 2 + 0.02);
    cupboardGroup.add(rackBack);

    const rackSideL = new THREE.Mesh(new THREE.BoxGeometry(0.05, rackH, rackD), darkOakTrimMat);
    rackSideL.position.set(-rackW / 2 + 0.025, rackH / 2, 0);
    cupboardGroup.add(rackSideL);

    const rackSideR = new THREE.Mesh(new THREE.BoxGeometry(0.05, rackH, rackD), darkOakTrimMat);
    rackSideR.position.set(rackW / 2 - 0.025, rackH / 2, 0);
    cupboardGroup.add(rackSideR);

    // Molded Crown Top
    const rackTop = new THREE.Mesh(new THREE.BoxGeometry(rackW + 0.10, 0.09, rackD + 0.08), darkOakTrimMat);
    rackTop.position.set(0, rackH, 0);
    cupboardGroup.add(rackTop);

    // Lower Storage Cabinet Divider Shelf (Height 0.90m)
    const cabinetShelf = new THREE.Mesh(new THREE.BoxGeometry(rackW - 0.08, 0.05, rackD - 0.04), darkOakTrimMat);
    cabinetShelf.position.set(0, 0.90, 0);
    cupboardGroup.add(cabinetShelf);

    // Cabinet Doors (2 doors with raised bevels and brass knobs)
    const doorW = (rackW - 0.12) / 2;
    const doorMat = new THREE.MeshToonMaterial({ color: 0x331f0e });
    for (let d = 0; d < 2; d++) {
      const cDoor = new THREE.Mesh(new THREE.BoxGeometry(doorW, 0.85, 0.03), doorMat);
      cDoor.position.set((d === 0 ? -1 : 1) * (doorW / 2 + 0.01), 0.44, rackD / 2 - 0.02);
      cupboardGroup.add(cDoor);

      // Recessed inner door panel
      const innerPanel = new THREE.Mesh(new THREE.BoxGeometry(doorW - 0.08, 0.72, 0.01), darkOakTrimMat);
      innerPanel.position.set((d === 0 ? -1 : 1) * (doorW / 2 + 0.01), 0.44, rackD / 2 - 0.005);
      cupboardGroup.add(innerPanel);

      // Polished brass door knob
      const knob = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.035, 0.04), handleMat);
      knob.position.set((d === 0 ? -1 : 1) * 0.05, 0.46, rackD / 2 + 0.015);
      cupboardGroup.add(knob);
    }

    // Upper Display Shelves & Objects
    // Shelf 1 (Y = 1.48) - Colorful 3D Books & Bookend
    const shelf1 = new THREE.Mesh(new THREE.BoxGeometry(rackW - 0.08, 0.04, rackD - 0.04), darkOakTrimMat);
    shelf1.position.set(0, 1.48, 0);
    cupboardGroup.add(shelf1);

    const bookColors = [0x881337, 0x1e3a8a, 0x14532d, 0x78350f, 0x1e293b, 0x9a3412, 0x312e81, 0x065f46];
    let bookX = -rackW / 2 + 0.15;
    for (let b = 0; b < 9; b++) {
      const bW = 0.048 + (b % 3) * 0.014;
      const bH = 0.32 + (b % 4) * 0.025;
      const bD = 0.28;
      const bookMesh = new THREE.Mesh(
        new THREE.BoxGeometry(bW, bH, bD),
        new THREE.MeshToonMaterial({ color: bookColors[b % bookColors.length] })
      );
      bookMesh.position.set(bookX + bW / 2, 1.50 + bH / 2, 0);
      cupboardGroup.add(bookMesh);
      bookX += bW + 0.01;
    }
    // Wooden bookend
    const bookend = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.28, 0.24), darkOakTrimMat);
    bookend.position.set(bookX + 0.03, 1.64, 0);
    cupboardGroup.add(bookend);

    // Leaning book against bookend
    const leaningBook = new THREE.Mesh(
      new THREE.BoxGeometry(0.05, 0.33, 0.27),
      new THREE.MeshToonMaterial({ color: 0xb45309 })
    );
    leaningBook.position.set(bookX + 0.09, 1.64, 0);
    leaningBook.rotation.z = 0.18;
    cupboardGroup.add(leaningBook);

    // Shelf 2 (Y = 2.08) - Succulent Plant, Minimalist Clock, Slate Storage Box
    const shelf2 = new THREE.Mesh(new THREE.BoxGeometry(rackW - 0.08, 0.04, rackD - 0.04), darkOakTrimMat);
    shelf2.position.set(0, 2.08, 0);
    cupboardGroup.add(shelf2);

    // Potted Succulent Plant on Shelf 2
    const sPot = new THREE.Mesh(
      new THREE.CylinderGeometry(0.11, 0.08, 0.15, 12),
      new THREE.MeshToonMaterial({ color: 0xf5f3ee })
    );
    sPot.position.set(-0.45, 2.18, 0);
    cupboardGroup.add(sPot);
    const sPlant = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.20, 0.22), leavesMat);
    sPlant.position.set(-0.45, 2.33, 0);
    cupboardGroup.add(sPlant);

    // Minimalist Studio Desk Clock
    const miniClock = new THREE.Mesh(
      new THREE.CylinderGeometry(0.08, 0.08, 0.04, 16),
      new THREE.MeshToonMaterial({ color: 0xd4af37 })
    );
    miniClock.rotation.x = Math.PI / 2;
    miniClock.position.set(0.0, 2.18, 0.05);
    cupboardGroup.add(miniClock);

    // Slate Blue Storage Box on Shelf 2
    const dBox = new THREE.Mesh(
      new THREE.BoxGeometry(0.44, 0.26, 0.32),
      new THREE.MeshToonMaterial({ color: 0x334155 })
    );
    dBox.position.set(0.42, 2.23, 0);
    cupboardGroup.add(dBox);

    // Warm Cupboard Interior Ambient Downlight
    const cupboardLight = new THREE.PointLight(0xffdfb0, 1.2, 2.8);
    cupboardLight.position.set(0, 2.50, 0.15);
    cupboardGroup.add(cupboardLight);

    scene.add(cupboardGroup);

    // 5. Large Executive Oak Desk (Centered in front of Alex at Z = -0.75)
    const deskGroup = new THREE.Group();
    deskGroup.position.set(0, 0, -0.75);

    const deskTop = new THREE.Mesh(new THREE.BoxGeometry(2.30, 0.09, 1.15), darkOakTrimMat);
    deskTop.position.set(0, 0.88, 0);
    deskGroup.add(deskTop);

    // 4 Sturdy Square Desk Legs with Brass Leveling Feet
    const legGeo = new THREE.BoxGeometry(0.10, 0.88, 0.10);
    for (const [lx, lz] of [[-1.05, -0.48], [1.05, -0.48], [-1.05, 0.48], [1.05, 0.48]]) {
      const leg = new THREE.Mesh(legGeo, darkOakTrimMat);
      leg.position.set(lx, 0.44, lz);
      deskGroup.add(leg);
      const foot = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.04, 0.11), handleMat);
      foot.position.set(lx, 0.02, lz);
      deskGroup.add(foot);
    }
    // Modesty Panel
    const modestyPanel = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.45, 0.03), darkOakTrimMat);
    modestyPanel.position.set(0, 0.62, 0.45);
    deskGroup.add(modestyPanel);
    scene.add(deskGroup);

    // 6. Desk Task Lamp with Warm Amber Light (Far back-left corner of desk, pushed back to Z = -1.25)
    // Tilted forward over the desk, COMPLETELY CLEAR of Alex's face and laptop in camera line of sight!
    const lampGroup = new THREE.Group();
    lampGroup.position.set(-1.05, 0.925, -1.25);
    const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.10, 0.025, 14), darkOakTrimMat);
    lampGroup.add(lampBase);

    const lampArm = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.58, 0.03), darkOakTrimMat);
    lampArm.position.set(0.02, 0.28, 0.10);
    lampArm.rotation.z = -0.12; // Tilted slightly towards desk surface
    lampArm.rotation.x = 0.22; // Tilted forward towards front desk edge
    lampGroup.add(lampArm);

    const lampShade = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.16, 14), darkOakTrimMat);
    lampShade.position.set(0.04, 0.52, 0.14);
    lampShade.rotation.z = Math.PI / 5.0;
    lampShade.rotation.x = 0.35;
    lampGroup.add(lampShade);

    // Warm amber desk illumination pooling across coffee cup, notepad, and desk surface
    const lampLight = new THREE.PointLight(0xffe28a, 2.8, 3.4);
    lampLight.position.set(0.06, 0.48, 0.16);
    lampGroup.add(lampLight);
    scene.add(lampGroup);

    // 7. Sleek Modern Laptop ("give him a laptop" - centered directly in front of Alex)
    // Physical orientation: Screen faces Alex (-Z), outer metallic lid faces the camera/room (+Z)
    const laptopGroup = new THREE.Group();
    laptopGroup.position.set(0.04, 0.925, -0.96);
    laptopGroup.rotation.y = 0.08;

    // Laptop chassis / base
    const laptopBaseMat = new THREE.MeshToonMaterial({ color: 0x1f242d });
    const laptopBase = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.016, 0.35), laptopBaseMat);
    laptopGroup.add(laptopBase);

    // Trackpad (closest to Alex at -Z where wrists rest)
    const touchpad = new THREE.Mesh(
      new THREE.BoxGeometry(0.16, 0.002, 0.10),
      new THREE.MeshBasicMaterial({ color: 0x181c23 })
    );
    touchpad.position.set(0, 0.009, -0.11);
    laptopGroup.add(touchpad);

    // Keyboard keys area (centered between trackpad and hinge)
    const keyboardArea = new THREE.Mesh(
      new THREE.BoxGeometry(0.45, 0.003, 0.18),
      new THREE.MeshBasicMaterial({ color: 0x0f1217 })
    );
    keyboardArea.position.set(0, 0.009, 0.02);
    laptopGroup.add(keyboardArea);

    // Laptop Screen Lid (hinged at far side away from Alex at +Z, open tilted towards the room)
    const screenHinge = new THREE.Group();
    screenHinge.position.set(0, 0.01, 0.165); // Far edge away from Alex
    screenHinge.rotation.x = 0.28; // Open tilted backwards away from keyboard

    const lidMat = new THREE.MeshToonMaterial({ color: 0x1a1e26 });
    const lid = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.34, 0.012), lidMat);
    lid.position.set(0, 0.17, 0);
    screenHinge.add(lid);

    // Screen display with glowing IDE editor texture (FACES ALEX at -Z!)
    const screenTex = createLaptopScreenTexture();
    const screenMat = new THREE.MeshBasicMaterial({ map: screenTex });
    const screenMesh = new THREE.Mesh(new THREE.PlaneGeometry(0.49, 0.31), screenMat);
    screenMesh.position.set(0, 0.17, -0.007);
    screenMesh.rotation.y = Math.PI; // Normal points to -Z directly into Alex's eyes!
    screenHinge.add(screenMesh);

    // Sleek executive tech logo badge on outer lid (FACES ROOM / CAMERA at +Z!)
    const logoBadge = new THREE.Mesh(
      new THREE.BoxGeometry(0.08, 0.08, 0.002),
      new THREE.MeshBasicMaterial({ color: 0x38bdf8 })
    );
    logoBadge.position.set(0, 0.17, 0.007);
    screenHinge.add(logoBadge);

    laptopGroup.add(screenHinge);

    // Soft Laptop Screen Glow onto keyboard and Alex's face
    const laptopGlow = new THREE.PointLight(0x38bdf8, 1.4, 1.8);
    laptopGlow.position.set(0, 0.20, -0.05); // Shining onto Alex and keyboard
    laptopGroup.add(laptopGlow);

    scene.add(laptopGroup);

    // 8. Empty Ceramic Coffee Cup ("an empty coffee cup" - placed prominently on desk)
    const cupGroup = new THREE.Group();
    cupGroup.position.set(-0.68, 0.925, -0.56); // Cleanly visible in front of desk lamp, beside notepad
    cupGroup.rotation.y = 0.55;

    const mugMat = new THREE.MeshToonMaterial({ color: 0xedeae2 }); // Ceramic porcelain
    const mugOuter = new THREE.Mesh(new THREE.CylinderGeometry(0.072, 0.058, 0.12, 16), mugMat);
    mugOuter.position.y = 0.06;
    cupGroup.add(mugOuter);

    // Dark empty interior cavity
    const mugInner = new THREE.Mesh(
      new THREE.CylinderGeometry(0.058, 0.048, 0.105, 16),
      new THREE.MeshBasicMaterial({ color: 0x362c24 })
    );
    mugInner.position.y = 0.068;
    cupGroup.add(mugInner);

    // Dried dark coffee ring stain at the bottom
    const coffeeStain = new THREE.Mesh(
      new THREE.CylinderGeometry(0.046, 0.046, 0.005, 14),
      new THREE.MeshBasicMaterial({ color: 0x1c1007 })
    );
    coffeeStain.position.y = 0.018;
    cupGroup.add(coffeeStain);

    // 3D Curved Mug Handle
    const mugHandle = new THREE.Mesh(
      new THREE.TorusGeometry(0.042, 0.012, 8, 16, Math.PI * 1.15),
      mugMat
    );
    mugHandle.rotation.z = Math.PI / 2;
    mugHandle.position.set(-0.072, 0.06, 0);
    cupGroup.add(mugHandle);
    scene.add(cupGroup);

    // 9. Short Note-Taking Paper & Pen ("a short note taking paper and a pen also in the table")
    const noteGroup = new THREE.Group();
    noteGroup.position.set(-0.34, 0.925, -0.46); // Cleanly in foreground between coffee cup & laptop
    noteGroup.rotation.y = -0.18;

    const noteTex = createNotePaperTexture();
    const noteMat = new THREE.MeshBasicMaterial({ map: noteTex });
    const notePad = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.008, 0.28), [
      new THREE.MeshBasicMaterial({ color: 0xede8d5 }),
      new THREE.MeshBasicMaterial({ color: 0xede8d5 }),
      noteMat,
      new THREE.MeshBasicMaterial({ color: 0xede8d5 }),
      new THREE.MeshBasicMaterial({ color: 0xede8d5 }),
      new THREE.MeshBasicMaterial({ color: 0xede8d5 }),
    ]);
    notePad.position.set(0, 0.004, 0);
    noteGroup.add(notePad);

    // Sleek Executive Pen lying across the notepad
    const penGroup = new THREE.Group();
    penGroup.position.set(0.04, 0.014, 0.02);
    penGroup.rotation.y = 0.42;
    const penBody = new THREE.Mesh(
      new THREE.CylinderGeometry(0.009, 0.009, 0.17, 10),
      new THREE.MeshToonMaterial({ color: 0x111827 })
    );
    penBody.rotation.x = Math.PI / 2;
    penGroup.add(penBody);

    const penClip = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.020, 0.065), handleMat);
    penClip.position.set(0, 0.011, -0.045);
    penGroup.add(penClip);

    const penTip = new THREE.Mesh(
      new THREE.ConeGeometry(0.009, 0.028, 10),
      new THREE.MeshToonMaterial({ color: 0xd4af37 })
    );
    penTip.rotation.x = -Math.PI / 2;
    penTip.position.set(0, 0, 0.098);
    penGroup.add(penTip);

    noteGroup.add(penGroup);
    scene.add(noteGroup);

    // 10. Clean Meal Prep Glass Box ("eat clean" - placed on right side of desk)
    const lunchBox = new THREE.Mesh(
      new THREE.BoxGeometry(0.36, 0.12, 0.26),
      new THREE.MeshBasicMaterial({ color: 0x22c55e, transparent: true, opacity: 0.85 })
    );
    lunchBox.position.set(0.70, 0.98, -0.72);
    scene.add(lunchBox);

    // 11. Ergonomic Office Chair & Alex Seated (Facing desk & laptop, back to back wall)
    const chairBase = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.08, 0.68), darkOakTrimMat);
    chairBase.position.set(0.04, 0.45, -1.38);
    scene.add(chairBase);

    const chairBack = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.78, 0.08), darkOakTrimMat);
    chairBack.position.set(0.04, 0.88, -1.68);
    scene.add(chairBack);

    // Alex seated at desk facing forward (+Z towards laptop and room)
    character.root.position.set(0.04, 0.22, -1.35);
    character.root.rotation.set(0, 0, 0);

    // Studio Lighting
    scene.add(new THREE.AmbientLight(0xfff5ea, 1.10));
    const ceilingKey = new THREE.DirectionalLight(0xffeedd, 1.35);
    ceilingKey.position.set(-2.5, 4.2, 1.8);
    scene.add(ceilingKey);

    customUpdate = (t) => {
      if (shotId === 4) {
        character.setSittingProud(t);
      } else {
        character.setTyping(t);
        // Fine-tune head angle for clip 3 so Alex's face is clearly visible and looking at laptop
        character.headGroup.rotation.set(0.12, -0.10, 0);
      }
    };
  }

  // =========================================================================
  // SCENE 5: NATURAL SUNRISE OVERLOOK (Shot 5 - Pedestal Tower Removed)
  // =========================================================================
  else if (shotId === 5) {
    scene.background = new THREE.Color(0xffb882); // Golden dawn sunrise horizon

    // 1. Lighting Setup (Dramatic Sunrise Golden Hour)
    scene.add(new THREE.AmbientLight(0xffeedd, 1.15));
    const sunriseKey = new THREE.DirectionalLight(0xffaa33, 2.5);
    sunriseKey.position.set(6, 12, -10);
    scene.add(sunriseKey);

    const skyFill = new THREE.DirectionalLight(0x88bbff, 0.65);
    skyFill.position.set(-8, 6, 8);
    scene.add(skyFill);

    // Glowing Sunrise Sun Disk on distant horizon
    const sunMat = new THREE.MeshBasicMaterial({ color: 0xffea88 });
    const sunMesh = new THREE.Mesh(new THREE.PlaneGeometry(5.4, 5.4), sunMat);
    sunMesh.position.set(0.0, 7.8, -26);
    scene.add(sunMesh);

    // 2. Base Ground Landscape
    const groundBase = new THREE.Mesh(new THREE.BoxGeometry(36.0, 1.0, 36.0), grassBlockMats);
    groundBase.position.set(0, -0.5, 0);
    scene.add(groundBase);

    // 3. Summit Peak Plateau (Elevation Y = 4.20)
    const summitPlateau = new THREE.Mesh(new THREE.BoxGeometry(6.2, 0.8, 4.4), grassBlockMats);
    summitPlateau.position.set(0, 3.8, -2.2);
    scene.add(summitPlateau);

    // 4. The Grand Mountain Staircase (12 fully visible, elevated stone steps)
    const stairMat = stoneMat;
    const stairTrimMat = new THREE.MeshToonMaterial({ color: 0x3d2714 }); // Dark spruce curb
    const totalSteps = 12;
    const stepWidth = 3.6;
    const stepDepth = 0.70;
    const stepHeight = 0.35;

    for (let i = 0; i < totalSteps; i++) {
      const stepY = (i + 1) * stepHeight;
      const stepZ = 6.4 - i * 0.65; // from Z = 6.4 down to Z = -0.75

      // Step slab
      const stepMesh = new THREE.Mesh(
        new THREE.BoxGeometry(stepWidth, stepHeight, stepDepth + 0.05),
        stairMat
      );
      stepMesh.position.set(0, stepY - stepHeight / 2, stepZ);
      scene.add(stepMesh);

      // Solid foundation support under each step so it's a solid mountain stairway
      if (i > 0) {
        const supportMesh = new THREE.Mesh(
          new THREE.BoxGeometry(stepWidth, stepY - stepHeight, stepDepth),
          dirtMat
        );
        supportMesh.position.set(0, (stepY - stepHeight) / 2, stepZ);
        scene.add(supportMesh);
      }

      // Side stair curb stones
      const curbL = new THREE.Mesh(new THREE.BoxGeometry(0.24, stepHeight + 0.12, stepDepth), stairTrimMat);
      curbL.position.set(-stepWidth / 2 - 0.12, stepY - stepHeight / 2 + 0.06, stepZ);
      scene.add(curbL);

      const curbR = new THREE.Mesh(new THREE.BoxGeometry(0.24, stepHeight + 0.12, stepDepth), stairTrimMat);
      curbR.position.set(stepWidth / 2 + 0.12, stepY - stepHeight / 2 + 0.06, stepZ);
      scene.add(curbR);
    }

    // 5. Terraced Mountain Flanks on Left and Right of Stairs
    // Left Flank Terraces
    const leftTier1 = new THREE.Mesh(new THREE.BoxGeometry(6.0, 1.2, 12.0), grassBlockMats);
    leftTier1.position.set(-5.0, 0.6, 2.0);
    scene.add(leftTier1);

    const leftTier2 = new THREE.Mesh(new THREE.BoxGeometry(5.0, 1.4, 8.0), stoneMat);
    leftTier2.position.set(-4.5, 1.9, 0.0);
    scene.add(leftTier2);

    const leftTier3 = new THREE.Mesh(new THREE.BoxGeometry(4.0, 1.2, 5.0), grassBlockMats);
    leftTier3.position.set(-4.0, 3.2, -1.5);
    scene.add(leftTier3);

    // Right Flank Terraces
    const rightTier1 = new THREE.Mesh(new THREE.BoxGeometry(6.0, 1.2, 12.0), grassBlockMats);
    rightTier1.position.set(5.0, 0.6, 2.0);
    scene.add(rightTier1);

    const rightTier2 = new THREE.Mesh(new THREE.BoxGeometry(5.0, 1.4, 8.0), stoneMat);
    rightTier2.position.set(4.5, 1.9, 0.0);
    scene.add(rightTier2);

    const rightTier3 = new THREE.Mesh(new THREE.BoxGeometry(4.0, 1.2, 5.0), grassBlockMats);
    rightTier3.position.set(4.0, 3.2, -1.5);
    scene.add(rightTier3);

    // 6. Alpine Spruce Trees on Mountain Flanks
    const treePositions = [
      [-5.5, 1.2, 3.5],
      [5.2, 1.2, 4.0],
      [-4.5, 2.6, 0.5],
      [4.6, 2.6, 0.8],
      [-4.2, 3.8, -2.5],
      [4.2, 3.8, -2.2],
      [-7.5, 0.0, 6.5],
      [7.2, 0.0, 6.8],
    ];
    treePositions.forEach(([tx, ty, tz]) => {
      const trunk = new THREE.Mesh(new THREE.BoxGeometry(0.35, 1.8, 0.35), oakLogMats);
      trunk.position.set(tx, ty + 0.9, tz);
      scene.add(trunk);

      const foliage1 = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.0, 1.6), leavesMat);
      foliage1.position.set(tx, ty + 2.0, tz);
      scene.add(foliage1);

      const foliage2 = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.9, 1.0), leavesMat);
      foliage2.position.set(tx, ty + 2.8, tz);
      scene.add(foliage2);
    });

    // 7. Summit Victory Flag (Beside Main Hero at the Peak)
    // Banner cloth mounted proudly at the top of the flagpole directly under the finial ball
    const flagGroup = new THREE.Group();
    flagGroup.position.set(-0.65, 4.20, -2.00);

    // Stone Pedestal Base
    const flagBase = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.22, 0.45), stoneMat);
    flagBase.position.set(0, 0.11, 0);
    flagGroup.add(flagBase);

    // Metallic Flagpole (Proportional 2.0m mast)
    const poleGeo = new THREE.CylinderGeometry(0.035, 0.038, 2.0, 12);
    const poleMat = new THREE.MeshToonMaterial({ color: 0xd4af37 }); // Golden bronze mast
    const poleMesh = new THREE.Mesh(poleGeo, poleMat);
    poleMesh.position.set(0, 1.10, 0);
    flagGroup.add(poleMesh);

    // Golden Spherical Finial on pole tip
    const finialMesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.09, 12, 12),
      new THREE.MeshToonMaterial({ color: 0xffd700 })
    );
    finialMesh.position.set(0, 2.12, 0);
    flagGroup.add(finialMesh);

    // Animated Fluttering Crimson & Gold Victory Banner (Mounted at the very top of the pole)
    const bannerGroup = new THREE.Group();
    bannerGroup.position.set(0, 1.74, 0); // Top of banner (1.74 + 0.36 = 2.10) directly meets finial ball

    const flagFabric = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.72, 0.04), redWoolMat);
    flagFabric.position.set(-0.60, 0, 0); // Extends left from the pole
    bannerGroup.add(flagFabric);

    const goldTrimMat = new THREE.MeshToonMaterial({ color: 0xffd700 });
    const goldTrimTop = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.06, 0.05), goldTrimMat);
    goldTrimTop.position.set(-0.60, 0.33, 0);
    bannerGroup.add(goldTrimTop);

    const goldTrimBottom = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.06, 0.05), goldTrimMat);
    goldTrimBottom.position.set(-0.60, -0.33, 0);
    bannerGroup.add(goldTrimBottom);

    flagGroup.add(bannerGroup);
    scene.add(flagGroup);

    // 8. Main Hero Character: Alex (Side by Side with the Flag at the Peak)
    character.root.position.set(0.55, 4.20, -2.00);
    character.root.rotation.set(0, 0.10, 0); // Heroic angle facing camera & sunrise

    // 9. Secondary Climbers: 8 People Far Away Down Below Near Mountain Base
    // Leaving Steps 4 through 12 completely clear so the summit feels isolated and conquered!
    
    // --- GROUP A: 4 PEOPLE ON THE GROUND AT MOUNTAIN BASE ---
    // Climber 1: Looking up in awe and intimidation at the mountain base
    const climber1 = new VoxelCharacter("Marcus");
    climber1.setShirtColor(0x334155); // Slate / charcoal
    climber1.root.position.set(-2.5, 0.0, 7.5);
    climber1.root.rotation.set(0, Math.PI - 0.20, 0);
    scene.add(climber1.root);

    // Climber 2: Sitting on ground overwhelmed / giving up
    const climber2 = new VoxelCharacter("Climber2");
    climber2.setShirtColor(0x92400e); // Rust brown
    climber2.root.position.set(2.5, 0.0, 7.3);
    climber2.root.rotation.set(0, Math.PI + 0.30, 0);
    scene.add(climber2.root);

    // Climber 3: Hesitating nervous at base of stairs looking up
    const climber3 = new VoxelCharacter("Climber3");
    climber3.setShirtColor(0x65a30d); // Olive
    climber3.root.position.set(-1.4, 0.0, 7.0);
    climber3.root.rotation.set(0, Math.PI - 0.05, 0);
    scene.add(climber3.root);

    // Climber 4: Stumbling onto the entrance threshold
    const climber4 = new VoxelCharacter("Climber4");
    climber4.setShirtColor(0x991b1b); // Brick red
    climber4.root.position.set(1.2, 0.0, 6.8);
    climber4.root.rotation.set(0, Math.PI, 0);
    scene.add(climber4.root);

    // --- GROUP B: 4 PEOPLE AT THE LOWEST INITIAL STEPS (STEPS 1, 2, 3) ---
    // Climber 5: On Step 1 (Y = 0.35, Z = 6.4), exhausted on knees catching breath
    const climber5 = new VoxelCharacter("Climber5");
    climber5.setShirtColor(0xd97706); // Amber
    climber5.root.position.set(-0.7, 0.35, 6.35);
    climber5.root.rotation.set(0, Math.PI, 0);
    scene.add(climber5.root);

    // Climber 6: Also on Step 1 (Y = 0.35, Z = 6.4), stumbling to take a step
    const climber6 = new VoxelCharacter("Climber6");
    climber6.setShirtColor(0x2563eb); // Royal blue
    climber6.root.position.set(0.6, 0.35, 6.30);
    climber6.root.rotation.set(0, Math.PI, 0);
    scene.add(climber6.root);

    // Climber 7: Sat down on Step 2 (Y = 0.70, Z = 5.75) dejected, energy depleted
    const climber7 = new VoxelCharacter("Climber7");
    climber7.setShirtColor(0x7c3aed); // Purple
    climber7.root.position.set(0.5, 0.70, 5.70);
    climber7.root.rotation.set(0, Math.PI, 0);
    scene.add(climber7.root);

    // Climber 8: Reached Step 3 (Y = 1.05, Z = 5.10) — farthest reached, still far down from summit!
    const climber8 = new VoxelCharacter("Climber8");
    climber8.setShirtColor(0x059669); // Emerald green
    climber8.root.position.set(-0.4, 1.05, 5.05);
    climber8.root.rotation.set(0, Math.PI, 0);
    scene.add(climber8.root);

    customUpdate = (t) => {
      // Alex stands heroic beside the flag at the peak
      character.setTriumphantSummit(t);

      // Flag banner wind flutter
      bannerGroup.rotation.y = Math.sin(t * 5.0) * 0.18 + Math.cos(t * 2.8) * 0.08;
      bannerGroup.rotation.z = Math.sin(t * 3.6) * 0.06;

      // Group A (Ground Base)
      climber1.setLookingUpFromBase(t);
      climber2.setSittingDejected(t);
      climber3.setLookingUpFromBase(t);
      climber4.setStumblingFirstStep(t);

      // Group B (Lowest Initial Steps 1 to 3)
      climber5.setFatiguedOnKnees(t);
      climber6.setStumblingFirstStep(t);
      climber7.setSittingDejected(t);
      climber8.setClimbingStairs(t, 2.0);
    };
  }  // =========================================================================
  // SCENE 6: THEN DAY FOUR ARRIVES (Shot 6)
  // Script: "THEN DAY FOUR ARRIVES."
  // 100% Consistent bedroom with Clip 1. Alex in bed on Day 4 waking up tired.
  // Thought bubble floats above head with Tuesday's fire burning inside the bubble!
  // =========================================================================
  else if (shotId === 6) {
    buildStandardBedroom(scene, floorMat, darkOakTrimMat, whiteWoolMat, oakWallMat, {
      timeOfDay: "predawn",
      clockTime: "05:00",
      clockColor: "cyan",
      duvet: "duvet",
      shoesPresent: true,
      phoneFaceDown: true,
    });

    // Alex in bed looking tired
    character.root.position.set(0.2, 0, -0.85);
    const tiredFaceTex = createVoxelFaceTexture(true);
    const tiredFaceMat = new THREE.MeshToonMaterial({ map: tiredFaceTex });
    (character.head.material as THREE.Material[])[4] = tiredFaceMat;

    // Stylized 3D Thought Bubble with Fire Inside
    const thoughtBubble = createThoughtBubbleWithFire();
    scene.add(thoughtBubble.group);

    customUpdate = (t) => {
      character.setLyingInBed(t);
      character.headGroup.rotation.set(0.08, 0.25, -0.05);
      thoughtBubble.update(t);
    };
  }

  // =========================================================================
  // SCENE 7: COLD BEDROOM AT 5:00 AM (Shot 7)
  // Script: "You wake up tired. The room is cold. Your bed is warm."
  // 100% Consistent bedroom assets with Clip 1, 6, 8, 9, 10.
  // =========================================================================
  else if (shotId === 7) {
    buildStandardBedroom(scene, floorMat, darkOakTrimMat, whiteWoolMat, oakWallMat, {
      timeOfDay: "predawn",
      clockTime: "05:00",
      clockColor: "cyan",
      duvet: "duvet",
      shoesPresent: true,
      phoneFaceDown: true,
    });

    character.root.position.set(0.2, 0, -0.85);
    const tiredFaceTex = createVoxelFaceTexture(true);
    const tiredFaceMat = new THREE.MeshToonMaterial({ map: tiredFaceTex });
    (character.head.material as THREE.Material[])[4] = tiredFaceMat;

    customUpdate = (t) => {
      character.setLyingInBed(t);
      character.headGroup.rotation.set(0.05, 0.12, 0);
    };
  }

  // =========================================================================
  // SCENE 8: FIERY MOTIVATION VANISHING INTO THIN AIR (Shot 8)
  // Script: "And suddenly, that fiery motivation from Tuesday has vanished into thin air."
  // Fire burns inside the thought bubble, then sputters, turns to smoke and vanishes.
  // =========================================================================
  else if (shotId === 8) {
    buildStandardBedroom(scene, floorMat, darkOakTrimMat, whiteWoolMat, oakWallMat, {
      timeOfDay: "predawn",
      clockTime: "05:00",
      clockColor: "cyan",
      duvet: "duvet",
      shoesPresent: true,
      phoneFaceDown: true,
    });

    character.root.position.set(0.2, 0, -0.85);
    const tiredFaceTex = createVoxelFaceTexture(true);
    const tiredFaceMat = new THREE.MeshToonMaterial({ map: tiredFaceTex });
    (character.head.material as THREE.Material[])[4] = tiredFaceMat;

    // Stylized Thought Bubble with vanishing fire
    const thoughtBubble = createThoughtBubbleWithFire();
    scene.add(thoughtBubble.group);

    customUpdate = (t) => {
      character.setLyingInBed(t);
      character.headGroup.rotation.set(0.06, 0.28, -0.05);

      // Vanishing fire animation inside thought bubble:
      // t < 2.0s: crackles normally
      // 2.0s <= t <= 4.2s: fades into translucent smoke
      // t > 4.2s: thought bubble and fire vanish
      const vanishStart = 1.8;
      const vanishEnd = 4.0;
      const progress = Math.max(0, Math.min(1, (t - vanishStart) / (vanishEnd - vanishStart)));

      if (progress < 1.0) {
        thoughtBubble.update(t);
        const scale = 1.0 - progress * 0.9;
        thoughtBubble.group.scale.set(scale, scale, scale);
      } else {
        thoughtBubble.group.visible = false;
      }
    };
  }

  // =========================================================================
  // SCENE 9: THE 30-MINUTE NEGOTIATION & SNOOZE SLAP (Shot 9)
  // Script: "You negotiate with yourself for thirty seconds, turn off the alarm, and fall back asleep."
  // Clock displays 05:30 AM. Snooze button press mechanics.
  // =========================================================================
  else if (shotId === 9) {
    const elements = buildStandardBedroom(scene, floorMat, darkOakTrimMat, whiteWoolMat, oakWallMat, {
      timeOfDay: "predawn",
      clockTime: "05:30",
      clockColor: "cyan",
      duvet: "duvet",
      phoneFaceDown: true,
    });

    character.root.position.set(0.35, 0, -0.16);
    const tiredFaceTex = createVoxelFaceTexture(true);
    const tiredFaceMat = new THREE.MeshToonMaterial({ map: tiredFaceTex });
    (character.head.material as THREE.Material[])[4] = tiredFaceMat;

    customUpdate = (t) => {
      character.setNegotiateAlarmAndSleep(t);

      if (t >= 3.2 && t <= 4.0) {
        const pressPhase = (t - 3.2) / 0.8;
        const press = Math.sin(pressPhase * Math.PI);
        elements.buttonTop.position.y = 0.125 - press * 0.022;
      } else {
        elements.buttonTop.position.y = 0.125;
      }
    };
  }

  // =========================================================================
  // SCENE 10: THE WEIGHT OF GUILT AT NOON (Shot 10)
  // Script: "By noon, the familiar weight of guilt sets in. You tell yourself you lack discipline. You tell yourself you are just lazy."
  // Consistent Bedroom: Harsh midday sun, 12:00 PM amber clock.
  // Alex seated naturally on the edge of the mattress with head bowed down in guilt.
  // =========================================================================
  else if (shotId === 10) {
    buildStandardBedroom(scene, floorMat, darkOakTrimMat, whiteWoolMat, oakWallMat, {
      timeOfDay: "noon",
      clockTime: "12:00",
      clockPeriod: "PM",
      clockColor: "amber",
      duvet: "folded",
      phoneFaceDown: true,
    });

    // Alex seated on bed with legs forward, head bowed in guilt
    character.root.position.set(0.20, 0.24, -0.65);
    character.root.rotation.set(0, 0.15, 0);

    const tiredFaceTex = createVoxelFaceTexture(true);
    const tiredFaceMat = new THREE.MeshToonMaterial({ map: tiredFaceTex });
    (character.head.material as THREE.Material[])[4] = tiredFaceMat;

    customUpdate = (t) => {
      character.setSittingGuiltHeadDown(t);
    };
  }

  // =========================================================================
  // SCENE 11: SENIOR MENTOR STAGE (Shot 11)
  // Script: "Here is the truth an experienced senior will tell you."
  // MasterClass Architectural Stage: Tiered walnut platform, acoustic slat wall,
  // theatrical key lighting. Senior Mentor (Marcus) stands facing the Hero (Alex),
  // moving his hand in smooth explanatory gestures while Alex listens attentively.
  // =========================================================================
  else if (shotId === 11) {
    scene.background = new THREE.Color(0x0c1017);

    // 1. Tiered Architectural Stage Platform
    const stageGroup = new THREE.Group();

    // Base Tier (Dark Oak with Brushed Brass Trim)
    const baseGeo = new THREE.CylinderGeometry(2.6, 2.8, 0.16, 36);
    const baseMesh = new THREE.Mesh(baseGeo, darkOakTrimMat);
    baseMesh.position.y = 0.08;
    stageGroup.add(baseMesh);

    const brassRing = new THREE.Mesh(
      new THREE.CylinderGeometry(2.81, 2.81, 0.04, 36),
      new THREE.MeshToonMaterial({ color: 0xd4af37 })
    );
    brassRing.position.y = 0.03;
    stageGroup.add(brassRing);

    // Upper Tier (Spruce Plank Flooring)
    const upperGeo = new THREE.CylinderGeometry(2.1, 2.3, 0.20, 36);
    const upperMesh = new THREE.Mesh(upperGeo, floorMat);
    upperMesh.position.y = 0.24;
    stageGroup.add(upperMesh);

    scene.add(stageGroup);

    // 2. Studio Acoustic Timber Slat Wall in Background
    const backdropGroup = new THREE.Group();
    backdropGroup.position.set(0, 0, -2.1);

    // Matte Slate Rear Wall
    const rearWall = new THREE.Mesh(
      new THREE.BoxGeometry(7.2, 4.4, 0.15),
      new THREE.MeshToonMaterial({ color: 0x111622 })
    );
    rearWall.position.set(0, 2.2, -0.1);
    backdropGroup.add(rearWall);

    // Vertical Architectural Timber Slats
    const slatMat = new THREE.MeshToonMaterial({ color: 0x4a3220 });
    const slatCount = 26;
    for (let i = 0; i < slatCount; i++) {
      const sx = -3.2 + i * 0.256;
      const slat = new THREE.Mesh(new THREE.BoxGeometry(0.08, 4.2, 0.10), slatMat);
      slat.position.set(sx, 2.1, 0.05);
      backdropGroup.add(slat);
    }

    // Warm Amber LED Uplight grazing the timber slats
    const slatUplight = new THREE.PointLight(0xf59e0b, 1.8, 4.5);
    slatUplight.position.set(0, 0.4, 0.2);
    backdropGroup.add(slatUplight);

    scene.add(backdropGroup);

    // 3. Theatrical Studio Lighting
    // Warm Key Spotlight from High Front-Right
    const keySpot = new THREE.SpotLight(0xfff5ea, 3.6, 12, Math.PI / 4, 0.35);
    keySpot.position.set(0.6, 4.0, 2.8);
    keySpot.target.position.set(0, 1.4, 0);
    scene.add(keySpot);
    scene.add(keySpot.target);

    // Front Eye-Level Fill Light to illuminate face & expression
    const faceFill = new THREE.DirectionalLight(0xfffaed, 1.2);
    faceFill.position.set(0, 1.7, 3.2);
    scene.add(faceFill);

    // Cyan Rim Light from Back-Left for sharp voxel silhouette
    const rimLight = new THREE.DirectionalLight(0x00f0ff, 1.5);
    rimLight.position.set(-3.0, 3.5, -1.8);
    scene.add(rimLight);

    // Soft Ambient Studio Fill
    scene.add(new THREE.AmbientLight(0x182030, 0.9));

    // 4. Characters: Senior Mentor (Marcus) & Hero (Alex)
    // Marcus on the right standing in front of Alex, turned toward him
    const mentor = new VoxelCharacter("Marcus");
    mentor.root.position.set(0.55, 0.34, 0.25);
    mentor.root.rotation.set(0, -Math.PI / 2 - 0.45, 0);
    scene.add(mentor.root);

    // Alex on the left, standing facing Marcus attentively
    character.root.position.set(-0.55, 0.34, -0.05);
    character.root.rotation.set(0, Math.PI / 2 - 0.35, 0);
    character.root.visible = true;

    customUpdate = (t) => {
      // Marcus moves his hand with natural explanatory arcs
      mentor.setExplainingToHero(t);
      // Alex listens attentively with subtle nods
      character.setListeningHero(t);
    };
  }

  // =========================================================================
  // SCENE 12: THE BROKEN WILLPOWER LEVER (Shot 12)
  // =========================================================================
  // =========================================================================
  // SCENE 12: THE BROKEN WILLPOWER MECHANISM (Shot 12)
  // Script: "You did not fail because you lack willpower. You failed because you asked willpower to do a job it was never built for."
  // Visual: Heavy industrial test apparatus labeled "WILLPOWER". Lever arm snapped
  // in half under a colossal "RADICAL OVERHAUL" crushing block, with glowing stress fractures.
  // Alex stands beside it, observing the catastrophic failure in profound realization.
  // =========================================================================
  // =========================================================================
  // SCENE 12: THE WRONG JOB FOR WILLPOWER (Shot 12)
  // Script: "You did not fail because you lack willpower. You failed because you asked willpower to do a job it was never built for."
  // Visual Clarity: MasterClass Studio Demonstration Table contrasting:
  // 1. LEFT: "WILLPOWER" - A tiny fragile glass battery cell crushed and sparking
  //    under an impossibly massive 500kg iron weight block.
  // 2. RIGHT: "DAILY HABIT SYSTEM" - An elegant brass & steel gear train with
  //    3 intermeshed rotating cogs and pulley cable lifting weight effortlessly.
  // Marcus gestures between both sides, while Alex observes in sudden enlightenment.
  // =========================================================================
  else if (shotId === 12) {
    scene.background = new THREE.Color(0x0c1017);

    // 1. Studio Platform Base
    const floor = new THREE.Mesh(new THREE.BoxGeometry(8.0, 0.2, 8.0), floorMat);
    floor.position.y = -0.1;
    scene.add(floor);

    // Rear Acoustic Timber Slat Backdrop
    const rearWall = new THREE.Mesh(
      new THREE.BoxGeometry(7.6, 4.4, 0.15),
      new THREE.MeshToonMaterial({ color: 0x111622 })
    );
    rearWall.position.set(0, 2.2, -2.2);
    scene.add(rearWall);

    const slatMat = new THREE.MeshToonMaterial({ color: 0x4a3220 });
    for (let i = 0; i < 28; i++) {
      const sx = -3.4 + i * 0.252;
      const slat = new THREE.Mesh(new THREE.BoxGeometry(0.08, 4.2, 0.10), slatMat);
      slat.position.set(sx, 2.1, -2.05);
      scene.add(slat);
    }

    // 2. Central Demonstration Table
    const tableGroup = new THREE.Group();
    tableGroup.position.set(0, 0, -0.2);

    const tableTop = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.10, 1.4), darkOakTrimMat);
    tableTop.position.set(0, 0.85, 0);
    tableGroup.add(tableTop);

    for (const [tx, tz] of [[-1.65, -0.55], [1.65, -0.55], [-1.65, 0.55], [1.65, 0.55]]) {
      const leg = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.85, 0.10), darkOakTrimMat);
      leg.position.set(tx, 0.425, tz);
      tableGroup.add(leg);
    }

    // -----------------------------------------------------------------------
    // LEFT SIDE: TINY CRUSHED WILLPOWER CELL (SPARK PLUG)
    // -----------------------------------------------------------------------
    const cellGroup = new THREE.Group();
    cellGroup.position.set(-1.0, 0.90, 0);

    // Pedestal base with label plaque
    const cellBase = new THREE.Mesh(
      new THREE.BoxGeometry(0.90, 0.08, 0.90),
      new THREE.MeshToonMaterial({ color: 0x1c1917 })
    );
    cellBase.position.y = 0.04;
    cellGroup.add(cellBase);

    // Red warning accent rim
    const cellRim = new THREE.Mesh(
      new THREE.BoxGeometry(0.86, 0.02, 0.86),
      new THREE.MeshBasicMaterial({ color: 0xef4444 })
    );
    cellRim.position.y = 0.09;
    cellGroup.add(cellRim);

    // Fragile cylindrical glass battery chamber (crushed/shattered)
    const glassTube = new THREE.Mesh(
      new THREE.CylinderGeometry(0.20, 0.20, 0.35, 16),
      new THREE.MeshToonMaterial({ color: 0xfee2e2, transparent: true, opacity: 0.55 })
    );
    glassTube.position.y = 0.26;
    cellGroup.add(glassTube);

    // Dead 0% red depleted battery filament inside
    const deadCore = new THREE.Mesh(
      new THREE.CylinderGeometry(0.08, 0.08, 0.22, 12),
      new THREE.MeshBasicMaterial({ color: 0xdc2626 })
    );
    deadCore.position.y = 0.26;
    cellGroup.add(deadCore);

    // Colossal 500kg dark iron crushing block resting right on top of the tiny battery
    const crushingBlock = new THREE.Mesh(
      new THREE.BoxGeometry(0.80, 0.65, 0.70),
      new THREE.MeshToonMaterial({ color: 0x27272a })
    );
    crushingBlock.position.set(0, 0.76, 0);
    cellGroup.add(crushingBlock);

    // Stress cracks on crushing block
    const crackMat = new THREE.MeshBasicMaterial({ color: 0xef4444 });
    const crackA = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.45, 0.03), crackMat);
    crackA.rotation.z = 0.35;
    crackA.position.set(0.05, 0.76, 0.36);
    cellGroup.add(crackA);

    // Feeble warning sparks flickering at base of crushed battery
    const sparkLight = new THREE.PointLight(0xff3300, 2.2, 2.5);
    sparkLight.position.set(0, 0.35, 0.25);
    cellGroup.add(sparkLight);

    tableGroup.add(cellGroup);

    // -----------------------------------------------------------------------
    // RIGHT SIDE: EFFORTLESS ROTATING GEAR SYSTEM & PULLEY
    // -----------------------------------------------------------------------
    const gearGroup = new THREE.Group();
    gearGroup.position.set(1.0, 0.90, 0);

    // Sturdy brass machinery mounting frame
    const brassMat = new THREE.MeshToonMaterial({ color: 0xd4af37 });
    const steelMat = new THREE.MeshToonMaterial({ color: 0x71717a });

    const gearBase = new THREE.Mesh(
      new THREE.BoxGeometry(1.10, 0.08, 0.90),
      new THREE.MeshToonMaterial({ color: 0x1e293b })
    );
    gearBase.position.y = 0.04;
    gearGroup.add(gearBase);

    // Glowing cyan accent line on habit system
    const sysRim = new THREE.Mesh(
      new THREE.BoxGeometry(1.06, 0.02, 0.86),
      new THREE.MeshBasicMaterial({ color: 0x00f0ff })
    );
    sysRim.position.y = 0.09;
    gearGroup.add(sysRim);

    // Frame uprights
    const postA = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.85, 0.06), steelMat);
    postA.position.set(-0.35, 0.50, -0.20);
    gearGroup.add(postA);

    const postB = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.85, 0.06), steelMat);
    postB.position.set(0.35, 0.50, -0.20);
    gearGroup.add(postB);

    const crossArm = new THREE.Mesh(new THREE.BoxGeometry(0.80, 0.06, 0.06), steelMat);
    crossArm.position.set(0, 0.90, -0.20);
    gearGroup.add(crossArm);

    // 3 Intermeshed Rotating Clockwork Cogwheels
    // Gear 1: Large drive gear (brass)
    const gear1 = new THREE.Group();
    gear1.position.set(-0.15, 0.52, -0.12);
    const g1Center = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.04, 16), brassMat);
    g1Center.rotation.x = Math.PI / 2;
    gear1.add(g1Center);
    for (let c = 0; c < 8; c++) {
      const tooth = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.06, 0.04), brassMat);
      const angle = (c / 8) * Math.PI * 2;
      tooth.position.set(Math.cos(angle) * 0.28, Math.sin(angle) * 0.28, 0);
      tooth.rotation.z = angle;
      gear1.add(tooth);
    }
    gearGroup.add(gear1);

    // Gear 2: Intermediate gear (cyan steel)
    const gear2 = new THREE.Group();
    gear2.position.set(0.22, 0.65, -0.12);
    const g2Mat = new THREE.MeshToonMaterial({ color: 0x0284c7 });
    const g2Center = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.04, 14), g2Mat);
    g2Center.rotation.x = Math.PI / 2;
    gear2.add(g2Center);
    for (let c = 0; c < 6; c++) {
      const tooth = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.05, 0.04), g2Mat);
      const angle = (c / 6) * Math.PI * 2;
      tooth.position.set(Math.cos(angle) * 0.18, Math.sin(angle) * 0.18, 0);
      tooth.rotation.z = angle;
      gear2.add(tooth);
    }
    gearGroup.add(gear2);

    // Overhead Pulley Drum & Cable effortlessly holding counterweight
    const pulley = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.14, 14), steelMat);
    pulley.rotation.z = Math.PI / 2;
    pulley.position.set(0.35, 0.88, 0.05);
    gearGroup.add(pulley);

    // Cable extending down
    const cable = new THREE.Mesh(
      new THREE.CylinderGeometry(0.012, 0.012, 0.45),
      new THREE.MeshBasicMaterial({ color: 0xe2e8f0 })
    );
    cable.position.set(0.35, 0.65, 0.05);
    gearGroup.add(cable);

    // Smoothly suspended weight block lifted with mechanical advantage
    const liftedWeight = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.28, 0.28), steelMat);
    liftedWeight.position.set(0.35, 0.40, 0.05);
    gearGroup.add(liftedWeight);

    tableGroup.add(gearGroup);
    scene.add(tableGroup);

    // 3. Characters: Marcus (Senior Mentor) & Alex (Hero)
    // Marcus stands on the right beside the gear system, gesturing smoothly
    const mentor = new VoxelCharacter("Marcus");
    mentor.root.position.set(1.45, 0, 0.15);
    mentor.root.rotation.set(0, -Math.PI / 4, 0);
    scene.add(mentor.root);

    // Alex stands on the left beside the crushed willpower cell, looking in revelation
    character.root.position.set(-1.45, 0, 0.25);
    character.root.rotation.set(0, Math.PI / 4, 0);
    character.root.visible = true;

    // Theatrical Studio Lighting
    const keySpot = new THREE.SpotLight(0xfff5ea, 3.4, 12, Math.PI / 4, 0.35);
    keySpot.position.set(0, 4.2, 3.2);
    keySpot.target.position.set(0, 1.2, 0);
    scene.add(keySpot);
    scene.add(keySpot.target);

    const cyanAccent = new THREE.DirectionalLight(0x00f0ff, 1.4);
    cyanAccent.position.set(3.0, 2.5, 2.0);
    scene.add(cyanAccent);

    scene.add(new THREE.AmbientLight(0x182030, 0.95));

    customUpdate = (t) => {
      // Intermeshed gears rotate continuously in opposite directions
      gear1.rotation.z = t * 1.8;
      gear2.rotation.z = -t * 2.7;

      // Gentle floating lift on the suspended weight
      liftedWeight.position.y = 0.40 + Math.sin(t * 1.8) * 0.04;
      cable.scale.y = 1.0 - Math.sin(t * 1.8) * 0.08;

      // Feeble spark flicker on the dead willpower battery
      sparkLight.intensity = 1.8 + Math.sin(t * 16.0) * 0.6;

      // Marcus gestures explaining the difference
      mentor.setExplainingToHero(t);

      // Alex listens attentively, looking at the demonstration
      character.setListeningHero(t);
    };
  }

  // =========================================================================
  // SCENE 13: THE SURVIVAL BRAIN (Shot 13)
  // Script: "Your brain is not an inspiration machine. Your brain is a survival organ designed to conserve energy."
  // Visual: Deep neural cyber-space, floating platform dais, intricate 3D
  // bioluminescent cyan/amber voxel brain with pulsing synaptic conduits.
  // Clean architectural framing without heavy text billboards.
  // Marcus lectures beside the matrix.
  // =========================================================================
  else if (shotId === 13) {
    scene.background = new THREE.Color(0x050811);

    // 1. Floating Holographic Platform Dais
    const platform = new THREE.Group();
    const daisBase = new THREE.Mesh(
      new THREE.CylinderGeometry(2.4, 2.6, 0.16, 36),
      new THREE.MeshToonMaterial({ color: 0x121722 })
    );
    daisBase.position.y = 0.08;
    platform.add(daisBase);

    // Glowing Cyan Trim Ring
    const trimRing = new THREE.Mesh(
      new THREE.CylinderGeometry(2.61, 2.61, 0.03, 36),
      new THREE.MeshBasicMaterial({ color: 0x00f0ff })
    );
    trimRing.position.y = 0.04;
    platform.add(trimRing);

    // Upper Circular Surface
    const daisSurface = new THREE.Mesh(
      new THREE.CylinderGeometry(2.1, 2.1, 0.08, 36),
      new THREE.MeshToonMaterial({ color: 0x1a2130 })
    );
    daisSurface.position.y = 0.16;
    platform.add(daisSurface);
    scene.add(platform);

    // 2. 3D Bioluminescent Neural Voxel Brain Model
    const brainGroup = new THREE.Group();
    brainGroup.position.set(0.9, 1.45, 0.1);

    const voxelSize = 0.14;
    const vGeo = new THREE.BoxGeometry(voxelSize * 0.90, voxelSize * 0.90, voxelSize * 0.90);
    const cyanOuterMat = new THREE.MeshToonMaterial({
      color: 0x00b8e6,
      emissive: 0x002d4d,
      emissiveIntensity: 0.35,
    });
    const cyanBrightMat = new THREE.MeshBasicMaterial({ color: 0x5ce1e6 });
    const coreAmberMat = new THREE.MeshToonMaterial({
      color: 0xff9900,
      emissive: 0x994400,
      emissiveIntensity: 0.6,
    });

    const synapticPulseVoxels: THREE.Mesh[] = [];

    // Construct dual-hemisphere voxel brain
    for (let xi = -6; xi <= 6; xi++) {
      for (let yi = -5; yi <= 5; yi++) {
        for (let zi = -6; zi <= 6; zi++) {
          const x = xi * voxelSize;
          const y = yi * voxelSize;
          const z = zi * voxelSize;

          const normX = x / 0.88;
          const normY = (y + (z < -0.2 ? 0.08 : 0)) / 0.72;
          const normZ = (z - 0.05) / 0.92;
          const distSq = normX * normX + normY * normY + normZ * normZ;

          if (distSq <= 1.0) {
            const isFissure = Math.abs(x) < 0.075;
            const isCorpusCallosum = isFissure && y < 0.05 && y > -0.20 && Math.abs(z) < 0.35;

            if (!isFissure || isCorpusCallosum) {
              const isCore = distSq < 0.25;
              let mat: THREE.Material = cyanOuterMat;
              if (isCore) {
                mat = coreAmberMat;
              } else if (Math.random() < 0.14) {
                mat = cyanBrightMat;
              }

              const cube = new THREE.Mesh(vGeo, mat);
              cube.position.set(x, y, z);
              brainGroup.add(cube);

              if (mat === cyanBrightMat) {
                synapticPulseVoxels.push(cube);
              }
            }
          }
        }
      }
    }

    // Concentric Holographic Orbital Rings around Brain
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.35,
      wireframe: true,
    });
    const orbitRing1 = new THREE.Mesh(new THREE.TorusGeometry(1.28, 0.012, 8, 48), ringMat);
    orbitRing1.rotation.x = Math.PI / 3;
    brainGroup.add(orbitRing1);

    const orbitRing2 = new THREE.Mesh(new THREE.TorusGeometry(1.38, 0.010, 8, 48), ringMat);
    orbitRing2.rotation.y = Math.PI / 4;
    brainGroup.add(orbitRing2);

    scene.add(brainGroup);

    // 3. Balanced Studio Fill & Synaptic Glow (Heavy text billboard removed per user request)
    const brainLight = new THREE.PointLight(0x00e5ff, 1.8, 6);
    brainLight.position.set(0.9, 1.45, 0.4);
    scene.add(brainLight);

    const coreAmberLight = new THREE.PointLight(0xff7700, 1.4, 3);
    coreAmberLight.position.set(0.9, 1.45, 0.1);
    scene.add(coreAmberLight);

    const keySpot = new THREE.SpotLight(0xfffaed, 2.6, 12, Math.PI / 4, 0.4);
    keySpot.position.set(-1.2, 4.0, 3.0);
    keySpot.target.position.set(-0.85, 1.0, 0.3);
    scene.add(keySpot);
    scene.add(keySpot.target);

    scene.add(new THREE.AmbientLight(0x182436, 0.95));

    // 4. Senior Mentor (Marcus) Lecturing Beside the Matrix
    const mentor = new VoxelCharacter("Marcus");
    mentor.root.position.set(-0.85, 0.20, 0.3);
    scene.add(mentor.root);
    character.root.visible = false; // Alex is off-stage viewing the presentation

    customUpdate = (t) => {
      // Smooth slow rotation & organic floating bob of brain matrix
      brainGroup.rotation.y = t * 0.42;
      brainGroup.position.y = 1.45 + Math.sin(t * 1.6) * 0.05;

      orbitRing1.rotation.z = t * 0.5;
      orbitRing2.rotation.x = t * 0.35;

      // Pulse synaptic nodes
      for (let i = 0; i < synapticPulseVoxels.length; i++) {
        const s = 1.0 + Math.sin(t * 5.0 + i * 1.3) * 0.25;
        synapticPulseVoxels[i].scale.set(s, s, s);
      }

      // Mentor gestures towards the brain matrix
      mentor.setMentorSpeak(t);
      mentor.root.rotation.set(0, 0.42, 0);
    };
  }

  // =========================================================================
  // SCENE 14: THE HOMEOSTATIC ALARM (Shot 14)
  // Script: "When you try to force huge, drastic changes overnight, your biology sounds the alarm."
  // Visual: High-stakes industrial biological emergency platform, dual revolving
  // crimson emergency beacons sweeping the scene, hazard chevrons.
  // Heavy text billboard removed per user directive. Alex braces against the biological storm.
  // =========================================================================
  else if (shotId === 14) {
    scene.background = new THREE.Color(0x0a0204);

    // 1. Heavy Industrial Hazard Platform
    const platform = new THREE.Group();
    const ironFloor = new THREE.Mesh(
      new THREE.BoxGeometry(6.6, 0.22, 6.6),
      new THREE.MeshToonMaterial({ color: 0x14161c })
    );
    ironFloor.position.y = -0.11;
    platform.add(ironFloor);

    // Hazard Yellow & Black Safety Borders
    const hazardMatY = new THREE.MeshBasicMaterial({ color: 0xffcc00 });
    const hazardMatK = new THREE.MeshBasicMaterial({ color: 0x111111 });

    for (let i = 0; i < 18; i++) {
      const segX = -3.15 + i * 0.35;
      const segMat = i % 2 === 0 ? hazardMatY : hazardMatK;
      const segF = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.23, 0.14), segMat);
      segF.position.set(segX, -0.10, 3.23);
      platform.add(segF);
      const segB = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.23, 0.14), segMat);
      segB.position.set(segX, -0.10, -3.23);
      platform.add(segB);
    }
    scene.add(platform);

    // 2. Industrial Emergency Siren Tower
    const towerGroup = new THREE.Group();
    towerGroup.position.set(1.65, 0, -0.6);

    const steelMat = new THREE.MeshToonMaterial({ color: 0x242832 });
    const rustDarkMat = new THREE.MeshToonMaterial({ color: 0x3d1c1c });

    for (const [tx, tz] of [[-0.30, -0.30], [0.30, -0.30], [-0.30, 0.30], [0.30, 0.30]]) {
      const col = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.9, 0.08), steelMat);
      col.position.set(tx, 0.95, tz);
      towerGroup.add(col);
    }

    for (const sy of [0.6, 1.2, 1.8]) {
      const ring = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.06, 0.68), rustDarkMat);
      ring.position.y = sy;
      towerGroup.add(ring);
    }

    const headPlatform = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.48, 0.10, 16), steelMat);
    headPlatform.position.y = 1.95;
    towerGroup.add(headPlatform);

    // Rotating Siren Beacon Assembly
    const sirenRotator = new THREE.Group();
    sirenRotator.position.y = 2.12;

    const sirenHub = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.22, 16), rustDarkMat);
    sirenRotator.add(sirenHub);

    // Dual Ruby Emergency Domes
    const rubyMat = new THREE.MeshBasicMaterial({ color: 0xff0033 });
    const lensL = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.22, 16), rubyMat);
    lensL.position.x = -0.26;
    lensL.rotation.z = Math.PI / 2;
    sirenRotator.add(lensL);

    const lensR = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.22, 16), rubyMat);
    lensR.position.x = 0.26;
    lensR.rotation.z = Math.PI / 2;
    sirenRotator.add(lensR);

    // Sweeping Emergency Spotlights
    const spotL = new THREE.SpotLight(0xff0033, 5.5, 14, Math.PI / 5, 0.35);
    spotL.position.set(-0.30, 0, 0);
    const targetL = new THREE.Object3D();
    targetL.position.set(-6.0, -1.2, 0);
    sirenRotator.add(spotL);
    sirenRotator.add(targetL);
    spotL.target = targetL;

    const spotR = new THREE.SpotLight(0xff0033, 5.5, 14, Math.PI / 5, 0.35);
    spotR.position.set(0.30, 0, 0);
    const targetR = new THREE.Object3D();
    targetR.position.set(6.0, -1.2, 0);
    sirenRotator.add(spotR);
    sirenRotator.add(targetR);
    spotR.target = targetR;

    towerGroup.add(sirenRotator);
    scene.add(towerGroup);

    // 3. Balanced Studio Fill & Sweeping Red Alarm Lights (Heavy text billboard removed)
    const frontFill = new THREE.DirectionalLight(0xe8edf8, 1.2);
    frontFill.position.set(0, 2.0, 4.0);
    scene.add(frontFill);

    const redStrobe = new THREE.PointLight(0xff002b, 2.8, 10);
    redStrobe.position.set(0, 3.2, 0);
    scene.add(redStrobe);

    scene.add(new THREE.AmbientLight(0x280e14, 0.90));

    // 4. Alex Bracing Against the Biological Emergency
    character.root.position.set(0, 0, 0.2);
    character.root.visible = true;

    customUpdate = (t) => {
      character.setBracingWind(t);
      sirenRotator.rotation.y = t * 6.2;
      redStrobe.intensity = Math.sin(t * 10.0) > 0 ? 3.0 : 0.4;
    };
  }

  // =========================================================================
  // SCENE 15: REAL GYM VS REAL STUDY (Shot 15)
  // Script: "Day by day, the man who went to the gym for twenty minutes is laughing at the man who killed himself on day one and quit."
  // Left: Iron Forge Gym - Alex in athletic posture performing clean, rhythmic
  //       dumbbell bicep curls with hex dumbbells.
  // Right: Cozy Study - Marcus sitting comfortably in chair, a stack of 2-3 books
  //        on the desk, holding an open hardcover book in both hands reading peacefully.
  // =========================================================================
  else if (shotId === 15) {
    scene.background = new THREE.Color(0x181e28);

    // -----------------------------------------------------------------------
    // LEFT SIDE: IRON FORGE GYM (Real Gym Set)
    // -----------------------------------------------------------------------
    const gymGroup = new THREE.Group();
    gymGroup.position.set(-2.5, 0, 0);

    // 1. Black heavy-duty rubber gym floor mat with safety border
    const rubberMat = new THREE.Mesh(
      new THREE.BoxGeometry(4.8, 0.22, 5.0),
      new THREE.MeshToonMaterial({ color: 0x18181c })
    );
    rubberMat.position.y = -0.09;
    gymGroup.add(rubberMat);

    const hazardBorder = new THREE.Mesh(
      new THREE.BoxGeometry(4.8, 0.23, 0.1),
      new THREE.MeshBasicMaterial({ color: 0xffd700 })
    );
    hazardBorder.position.set(0, -0.08, 2.45);
    gymGroup.add(hazardBorder);

    // 2. Concrete gym wall with full-height mirror & Banner
    const gymWall = new THREE.Mesh(
      new THREE.BoxGeometry(4.8, 3.8, 0.2),
      new THREE.MeshToonMaterial({ color: 0x2a2e36 })
    );
    gymWall.position.set(0, 1.9, -2.4);
    gymGroup.add(gymWall);

    const gymMirror = new THREE.Mesh(
      new THREE.BoxGeometry(3.6, 2.0, 0.04),
      new THREE.MeshBasicMaterial({ color: 0x6e8a9c, transparent: true, opacity: 0.85 })
    );
    gymMirror.position.set(0, 1.7, -2.28);
    gymGroup.add(gymMirror);

    // "IRON FORGE // NO DAYS OFF" Banner above mirror
    const gymBannerTex = createGymBannerTexture();
    const gymBanner = new THREE.Mesh(
      new THREE.BoxGeometry(3.4, 0.72, 0.04),
      new THREE.MeshBasicMaterial({ map: gymBannerTex })
    );
    gymBanner.position.set(0, 3.25, -2.28);
    gymGroup.add(gymBanner);

    // 3. Dumbbell Storage Rack on the Left Wall
    const plateMat = new THREE.MeshToonMaterial({ color: 0x141416 });
    const dbStand = new THREE.Mesh(
      new THREE.BoxGeometry(0.6, 0.75, 1.6),
      new THREE.MeshToonMaterial({ color: 0x2c3038 })
    );
    dbStand.position.set(-1.8, 0.38, 0.3);
    gymGroup.add(dbStand);

    for (let d = -0.5; d <= 0.5; d += 0.35) {
      const db = new THREE.Group();
      const h = new THREE.Mesh(
        new THREE.CylinderGeometry(0.02, 0.02, 0.26),
        new THREE.MeshToonMaterial({ color: 0xd8d8d8 })
      );
      db.add(h);
      const wL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.06), plateMat);
      wL.position.y = -0.11;
      db.add(wL);
      const wR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.06), plateMat);
      wR.position.y = 0.11;
      db.add(wR);
      db.rotation.x = Math.PI / 2;
      db.position.set(-1.8, 0.8, 0.3 + d);
      gymGroup.add(db);
    }
    scene.add(gymGroup);

    // 4. Pair of Hex Dumbbells Attached to Alex's Hands
    // Right Dumbbell
    const dbRight = new THREE.Group();
    const handleR = new THREE.Mesh(
      new THREE.CylinderGeometry(0.022, 0.022, 0.28),
      new THREE.MeshToonMaterial({ color: 0xd8d8d8 })
    );
    dbRight.add(handleR);
    const weightR1 = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.13, 0.07), plateMat);
    weightR1.position.y = -0.12;
    dbRight.add(weightR1);
    const weightR2 = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.13, 0.07), plateMat);
    weightR2.position.y = 0.12;
    dbRight.add(weightR2);
    dbRight.rotation.x = Math.PI / 2;
    dbRight.position.set(0, -0.62, 0); // At hand level
    character.armRight.add(dbRight);

    // Left Dumbbell
    const dbLeft = new THREE.Group();
    const handleL = new THREE.Mesh(
      new THREE.CylinderGeometry(0.022, 0.022, 0.28),
      new THREE.MeshToonMaterial({ color: 0xd8d8d8 })
    );
    dbLeft.add(handleL);
    const weightL1 = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.13, 0.07), plateMat);
    weightL1.position.y = -0.12;
    dbLeft.add(weightL1);
    const weightL2 = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.13, 0.07), plateMat);
    weightL2.position.y = 0.12;
    dbLeft.add(weightL2);
    dbLeft.rotation.x = Math.PI / 2;
    dbLeft.position.set(0, -0.62, 0); // At hand level
    character.armLeft.add(dbLeft);

    // Position Alex in the center of the gym mat
    character.root.position.set(-2.5, 0, 0.2);
    character.root.rotation.set(0, 0.15, 0);
    character.root.visible = true;

    // -----------------------------------------------------------------------
    // RIGHT SIDE: COZY STUDY & READING ROUTINE (Real Study Set)
    // -----------------------------------------------------------------------
    const studyGroup = new THREE.Group();
    studyGroup.position.set(2.5, 0, 0);

    // 1. Warm spruce hardwood floor
    const studyFloor = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.22, 5.0), floorMat);
    studyFloor.position.y = -0.09;
    studyGroup.add(studyFloor);

    // 2. Warm cream wall with sunlight window
    const studyWall = new THREE.Mesh(
      new THREE.BoxGeometry(4.8, 3.8, 0.2),
      new THREE.MeshToonMaterial({ color: 0xf5f0ea })
    );
    studyWall.position.set(0, 1.9, -2.4);
    studyGroup.add(studyWall);

    const studyWindow = new THREE.Mesh(
      new THREE.BoxGeometry(1.6, 1.5, 0.24),
      new THREE.MeshBasicMaterial({ color: 0xfff2cc, transparent: true, opacity: 0.85 })
    );
    studyWindow.position.set(0.6, 2.0, -2.35);
    studyGroup.add(studyWindow);

    // 3. Polished Oak Study Desk
    const studyDesk = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.1, 1.0), oakWallMat);
    studyDesk.position.set(0, 0.85, 0.35);
    studyGroup.add(studyDesk);

    for (const [dx, dz] of [[-0.9, -0.1], [0.9, -0.1], [-0.9, 0.8], [0.9, 0.8]]) {
      const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.85, 0.08), darkOakTrimMat);
      leg.position.set(dx, 0.425, dz);
      studyGroup.add(leg);
    }

    // Brass Desk Lamp with warm glow
    const brassMat = new THREE.MeshToonMaterial({ color: 0xd4af37 });
    const lampStem = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.4), brassMat);
    lampStem.position.set(-0.65, 1.10, 0.25);
    studyGroup.add(lampStem);
    const lampShade = new THREE.Mesh(new THREE.ConeGeometry(0.14, 0.16, 8), brassMat);
    lampShade.rotation.z = 0.4;
    lampShade.position.set(-0.57, 1.28, 0.25);
    studyGroup.add(lampShade);

    const studyLampLight = new THREE.PointLight(0xffe6a3, 1.8, 2.5);
    studyLampLight.position.set(-0.55, 1.20, 0.30);
    studyGroup.add(studyLampLight);

    // Steaming Tea / Coffee Mug on desk
    const mug = new THREE.Mesh(
      new THREE.CylinderGeometry(0.08, 0.08, 0.15, 12),
      new THREE.MeshBasicMaterial({ color: 0x00f0ff })
    );
    mug.position.set(-0.35, 0.98, 0.50);
    studyGroup.add(mug);

    // Stack of 2-3 Books on Desk ("there should be 2-3 book stack")
    const bookStackGroup = new THREE.Group();
    bookStackGroup.position.set(0.55, 0.90, 0.35);

    // Bottom Book: Navy Leather
    const book1 = new THREE.Mesh(
      new THREE.BoxGeometry(0.38, 0.065, 0.28),
      new THREE.MeshToonMaterial({ color: 0x1e3a8a })
    );
    book1.position.y = 0.0325;
    bookStackGroup.add(book1);

    // Middle Book: Deep Crimson
    const book2 = new THREE.Mesh(
      new THREE.BoxGeometry(0.35, 0.055, 0.26),
      new THREE.MeshToonMaterial({ color: 0x991b1b })
    );
    book2.position.set(0.01, 0.0925, 0.01);
    book2.rotation.y = 0.08;
    bookStackGroup.add(book2);

    // Top Book: Emerald Green
    const book3 = new THREE.Mesh(
      new THREE.BoxGeometry(0.32, 0.050, 0.24),
      new THREE.MeshToonMaterial({ color: 0x065f46 })
    );
    book3.position.set(-0.01, 0.145, -0.01);
    book3.rotation.y = -0.05;
    bookStackGroup.add(book3);

    studyGroup.add(bookStackGroup);

    // Potted Green Indoor Plant
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.15, 0.35, 8), darkOakTrimMat);
    pot.position.set(1.6, 0.18, -1.4);
    studyGroup.add(pot);
    const bush = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.65, 0.55), leavesMat);
    bush.position.set(1.6, 0.6, -1.4);
    studyGroup.add(bush);

    // 4. Oak Study Chair for Marcus (Cleanly seated)
    const chairSeat = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.08, 0.62), darkOakTrimMat);
    chairSeat.position.set(0, 0.44, -0.15);
    studyGroup.add(chairSeat);

    const chairBack = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.70, 0.08), darkOakTrimMat);
    chairBack.position.set(0, 0.82, -0.42);
    studyGroup.add(chairBack);

    for (const [cx, cz] of [[-0.28, -0.38], [0.28, -0.38], [-0.28, 0.08], [0.28, 0.08]]) {
      const leg = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.44, 0.06), darkOakTrimMat);
      leg.position.set(cx, 0.22, cz);
      studyGroup.add(leg);
    }

    // Marcus Sitting in Chair Reading an Open Hardcover Book
    const calmMarcus = new VoxelCharacter("Marcus");
    calmMarcus.root.position.set(0, 0.44, -0.12);

    // 3D Open Hardcover Book in Marcus's Hands
    const openBookGroup = new THREE.Group();
    openBookGroup.position.set(0, 0.26, 0.34);
    openBookGroup.rotation.x = 0.32; // Angled facing up towards Marcus's eyes

    const bookCoverMat = new THREE.MeshToonMaterial({ color: 0x78350f }); // Rich amber leather cover
    const pageMat = new THREE.MeshBasicMaterial({ color: 0xfffcf0 }); // Ivory pages

    // Left Page Wing
    const leftPage = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.016, 0.28), pageMat);
    leftPage.position.set(-0.11, 0, 0);
    leftPage.rotation.z = 0.14;
    openBookGroup.add(leftPage);

    // Right Page Wing
    const rightPage = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.016, 0.28), pageMat);
    rightPage.position.set(0.11, 0, 0);
    rightPage.rotation.z = -0.14;
    openBookGroup.add(rightPage);

    // Spine
    const bookSpine = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.024, 0.29), bookCoverMat);
    bookSpine.position.set(0, -0.01, 0);
    openBookGroup.add(bookSpine);

    calmMarcus.root.add(openBookGroup);
    studyGroup.add(calmMarcus.root);

    scene.add(studyGroup);

    // Studio Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.95));

    const gymSpotlight = new THREE.DirectionalLight(0xffffff, 1.4);
    gymSpotlight.position.set(-2.5, 4.0, 2.0);
    scene.add(gymSpotlight);

    const windowSun = new THREE.DirectionalLight(0xfff4d6, 1.8);
    windowSun.position.set(4.2, 4.5, 1.0);
    windowSun.target.position.set(2.5, 1.0, 0.0);
    scene.add(windowSun);
    scene.add(windowSun.target);

    customUpdate = (t) => {
      // Alex performs athletic dumbbell bicep curls with proper form
      character.setDumbbellCurls(t);

      // Marcus sits comfortably reading his book peacefully
      calmMarcus.setSittingReadingBook(t);
    };
  }

  // =========================================================================
  // SCENE 16: THE ELIMINATION GATEWAY (Shot 16)
  // Script: "Consistency is not an act of willpower, it is the elimination of choice."
  // Alex facing -Z (back to camera, walking away down the corridor).
  // The camera tracks behind him, following him toward the radiant cyan gateway.
  // =========================================================================
  else if (shotId === 16) {
    scene.background = new THREE.Color(0x080c16);

    const darkSteelMat = new THREE.MeshStandardMaterial({
      color: 0x141822,
      roughness: 0.4,
      metalness: 0.8,
    });

    // Deep polished dark graphite runway
    const floorGeo = new THREE.BoxGeometry(4.6, 0.2, 22.0);
    const corridorFloor = new THREE.Mesh(floorGeo, darkSteelMat);
    corridorFloor.position.set(0, -0.1, 0);
    scene.add(corridorFloor);

    // Central glowing cyan runway guide line with pulsing energy
    const runway = new THREE.Mesh(
      new THREE.BoxGeometry(0.5, 0.22, 22.0),
      new THREE.MeshBasicMaterial({ color: 0x00f0ff })
    );
    runway.position.set(0, -0.09, 0);
    scene.add(runway);

    // Directional chevron markers along the center path
    const chevronMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    for (let cz = -8; cz <= 8; cz += 2.5) {
      const chevronL = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.23, 0.4), chevronMat);
      chevronL.position.set(-0.12, -0.08, cz);
      chevronL.rotation.y = 0.5;
      scene.add(chevronL);
      const chevronR = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.23, 0.4), chevronMat);
      chevronR.position.set(0.12, -0.08, cz);
      chevronR.rotation.y = -0.5;
      scene.add(chevronR);
    }

    // Heavy reinforced blast doors and structural portals
    const lockedDoorTex = createLockedBlastDoorTexture();
    const lockedDoorMat = new THREE.MeshStandardMaterial({
      map: lockedDoorTex,
      roughness: 0.4,
      metalness: 0.7,
    });

    const doorPositions = [-6.0, -2.5, 1.0, 4.5];
    const doorLights: THREE.PointLight[] = [];

    doorPositions.forEach((dz) => {
      // Portal arch overhead
      const portalArchL = new THREE.Mesh(new THREE.BoxGeometry(0.4, 3.8, 0.4), darkOakTrimMat);
      portalArchL.position.set(-2.2, 1.8, dz);
      scene.add(portalArchL);

      const portalArchR = new THREE.Mesh(new THREE.BoxGeometry(0.4, 3.8, 0.4), darkOakTrimMat);
      portalArchR.position.set(2.2, 1.8, dz);
      scene.add(portalArchR);

      const portalLintel = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.4, 0.4), darkOakTrimMat);
      portalLintel.position.set(0, 3.7, dz);
      scene.add(portalLintel);

      // Left blast door (permanently sealed)
      const doorL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 3.2, 2.0), lockedDoorMat);
      doorL.position.set(-2.0, 1.6, dz);
      doorL.rotation.y = 0.25;
      scene.add(doorL);

      // Right blast door (permanently sealed)
      const doorR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 3.2, 2.0), lockedDoorMat);
      doorR.position.set(2.0, 1.6, dz);
      doorR.rotation.y = Math.PI - 0.25;
      scene.add(doorR);

      // Red status lock beacon
      const lockBeacon = new THREE.Mesh(
        new THREE.BoxGeometry(0.25, 0.15, 0.15),
        new THREE.MeshBasicMaterial({ color: 0xff2a4d })
      );
      lockBeacon.position.set(0, 3.4, dz);
      scene.add(lockBeacon);

      const pLight = new THREE.PointLight(0xff2a4d, 1.8, 5.0);
      pLight.position.set(0, 3.2, dz);
      scene.add(pLight);
      doorLights.push(pLight);

      const bayLight = new THREE.PointLight(0xff4422, 1.5, 4.0);
      bayLight.position.set(0, 1.5, dz);
      scene.add(bayLight);
    });

    // Distant Exit Portal Gateway at the end of corridor (Z = -9.5)
    const portalGlow = new THREE.Mesh(
      new THREE.BoxGeometry(3.6, 4.2, 0.2),
      new THREE.MeshBasicMaterial({ color: 0x00f0ff })
    );
    portalGlow.position.set(0, 2.0, -9.6);
    scene.add(portalGlow);

    const gatewayRim = new THREE.DirectionalLight(0x00f0ff, 2.2);
    gatewayRim.position.set(0, 4.0, -10.0);
    gatewayRim.target.position.set(0, 1.0, 0);
    scene.add(gatewayRim);
    scene.add(gatewayRim.target);

    scene.add(new THREE.AmbientLight(0x101a2e, 0.85));

    // Alex faces AWAY from screen into the scene (-Z)
    character.root.position.set(0, 0, 3.5);
    character.root.rotation.set(0, Math.PI, 0); // Back facing camera, facing toward gateway!
    character.root.visible = true;

    customUpdate = (t) => {
      // Alex marches forward away from screen down the runway
      character.setMarchForward(t);
      // Smooth continuous walk away along -Z
      character.root.position.z = 3.5 - (t * 0.75);

      // Lock beacons gentle pulse
      doorLights.forEach((light, idx) => {
        light.intensity = 1.0 + Math.sin(t * 5.0 + idx) * 0.4;
      });
    };
  }

  // =========================================================================
  // SCENE 17: NO NEGOTIATION AT 7:00 AM (Shot 17)
  // Script: "They do not negotiate with their feelings at seven in the morning."
  // 100% Consistent Bedroom: Exact same room as Clip 1/2.
  // Clock displays 07:00 AM. Camera side-angled showing Alex waking up & rising.
  // =========================================================================
  else if (shotId === 17) {
    buildStandardBedroom(scene, floorMat, darkOakTrimMat, whiteWoolMat, oakWallMat, {
      timeOfDay: "morning",
      clockTime: "07:00",
      clockPeriod: "AM",
      clockColor: "cyan",
      duvet: "folded",
      shoesPresent: true,
      phoneFaceDown: false,
    });

    // Alex seated on bed edge waking up and rising decisively
    character.root.position.set(0.20, 0.49, -0.45);
    character.root.rotation.set(0, 0, 0);
    character.root.visible = true;

    customUpdate = (t) => {
      // Alex wakes up and stands up with decisive 7:00 AM momentum
      character.setDecisiveRise(t);
    };
  }

  // =========================================================================
  // SCENE 18: THE WORKSPACE ALTAR (Shot 18)
  // =========================================================================
  else if (shotId === 18) {
    scene.background = new THREE.Color(0x0e131d); // Clean studio slate

    const darkSteelMat = new THREE.MeshStandardMaterial({
      color: 0x161b26,
      roughness: 0.4,
      metalness: 0.8,
    });
    const wallMat = new THREE.MeshToonMaterial({ color: 0x1b2230 });

    // Dark graphite studio floor
    const floor = new THREE.Mesh(new THREE.BoxGeometry(8, 0.2, 8), darkSteelMat);
    floor.position.y = -0.1;
    scene.add(floor);

    // Modern studio backdrop wall
    const wall = new THREE.Mesh(new THREE.BoxGeometry(8, 4.5, 0.2), wallMat);
    wall.position.set(0, 2.15, -2.5);
    scene.add(wall);

    // Group all desk elements into a unified 3/4 angled assembly
    const deskAssembly = new THREE.Group();
    deskAssembly.position.set(0, 0, -0.6);
    deskAssembly.rotation.y = -0.30; // 3/4 cinematic angle toward camera

    // Minimalist executive floating cantilever desk
    const deskTop = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.10, 1.3), oakWallMat);
    deskTop.position.set(0, 0.85, 0);
    deskAssembly.add(deskTop);

    // Sturdy matte black steel legs
    for (const dx of [-1.15, 1.15]) {
      const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.85, 1.1), darkOakTrimMat);
      leg.position.set(dx, 0.425, 0);
      deskAssembly.add(leg);
    }

    // Modern Ergonomic Mesh Chair behind Alex
    const chairBack = new THREE.Mesh(new THREE.BoxGeometry(0.70, 0.72, 0.08), darkOakTrimMat);
    chairBack.position.set(0, 0.86, 0.95);
    deskAssembly.add(chairBack);

    // Modern Ultra-Thin Voxel Laptop
    const laptopGroup = new THREE.Group();
    laptopGroup.position.set(0, 0.90, 0.05);

    // Laptop Base (keyboard body)
    const laptopBase = new THREE.Mesh(
      new THREE.BoxGeometry(0.82, 0.03, 0.56),
      new THREE.MeshStandardMaterial({ color: 0x181e2b, roughness: 0.3, metalness: 0.8 })
    );
    laptopGroup.add(laptopBase);

    // Trackpad
    const trackpad = new THREE.Mesh(
      new THREE.BoxGeometry(0.24, 0.032, 0.16),
      new THREE.MeshBasicMaterial({ color: 0x222a3a })
    );
    trackpad.position.set(0, 0.005, 0.16);
    laptopGroup.add(trackpad);

    // Display Lid (angled smoothly open at 105 degrees)
    const laptopScreenGroup = new THREE.Group();
    laptopScreenGroup.position.set(0, 0.015, -0.27);
    laptopScreenGroup.rotation.x = -0.24; // Angled backward for clear viewing

    const lidCover = new THREE.Mesh(
      new THREE.BoxGeometry(0.82, 0.54, 0.02),
      new THREE.MeshStandardMaterial({ color: 0x181e2b, roughness: 0.3, metalness: 0.8 })
    );
    lidCover.position.set(0, 0.27, 0);
    laptopScreenGroup.add(lidCover);

    // Active Prose/Code Screen with IDE Texture
    const ideTex = createLaptopIDETexture();
    const screenDisplay = new THREE.Mesh(
      new THREE.BoxGeometry(0.78, 0.50, 0.005),
      new THREE.MeshBasicMaterial({ map: ideTex })
    );
    screenDisplay.position.set(0, 0.27, 0.012);
    laptopScreenGroup.add(screenDisplay);

    laptopGroup.add(laptopScreenGroup);
    deskAssembly.add(laptopGroup);

    // Focused Cyan glow from the laptop screen illuminating Alex
    const screenGlow = new THREE.PointLight(0x00f0ff, 2.4, 3.2);
    screenGlow.position.set(0, 1.25, 0.2);
    deskAssembly.add(screenGlow);

    // Desk Accessories: Ceramic steam mug and minimalist plant
    const mug = new THREE.Mesh(
      new THREE.CylinderGeometry(0.08, 0.07, 0.14, 12),
      new THREE.MeshStandardMaterial({ color: 0xf5f5f5, roughness: 0.2 })
    );
    mug.position.set(0.72, 0.97, 0.15);
    deskAssembly.add(mug);

    const plantPot = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.18, 0.22), darkOakTrimMat);
    plantPot.position.set(-0.85, 0.99, -0.15);
    deskAssembly.add(plantPot);
    const plantLeaves = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.24, 0.26), leavesMat);
    plantLeaves.position.set(-0.85, 1.18, -0.15);
    deskAssembly.add(plantLeaves);

    scene.add(deskAssembly);

    // Studio Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.85));
    const overheadKey = new THREE.DirectionalLight(0xffeedd, 1.4);
    overheadKey.position.set(0, 4.0, 1.5);
    scene.add(overheadKey);

    // Alex seated at the desk typing with zero hesitation
    character.root.position.set(-0.05, 0, 0.05);
    character.root.rotation.y = -0.30;

    customUpdate = (t) => {
      character.setTyping(t);
      screenGlow.intensity = 2.0 + Math.sin(t * 12.0) * 0.25;
    };
  }

  // =========================================================================
  // SCENE 19: THE FRICTION BLUEPRINT (Shot 19)
  // =========================================================================
  else if (shotId === 19) {
    scene.background = new THREE.Color(0x050d18); // Deep architectural blueprint dark

    const darkSteelMat = new THREE.MeshStandardMaterial({
      color: 0x0c1420,
      roughness: 0.4,
      metalness: 0.8,
    });

    // Architectural cyan coordinate grid on floor
    const grid = new THREE.GridHelper(10, 20, 0x00f0ff, 0x0a3355);
    grid.position.y = 0.01;
    scene.add(grid);

    const ground = new THREE.Mesh(new THREE.BoxGeometry(10, 0.2, 10), darkSteelMat);
    ground.position.y = -0.1;
    scene.add(ground);

    // Central Holographic Drafting Table
    const tableBase = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.55, 0.85, 16), darkOakTrimMat);
    tableBase.position.set(0.6, 0.425, 0);
    scene.add(tableBase);

    const draftingTable = new THREE.Mesh(
      new THREE.BoxGeometry(2.6, 0.10, 2.0),
      new THREE.MeshStandardMaterial({ color: 0x0a1c30, roughness: 0.3, metalness: 0.7 })
    );
    draftingTable.position.set(0.6, 0.90, 0);
    draftingTable.rotation.x = 0.35; // Tilted toward camera so blueprint schematic is fully visible
    scene.add(draftingTable);

    // Projected Blueprint Schematic Surface
    const blueprintTex = createBlueprintSchematicTexture();
    const blueprintPlate = new THREE.Mesh(
      new THREE.BoxGeometry(2.4, 0.02, 1.8),
      new THREE.MeshBasicMaterial({ map: blueprintTex })
    );
    blueprintPlate.position.set(0.6, 0.96, 0.04);
    blueprintPlate.rotation.x = 0.35;
    scene.add(blueprintPlate);

    // Dedicated key light for the blueprint schematic
    const bpLight = new THREE.DirectionalLight(0x00f0ff, 2.0);
    bpLight.position.set(0.6, 3.5, 2.0);
    bpLight.target = blueprintPlate;
    scene.add(bpLight);

    // Glowing Holographic 3D Route Elements Floating Above Table
    const holoGroup = new THREE.Group();
    holoGroup.position.set(0.6, 1.25, 0);

    // Concentric rotating holographic rings
    const ringGeo1 = new THREE.RingGeometry(0.85, 0.90, 32);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.7,
    });
    const holoRing1 = new THREE.Mesh(ringGeo1, ringMat);
    holoRing1.rotation.x = Math.PI / 2;
    holoGroup.add(holoRing1);

    const ringGeo2 = new THREE.RingGeometry(1.2, 1.24, 32);
    const ringMat2 = new THREE.MeshBasicMaterial({
      color: 0xffcc00,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.5,
    });
    const holoRing2 = new THREE.Mesh(ringGeo2, ringMat2);
    holoRing2.rotation.x = Math.PI / 2;
    holoGroup.add(holoRing2);

    scene.add(holoGroup);

    // Holographic Point Lights
    const holoLight = new THREE.PointLight(0x00f0ff, 2.5, 4.5);
    holoLight.position.set(0.6, 1.6, 0);
    scene.add(holoLight);

    scene.add(new THREE.AmbientLight(0x0a1a2e, 0.9));
    const studioKey = new THREE.DirectionalLight(0xffffff, 1.2);
    studioKey.position.set(-2, 4, 3);
    scene.add(studioKey);

    // Marcus in Master navy & gold robes presenting the system
    const marcusMaster = new VoxelCharacter("Marcus");
    marcusMaster.root.position.set(-1.2, 0, 0.2);
    marcusMaster.root.rotation.y = 0.45; // Angled toward table
    scene.add(marcusMaster.root);

    // Remove the default character from scene
    scene.remove(character.root);

    customUpdate = (t) => {
      marcusMaster.setPresentingMaster(t);
      holoGroup.rotation.y = t * 0.4;
      holoRing1.rotation.z = t * 0.3;
      holoRing2.rotation.z = -t * 0.2;
      holoLight.intensity = 2.2 + Math.sin(t * 3.0) * 0.4;
    };
  }

  // =========================================================================
  // SCENE 20: TRIO OF FRICTION PEDESTALS (Shot 20)
  // =========================================================================
  else if (shotId === 20) {
    scene.background = new THREE.Color(0x0c111a);

    const darkSteelMat = new THREE.MeshStandardMaterial({
      color: 0x141822,
      roughness: 0.4,
      metalness: 0.8,
    });

    const ground = new THREE.Mesh(new THREE.BoxGeometry(14, 0.2, 8), darkSteelMat);
    ground.position.y = -0.1;
    scene.add(ground);

    // Modern architectural gallery back wall
    const galleryWallMat = new THREE.MeshToonMaterial({ color: 0x161d2a });
    const galleryWall = new THREE.Mesh(new THREE.BoxGeometry(14, 4.5, 0.2), galleryWallMat);
    galleryWall.position.set(0, 2.15, -2.5);
    scene.add(galleryWall);

    // Three architectural display pedestals
    // -----------------------------------------------------------------------
    // PEDESTAL 1 (Left, x = -2.7): "Phone in another room"
    // -----------------------------------------------------------------------
    const ped1 = new THREE.Mesh(
      new THREE.CylinderGeometry(0.65, 0.75, 0.85, 20),
      new THREE.MeshStandardMaterial({ color: 0x1c2331, roughness: 0.3, metalness: 0.7 })
    );
    ped1.position.set(-2.7, 0.425, 0);
    scene.add(ped1);

    // Heavy Titanium Isolation Vault Box with Glass Beveled Window
    const vaultBox = new THREE.Mesh(
      new THREE.BoxGeometry(0.60, 0.22, 0.50),
      new THREE.MeshStandardMaterial({ color: 0x121720, roughness: 0.2, metalness: 0.9 })
    );
    vaultBox.position.set(-2.7, 0.96, 0);
    scene.add(vaultBox);

    // Smartphone resting inside locked vault with screen active (tilted toward camera)
    const phoneTex = createPhoneLockedTexture();
    const phoneScreen = new THREE.Mesh(
      new THREE.BoxGeometry(0.24, 0.02, 0.44),
      new THREE.MeshBasicMaterial({ map: phoneTex })
    );
    phoneScreen.position.set(-2.7, 1.10, 0.05);
    phoneScreen.rotation.x = -0.45;
    scene.add(phoneScreen);

    // Pedestal 1 Dedicated Spotlight
    const spot1 = new THREE.SpotLight(0x00f0ff, 2.8, 8.0, 0.45, 0.5);
    spot1.position.set(-2.7, 4.5, 0);
    spot1.target.position.set(-2.7, 1.0, 0);
    scene.add(spot1);
    scene.add(spot1.target);

    // -----------------------------------------------------------------------
    // PEDESTAL 2 (Center, x = 0.0): "Shoes directly by doorway"
    // -----------------------------------------------------------------------
    const ped2 = new THREE.Mesh(
      new THREE.BoxGeometry(1.6, 0.85, 1.2),
      floorMat
    );
    ped2.position.set(0.0, 0.425, 0);
    scene.add(ped2);

    // Miniature Doorway Threshold Frame
    const doorFrameL = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.4, 0.12), darkOakTrimMat);
    doorFrameL.position.set(-0.65, 1.55, -0.3);
    scene.add(doorFrameL);
    const doorFrameR = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.4, 0.12), darkOakTrimMat);
    doorFrameR.position.set(0.65, 1.55, -0.3);
    scene.add(doorFrameR);
    const doorFrameTop = new THREE.Mesh(new THREE.BoxGeometry(1.42, 0.12, 0.12), darkOakTrimMat);
    doorFrameTop.position.set(0, 2.25, -0.3);
    scene.add(doorFrameTop);

    // Running Shoes poised right at threshold
    const shoeMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, roughness: 0.3 });
    const soleMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const laceMat = new THREE.MeshBasicMaterial({ color: 0xffaa00 });

    const createShoe = (sx: number) => {
      const g = new THREE.Group();
      g.position.set(sx, 0.85, 0.1);
      // Sole
      const sole = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.05, 0.44), soleMat);
      sole.position.set(0, 0.025, 0);
      g.add(sole);
      // Body
      const body = new THREE.Mesh(new THREE.BoxGeometry(0.17, 0.12, 0.42), shoeMat);
      body.position.set(0, 0.11, 0);
      g.add(body);
      // Tongue & Laces
      const laces = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.04, 0.18), laceMat);
      laces.position.set(0, 0.17, 0.05);
      g.add(laces);
      return g;
    };

    const shoeLeft = createShoe(-0.16);
    const shoeRight = createShoe(0.16);
    scene.add(shoeLeft);
    scene.add(shoeRight);

    // Pedestal 2 Dedicated Spotlight (Golden morning doorway light)
    const spot2 = new THREE.SpotLight(0xffb74d, 2.8, 8.0, 0.45, 0.5);
    spot2.position.set(0.0, 4.5, 0);
    spot2.target.position.set(0.0, 1.0, 0);
    scene.add(spot2);
    scene.add(spot2.target);

    // -----------------------------------------------------------------------
    // PEDESTAL 3 (Right, x = +2.7): "Blank document open before bed"
    // -----------------------------------------------------------------------
    const ped3 = new THREE.Mesh(
      new THREE.CylinderGeometry(0.65, 0.75, 0.85, 20),
      new THREE.MeshStandardMaterial({ color: 0x1c2331, roughness: 0.3, metalness: 0.7 })
    );
    ped3.position.set(2.7, 0.425, 0);
    scene.add(ped3);

    // Laptop Stand & Laptop with Blank Document
    const laptopStand = new THREE.Mesh(
      new THREE.BoxGeometry(0.40, 0.12, 0.32),
      darkOakTrimMat
    );
    laptopStand.position.set(2.7, 0.91, 0);
    scene.add(laptopStand);

    const docGroup = new THREE.Group();
    docGroup.position.set(2.7, 0.97, 0);

    const lapBase = new THREE.Mesh(
      new THREE.BoxGeometry(0.68, 0.025, 0.46),
      new THREE.MeshStandardMaterial({ color: 0x222834, roughness: 0.3, metalness: 0.8 })
    );
    docGroup.add(lapBase);

    // Angled screen displaying blank doc
    const lapLid = new THREE.Group();
    lapLid.position.set(0, 0.012, -0.22);
    lapLid.rotation.x = -0.22;

    const lidMat = new THREE.MeshStandardMaterial({ color: 0x222834, roughness: 0.3, metalness: 0.8 });
    const lidBack = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.46, 0.02), lidMat);
    lidBack.position.set(0, 0.23, 0);
    lapLid.add(lidBack);

    const docTex = createBlankDocTexture();
    const docScreenMesh = new THREE.Mesh(
      new THREE.BoxGeometry(0.64, 0.42, 0.005),
      new THREE.MeshBasicMaterial({ map: docTex })
    );
    docScreenMesh.position.set(0, 0.23, 0.011);
    lapLid.add(docScreenMesh);

    docGroup.add(lapLid);
    scene.add(docGroup);

    // Pedestal 3 Dedicated Spotlight (Focused reading beam)
    const spot3 = new THREE.SpotLight(0xffffff, 2.8, 8.0, 0.45, 0.5);
    spot3.position.set(2.7, 4.5, 0);
    spot3.target.position.set(2.7, 1.0, 0);
    scene.add(spot3);
    scene.add(spot3.target);

    // Ambient gallery lighting
    scene.add(new THREE.AmbientLight(0xffffff, 1.15));

    // Marcus positioned as master curator presenting the trio of pedestals
    const marcusCurator = new VoxelCharacter("Marcus");
    marcusCurator.root.position.set(2.2, 0, -1.5);
    marcusCurator.root.rotation.y = -0.45; // Facing across toward the exhibits and viewer
    scene.add(marcusCurator.root);

    // Remove the default Alex character
    scene.remove(character.root);

    customUpdate = (t) => {
      // Dynamic presentation: Marcus gestures across the pedestals
      marcusCurator.setPresentingMaster(t);

      // Light choreography synced with narrative audio beats:
      if (t < 2.5) {
        spot1.intensity = 3.2;
        spot2.intensity = 1.0;
        spot3.intensity = 1.0;
      } else if (t < 5.0) {
        spot1.intensity = 1.0;
        spot2.intensity = 3.2;
        spot3.intensity = 1.0;
      } else {
        spot1.intensity = 1.2;
        spot2.intensity = 1.2;
        spot3.intensity = 3.2;
      }
    };
  }

  // =========================================================================
  // SCENE 21: THE BOULDER VS THE RIVERBED (Shot 21)
  // =========================================================================
  // =========================================================================
  // SCENE 21: THE BOULDER VS THE RIVERBED (Shot 21)
  // =========================================================================
  else if (shotId === 21) {
    scene.background = new THREE.Color(0x7eaec8); // Mountain sky horizon

    const mountainRockMat = new THREE.MeshToonMaterial({ color: 0x4a3c30 });
    const mudPathMat = new THREE.MeshStandardMaterial({ color: 0x36281c, roughness: 0.9 });
    const riverBankMat = new THREE.MeshStandardMaterial({ color: 0x546250, roughness: 0.7 });

    // Wide terrain base
    const terrainBase = new THREE.Mesh(new THREE.BoxGeometry(16, 0.2, 10), darkOakTrimMat);
    terrainBase.position.y = -0.1;
    scene.add(terrainBase);

    // -----------------------------------------------------------------------
    // LEFT SIDE: The Muddy Hill & The Giant Boulder
    // -----------------------------------------------------------------------
    const mudHillGroup = new THREE.Group();
    mudHillGroup.position.set(-3.6, 0, 0);

    // Steep incline slope
    const hillSlope = new THREE.Mesh(new THREE.BoxGeometry(5.5, 3.2, 8.0), mudPathMat);
    hillSlope.position.set(-0.5, 0.8, 0);
    hillSlope.rotation.z = -0.32; // Steep uphill
    mudHillGroup.add(hillSlope);

    // Rugged mountain rock outcroppings
    const rockGeo = new THREE.DodecahedronGeometry(0.7, 1);
    for (const [rx, ry, rz] of [[-2.2, 1.9, -1.5], [-2.4, 2.2, 1.2], [-1.0, 1.1, -2.4], [-0.8, 0.8, 2.2]]) {
      const rock = new THREE.Mesh(rockGeo, mountainRockMat);
      rock.position.set(rx, ry, rz);
      rock.rotation.set(rx, ry, rz);
      mudHillGroup.add(rock);
    }

    // The Colossal 1.8m Grey Granite Boulder
    const boulderGeo = new THREE.DodecahedronGeometry(1.4, 2);
    const boulderMat = new THREE.MeshStandardMaterial({
      color: 0x484e59,
      roughness: 0.85,
      metalness: 0.1,
    });
    const boulder = new THREE.Mesh(boulderGeo, boulderMat);
    boulder.position.set(-1.2, 1.7, 0);
    mudHillGroup.add(boulder);

    scene.add(mudHillGroup);

    // -----------------------------------------------------------------------
    // CENTER DIVIDER: Natural Granite Ridge
    // -----------------------------------------------------------------------
    const ridge = new THREE.Mesh(
      new THREE.BoxGeometry(1.2, 2.4, 8.0),
      mountainRockMat
    );
    ridge.position.set(-0.6, 0.8, 0);
    scene.add(ridge);

    // -----------------------------------------------------------------------
    // RIGHT SIDE: The Carved Riverbed & Effortless Flow
    // -----------------------------------------------------------------------
    const riverGroup = new THREE.Group();
    riverGroup.position.set(3.4, 0, 0);

    // Smooth carved riverbed bank
    const bankL = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.6, 8.0), riverBankMat);
    bankL.position.set(-2.0, 0.2, 0);
    riverGroup.add(bankL);

    const bankR = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.6, 8.0), riverBankMat);
    bankR.position.set(2.0, 0.2, 0);
    riverGroup.add(bankR);

    // Polished smooth river stones along banks
    const pebbleGeo = new THREE.DodecahedronGeometry(0.28, 1);
    const pebbleMat = new THREE.MeshStandardMaterial({ color: 0x7c8a99, roughness: 0.3 });
    for (let pz = -3.5; pz <= 3.5; pz += 1.2) {
      const p1 = new THREE.Mesh(pebbleGeo, pebbleMat);
      p1.position.set(-1.3, 0.32, pz + Math.sin(pz) * 0.3);
      riverGroup.add(p1);
      const p2 = new THREE.Mesh(pebbleGeo, pebbleMat);
      p2.position.set(1.3, 0.32, pz - Math.cos(pz) * 0.3);
      riverGroup.add(p2);
    }

    // Flowing Crystalline River Water
    const riverWaterMat = new THREE.MeshStandardMaterial({
      color: 0x00d4ff,
      roughness: 0.15,
      metalness: 0.2,
      transparent: true,
      opacity: 0.85,
    });
    const river = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.22, 8.2), riverWaterMat);
    river.position.set(0, 0.15, 0);
    riverGroup.add(river);

    // River foam / current lines
    const foamMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const foamLines: THREE.Mesh[] = [];
    for (let fz = -3.0; fz <= 3.0; fz += 1.5) {
      const foam = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.23, 0.12), foamMat);
      foam.position.set(0, 0.16, fz);
      riverGroup.add(foam);
      foamLines.push(foam);
    }

    scene.add(riverGroup);

    // Mountain Lighting: High golden sun
    const mountainSun = new THREE.DirectionalLight(0xfffaec, 2.2);
    mountainSun.position.set(4, 9, 5);
    mountainSun.target.position.set(0, 1, 0);
    scene.add(mountainSun);
    scene.add(mountainSun.target);

    scene.add(new THREE.AmbientLight(0xdde9f5, 0.95));

    // Left: Alex straining to push boulder
    character.root.position.set(-3.8, 0.9, 0.3);
    character.root.rotation.y = -Math.PI / 2 + 0.35; // Pushing up the slope

    // Right: Marcus standing serenely by riverbank
    const marcusRiver = new VoxelCharacter("Marcus");
    marcusRiver.root.position.set(4.8, 0.3, 0.5);
    marcusRiver.root.rotation.y = -0.4;
    scene.add(marcusRiver.root);

    const fzBase = (idx: number): number => -3.0 + idx * 1.5;

    customUpdate = (t) => {
      character.setPushingBoulder(t);
      marcusRiver.setStandingMentor(t);

      // Micro-tremor strain on boulder
      boulder.position.x = -1.2 + Math.sin(t * 14.0) * 0.015;

      // Flowing river current animation
      foamLines.forEach((foam, idx) => {
        foam.position.z = ((fzBase(idx) + t * 2.2) % 6.0) - 3.0;
      });
    };
  }

  // =========================================================================
  // SCENE 22: THE BROKEN TROPHY (Shot 22)
  // =========================================================================
  else if (shotId === 22) {
    scene.background = new THREE.Color(0x130d17); // Moody Friday burnout dusk

    const darkSlateMat = new THREE.MeshStandardMaterial({
      color: 0x18141d,
      roughness: 0.6,
      metalness: 0.4,
    });
    const goldMat = new THREE.MeshStandardMaterial({
      color: 0xd4af37,
      roughness: 0.25,
      metalness: 0.9,
    });
    const darkMarbleMat = new THREE.MeshStandardMaterial({
      color: 0x221a28,
      roughness: 0.3,
      metalness: 0.6,
    });

    // Dark studio loft floor
    const floor = new THREE.Mesh(new THREE.BoxGeometry(10, 0.2, 8), darkSlateMat);
    floor.position.y = -0.1;
    scene.add(floor);

    // Industrial rear wall with tall dusk windows
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(10, 4.5, 0.2), darkMarbleMat);
    backWall.position.set(0, 2.15, -3.2);
    scene.add(backWall);

    // High dusk window glowing dull burnt amber
    const duskWindow = new THREE.Mesh(
      new THREE.BoxGeometry(3.6, 2.4, 0.05),
      new THREE.MeshBasicMaterial({ color: 0x662a1a })
    );
    duskWindow.position.set(0, 2.6, -3.1);
    scene.add(duskWindow);

    // Central Fallen Monument Pedestal
    const pedestal = new THREE.Mesh(
      new THREE.BoxGeometry(1.4, 0.75, 1.4),
      darkMarbleMat
    );
    pedestal.position.set(0, 0.375, -0.4);
    scene.add(pedestal);

    // Etched Brass Plaque: "HEROIC WEEK: FAILED — DIED OF BURNOUT"
    const plaqueTex = createBrokenTrophyPlaqueTexture();
    const plaque = new THREE.Mesh(
      new THREE.BoxGeometry(0.85, 0.35, 0.02),
      new THREE.MeshBasicMaterial({ map: plaqueTex })
    );
    plaque.position.set(0, 0.38, 0.32);
    scene.add(plaque);

    // Shattered Golden Trophy Cup on top of pedestal and scattered on floor
    // Severed base on pedestal
    const trophyBase = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.45, 0.15, 16), goldMat);
    trophyBase.position.set(0, 0.82, -0.4);
    scene.add(trophyBase);

    // Broken trophy stem sheared off
    const brokenStem = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.12, 0.22, 12), goldMat);
    brokenStem.position.set(0.06, 0.96, -0.4);
    brokenStem.rotation.z = 0.45;
    scene.add(brokenStem);

    // Shattered Main Cup fallen onto floor
    const brokenCup1 = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.25, 0.55, 12, 1, true, 0, Math.PI), goldMat);
    brokenCup1.position.set(-0.75, 0.28, 0.3);
    brokenCup1.rotation.set(1.2, 0.3, -0.8);
    scene.add(brokenCup1);

    const brokenCup2 = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.25, 0.55, 12, 1, true, Math.PI, Math.PI), goldMat);
    brokenCup2.position.set(-0.35, 0.24, 0.6);
    brokenCup2.rotation.set(-0.9, -0.4, 0.6);
    scene.add(brokenCup2);

    // Severed golden handles
    const handleL = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.04, 8, 16, Math.PI), goldMat);
    handleL.position.set(-1.05, 0.12, 0.15);
    handleL.rotation.x = Math.PI / 2;
    scene.add(handleL);

    // Scattered gold trophy shards across the floor
    const shardGeo = new THREE.DodecahedronGeometry(0.08, 0);
    const shardPositions = [
      [-0.9, 0.04, 0.7], [-0.5, 0.04, 0.9], [0.4, 0.04, 0.6],
      [0.6, 0.04, 0.3], [-0.2, 0.04, 0.85], [-0.7, 0.04, -0.1]
    ];
    shardPositions.forEach(([sx, sy, sz]) => {
      const sh = new THREE.Mesh(shardGeo, goldMat);
      sh.position.set(sx, sy, sz);
      sh.rotation.set(sx * 3, sy * 2, sz * 4);
      scene.add(sh);
    });

    // Crumpled planning sheets & exhausted debris
    const paperMat = new THREE.MeshToonMaterial({ color: 0xdedede });
    for (const [px, pz] of [[0.9, 0.2], [-1.2, 0.8], [0.3, 1.1]]) {
      const crumpled = new THREE.Mesh(new THREE.DodecahedronGeometry(0.12, 1), paperMat);
      crumpled.position.set(px, 0.08, pz);
      scene.add(crumpled);
    }

    // Somber Dusk Lighting: Low-angle burnt amber rim
    const duskRim = new THREE.DirectionalLight(0xff5522, 2.0);
    duskRim.position.set(0, 4, -5);
    duskRim.target.position.set(0, 0.5, 0);
    scene.add(duskRim);
    scene.add(duskRim.target);

    // Dedicated cool key light for Alex and the plaque
    const studioKey = new THREE.DirectionalLight(0xd0d8e8, 1.2);
    studioKey.position.set(3, 4, 3);
    scene.add(studioKey);

    scene.add(new THREE.AmbientLight(0x2a1c32, 0.85));

    // Alex collapsed on knees beside the trophy in complete exhaustion
    character.root.position.set(0.95, 0, 0.25);
    character.root.rotation.y = -0.65; // Angled toward the shattered trophy

    customUpdate = (t) => {
      character.setCollapsedBurnout(t);
    };
  }

  // =========================================================================
  // SCENE 23: THE SHRINKING HURDLE (Shot 23)
  // =========================================================================
  else if (shotId === 23) {
    scene.background = new THREE.Color(0xf3f5f8); // High-key clean white studio

    // Polished light ash track floor
    const floor = new THREE.Mesh(new THREE.BoxGeometry(10, 0.2, 8), floorMat);
    floor.position.y = -0.1;
    scene.add(floor);

    // Track lane markings
    const lineMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    for (const lx of [-2.4, 0.0, 2.4]) {
      const line = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.22, 8.0), lineMat);
      line.position.set(lx, -0.09, 0);
      scene.add(line);
    }

    // -----------------------------------------------------------------------
    // LEFT LANE: The Impassable 3.5m "Exhaustion Wall" (Bypassed)
    // -----------------------------------------------------------------------
    const wallMat = new THREE.MeshStandardMaterial({
      color: 0x1a212d,
      roughness: 0.5,
      metalness: 0.7,
    });
    const giantWall = new THREE.Mesh(new THREE.BoxGeometry(2.2, 3.8, 0.4), wallMat);
    giantWall.position.set(-1.4, 1.9, 0);
    scene.add(giantWall);

    // Red warning stripe lintel on top of wall
    const hazardStripe = new THREE.Mesh(
      new THREE.BoxGeometry(2.24, 0.25, 0.42),
      new THREE.MeshBasicMaterial({ color: 0xff2a4d })
    );
    hazardStripe.position.set(-1.4, 3.7, 0);
    scene.add(hazardStripe);

    const wallLabelBeacon = new THREE.PointLight(0xff2a4d, 1.6, 3.0);
    wallLabelBeacon.position.set(-1.4, 2.8, 0.4);
    scene.add(wallLabelBeacon);

    // -----------------------------------------------------------------------
    // RIGHT LANE: The Tiny 2-Inch Hurdle
    // -----------------------------------------------------------------------
    const hurdleGroup = new THREE.Group();
    hurdleGroup.position.set(1.2, 0, 0);

    // Tiny 5cm high hurdle posts
    const postMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff });
    const postL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.10, 0.04), postMat);
    postL.position.set(-0.65, 0.05, 0);
    hurdleGroup.add(postL);

    const postR = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.10, 0.04), postMat);
    postR.position.set(0.65, 0.05, 0);
    hurdleGroup.add(postR);

    // Tiny 2-inch crossbar
    const crossbar = new THREE.Mesh(new THREE.BoxGeometry(1.34, 0.04, 0.04), postMat);
    crossbar.position.set(0, 0.08, 0);
    hurdleGroup.add(crossbar);

    // Base feet
    const footL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.02, 0.22), darkOakTrimMat);
    footL.position.set(-0.65, 0.01, 0);
    hurdleGroup.add(footL);
    const footR = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.02, 0.22), darkOakTrimMat);
    footR.position.set(0.65, 0.01, 0);
    hurdleGroup.add(footR);

    // Floating Holographic Sign above the hurdle: "BARRIER HEIGHT: 2 INCHES // RESISTANCE: RIDICULOUS"
    const signTex = createTinyHurdleSignTexture();
    const signMesh = new THREE.Mesh(
      new THREE.BoxGeometry(1.5, 0.62, 0.02),
      new THREE.MeshBasicMaterial({ map: signTex })
    );
    signMesh.position.set(0, 1.45, 0);
    hurdleGroup.add(signMesh);

    // Cyan glowing indicator light for hurdle lane
    const hurdleGlow = new THREE.PointLight(0x00f0ff, 2.2, 3.5);
    hurdleGlow.position.set(0, 0.8, 0.3);
    hurdleGroup.add(hurdleGlow);

    scene.add(hurdleGroup);

    // Crisp High-Key Lighting
    const keySun = new THREE.DirectionalLight(0xfffaec, 2.0);
    keySun.position.set(2, 6, 4);
    scene.add(keySun);

    scene.add(new THREE.AmbientLight(0xffffff, 1.1));

    // Alex poised right over the tiny 2-inch hurdle, stepping across casually
    character.root.position.set(1.2, 0, 0);

    customUpdate = (t) => {
      character.setSteppingHurdle(t);
      signMesh.position.y = 1.45 + Math.sin(t * 3.0) * 0.03;
    };
  }

  // =========================================================================
  // SCENE 24: TRIO OF ACTIONS (Shot 24)
  // =========================================================================
  else if (shotId === 24) {
    scene.background = new THREE.Color(0xf2efe9); // Warm architectural white

    // Unified wooden studio flooring
    const floor = new THREE.Mesh(new THREE.BoxGeometry(12, 0.2, 8), floorMat);
    floor.position.y = -0.1;
    scene.add(floor);

    // Modern studio rear wall
    const wall = new THREE.Mesh(
      new THREE.BoxGeometry(12, 4.5, 0.2),
      new THREE.MeshToonMaterial({ color: 0xe8e4dc })
    );
    wall.position.set(0, 2.15, -2.8);
    scene.add(wall);

    // -----------------------------------------------------------------------
    // ZONE 1 (Left, x = -3.0): "Sit in the chair for two minutes"
    // -----------------------------------------------------------------------
    const zone1Group = new THREE.Group();
    zone1Group.position.set(-3.0, 0, 0);

    const chairMesh = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.82, 0.80), darkOakTrimMat);
    chairMesh.position.set(0, 0.41, 0);
    zone1Group.add(chairMesh);

    const cushion = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.12, 0.70), new THREE.MeshToonMaterial({ color: 0x1f2e46 }));
    cushion.position.set(0, 0.47, 0);
    zone1Group.add(cushion);

    const chairBack = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.75, 0.10), new THREE.MeshToonMaterial({ color: 0x1f2e46 }));
    chairBack.position.set(0, 0.90, -0.35);
    zone1Group.add(chairBack);

    // Dedicated warm spotlight for chair
    const spotZone1 = new THREE.SpotLight(0xffeedd, 2.5, 6.0, 0.4, 0.4);
    spotZone1.position.set(0, 4.0, 0);
    zone1Group.add(spotZone1);

    scene.add(zone1Group);

    // -----------------------------------------------------------------------
    // ZONE 2 (Center, x = 0.0): "Write one clean paragraph"
    // -----------------------------------------------------------------------
    const zone2Group = new THREE.Group();
    zone2Group.position.set(0.0, 0, 0);

    const deskTop = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.08, 1.1), oakWallMat);
    deskTop.position.set(0, 0.85, 0);
    zone2Group.add(deskTop);

    for (const dx of [-0.8, 0.8]) {
      const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.85, 0.9), darkOakTrimMat);
      leg.position.set(dx, 0.425, 0);
      zone2Group.add(leg);
    }

    // Open Linen Notebook with handwritten clean paragraph
    const notebookTex = createTwoMinuteNotebookTexture();
    const notebook = new THREE.Mesh(
      new THREE.BoxGeometry(0.68, 0.03, 0.68),
      new THREE.MeshBasicMaterial({ map: notebookTex })
    );
    notebook.position.set(0, 0.90, 0.05);
    zone2Group.add(notebook);

    // Fountain pen resting beside notebook
    const pen = new THREE.Mesh(
      new THREE.CylinderGeometry(0.015, 0.015, 0.28),
      new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.9, roughness: 0.2 })
    );
    pen.position.set(0.42, 0.90, 0.05);
    pen.rotation.z = Math.PI / 4;
    zone2Group.add(pen);

    scene.add(zone2Group);

    // -----------------------------------------------------------------------
    // ZONE 3 (Right, x = +3.0): "Put on the sneakers and step outside"
    // -----------------------------------------------------------------------
    const zone3Group = new THREE.Group();
    zone3Group.position.set(3.0, 0, 0);

    // Architectural Doorway to the Morning Outside
    const doorFrameL = new THREE.Mesh(new THREE.BoxGeometry(0.14, 2.8, 0.14), darkOakTrimMat);
    doorFrameL.position.set(-0.75, 1.4, 0);
    zone3Group.add(doorFrameL);
    const doorFrameR = new THREE.Mesh(new THREE.BoxGeometry(0.14, 2.8, 0.14), darkOakTrimMat);
    doorFrameR.position.set(0.75, 1.4, 0);
    zone3Group.add(doorFrameR);
    const doorFrameTop = new THREE.Mesh(new THREE.BoxGeometry(1.64, 0.14, 0.14), darkOakTrimMat);
    doorFrameTop.position.set(0, 2.8, 0);
    zone3Group.add(doorFrameTop);

    // Radiant Morning Sunbeam pouring through doorway
    const outsideLight = new THREE.DirectionalLight(0xffeedd, 2.5);
    outsideLight.position.set(3.0, 4.5, -3.0);
    outsideLight.target.position.set(3.0, 1.0, 1.0);
    scene.add(outsideLight);
    scene.add(outsideLight.target);

    // Pair of turquoise running sneakers right by doorway
    const shoeMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, roughness: 0.3 });
    const soleMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const makeSneaker = (sx: number) => {
      const g = new THREE.Group();
      g.position.set(sx, 0.0, 0.3);
      const sole = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.04, 0.38), soleMat);
      sole.position.set(0, 0.02, 0);
      g.add(sole);
      const upper = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.10, 0.36), shoeMat);
      upper.position.set(0, 0.09, 0);
      g.add(upper);
      return g;
    };
    zone3Group.add(makeSneaker(-0.18));
    zone3Group.add(makeSneaker(0.18));

    scene.add(zone3Group);

    scene.add(new THREE.AmbientLight(0xffffff, 1.0));

    // Multi-Beat Dynamic Character Routing
    character.root.position.set(-3.0, 0, 0);

    customUpdate = (t) => {
      // 3 Beats (0-3s, 3-6s, 6-9s):
      if (t < 3.0) {
        // Beat 1: Seated peacefully in the chair
        character.root.position.set(-3.0, 0, 0);
        character.root.rotation.y = 0;
        character.setSittingProud(t);
      } else if (t < 6.0) {
        // Beat 2: At desk writing one clean paragraph
        character.root.position.set(0, 0, 0.6);
        character.root.rotation.y = 0;
        character.setTyping(t);
      } else {
        // Beat 3: Stepping out the door into the world
        character.root.position.set(3.0, 0, (t - 6.0) * 0.4);
        character.root.rotation.y = 0;
        character.setMarchForward(t);
      }
    };
  }

  // =========================================================================
  // SCENE 25: THE IDENTITY LEDGER & GOLDEN SCALE (Shot 25)
  // =========================================================================
  else if (shotId === 25) {
    scene.background = new THREE.Color(0xffdeb8); // Radiant golden sunrise horizon

    const cliffMat = new THREE.MeshStandardMaterial({ color: 0x5a483a, roughness: 0.8 });
    const polishedGoldMat = new THREE.MeshStandardMaterial({
      color: 0xffd700,
      roughness: 0.2,
      metalness: 0.9,
    });
    const oldInertiaMat = new THREE.MeshStandardMaterial({
      color: 0x2a323d,
      roughness: 0.8,
      metalness: 0.3,
    });

    // Summit Promontory overlooking golden dawn
    const cliff = new THREE.Mesh(new THREE.BoxGeometry(10, 2.0, 8), cliffMat);
    cliff.position.set(0, -0.4, 0);
    scene.add(cliff);

    // Stone plinth for the Golden Scale
    const scalePlinth = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.5, 1.4), darkOakTrimMat);
    scalePlinth.position.set(0.6, 0.85, 0);
    scene.add(scalePlinth);

    // -----------------------------------------------------------------------
    // THE MONUMENTAL GOLDEN BALANCE SCALE
    // -----------------------------------------------------------------------
    const scaleGroup = new THREE.Group();
    scaleGroup.position.set(0.6, 1.1, 0);

    // Ornate Golden Base
    const scaleBase = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, 0.15, 20), polishedGoldMat);
    scaleBase.position.y = 0.08;
    scaleGroup.add(scaleBase);

    // Main Vertical Column
    const scalePillar = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 1.8, 16), polishedGoldMat);
    scalePillar.position.y = 0.98;
    scaleGroup.add(scalePillar);

    // Pivot Fulcrum Sphere
    const fulcrum = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), polishedGoldMat);
    fulcrum.position.y = 1.88;
    scaleGroup.add(fulcrum);

    // Pivoting Balance Crossbeam
    const scaleBeamGroup = new THREE.Group();
    scaleBeamGroup.position.y = 1.88;

    const crossbeam = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.06, 0.06), polishedGoldMat);
    scaleBeamGroup.add(crossbeam);

    // Left Pan (Old Inertia)
    const panLeftGroup = new THREE.Group();
    panLeftGroup.position.set(-1.0, -0.5, 0);
    const leftPlate = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.30, 0.04, 16), polishedGoldMat);
    panLeftGroup.add(leftPlate);
    const chainL = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.5, 0.02), polishedGoldMat);
    chainL.position.set(0, 0.25, 0);
    panLeftGroup.add(chainL);

    // Heavy dark block of "OLD INERTIA" on left pan
    const oldWeight = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.32, 0.38), oldInertiaMat);
    oldWeight.position.set(0, 0.18, 0);
    panLeftGroup.add(oldWeight);

    scaleBeamGroup.add(panLeftGroup);

    // Right Pan (New Identity / Small Vote)
    const panRightGroup = new THREE.Group();
    panRightGroup.position.set(1.0, -0.5, 0);
    const rightPlate = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.30, 0.04, 16), polishedGoldMat);
    panRightGroup.add(rightPlate);
    const chainR = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.5, 0.02), polishedGoldMat);
    chainR.position.set(0, 0.25, 0);
    panRightGroup.add(chainR);

    // Radiant Golden Embossed Coin: "ONE SMALL VOTE"
    const coinTex = createGoldenScaleCoinTexture();
    const goldenCoin = new THREE.Mesh(
      new THREE.CylinderGeometry(0.18, 0.18, 0.04, 20),
      new THREE.MeshBasicMaterial({ map: coinTex })
    );
    goldenCoin.position.set(0, 0.08, 0);
    goldenCoin.rotation.x = Math.PI / 2;
    panRightGroup.add(goldenCoin);

    scaleBeamGroup.add(panRightGroup);
    scaleGroup.add(scaleBeamGroup);

    scene.add(scaleGroup);

    // Golden Particle Sparkle Point Light at the Right Pan
    const coinGlow = new THREE.PointLight(0xffd700, 3.2, 4.0);
    coinGlow.position.set(1.6, 2.4, 0);
    scene.add(coinGlow);

    // Majestic Golden Sunrise Directional Light
    const sunriseSun = new THREE.DirectionalLight(0xffa726, 2.6);
    sunriseSun.position.set(2, 6, -8);
    sunriseSun.target.position.set(0, 1.5, 0);
    scene.add(sunriseSun);
    scene.add(sunriseSun.target);

    scene.add(new THREE.AmbientLight(0xffecc8, 0.95));

    // Alex poised dropping the golden vote coin
    character.root.position.set(-0.6, 0.75, 0.3);

    // Marcus standing proudly at left crest witnessing the triumph
    const marcusSummit = new VoxelCharacter("Marcus");
    marcusSummit.root.position.set(-2.2, 0.75, -0.4);
    marcusSummit.root.rotation.y = 0.35;
    scene.add(marcusSummit.root);

    customUpdate = (t) => {
      character.setDroppingCoin(t);
      marcusSummit.setStandingMentor(t);

      // Scale tipping physics synced with coin drop (at t = 2.4s):
      if (t < 2.0) {
        // Weighed down on the left by old inertia
        scaleBeamGroup.rotation.z = -0.15 + Math.sin(t * 1.5) * 0.02;
      } else if (t < 3.2) {
        // Tipping decisively down to the right!
        const tipP = (t - 2.0) / 1.2;
        const easeTip = tipP * tipP * (3 - 2 * tipP);
        scaleBeamGroup.rotation.z = -0.15 + 0.35 * easeTip;
        coinGlow.intensity = 3.0 + Math.sin(t * 10.0) * 1.5;
      } else {
        // Locked in triumph on the right (new identity wins!)
        scaleBeamGroup.rotation.z = 0.20 + Math.sin(t * 1.0) * 0.01;
        coinGlow.intensity = 3.5;
      }
    };
  }

  // =========================================================================
  // DEFAULT MENTOR STAGE
  // =========================================================================
  else {
    scene.background = new THREE.Color(0x10141e);
    const ground = new THREE.Mesh(new THREE.BoxGeometry(8, 0.2, 8), floorMat);
    ground.position.y = -0.1;
    scene.add(ground);

    scene.add(new THREE.AmbientLight(0xffffff, 1.0));
    character.root.position.set(0, 0, 0);
    customUpdate = (t) => {
      character.setStandingMentor(t);
    };
  }

  return {
    scene,
    character,
    update: (time: number, camera?: THREE.PerspectiveCamera) => {
      customUpdate(time, camera);
    },
  };
}
