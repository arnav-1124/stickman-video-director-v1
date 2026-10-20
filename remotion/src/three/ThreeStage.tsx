import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { buildSceneByShotId, SceneBundle } from "./scenes/ConsistencyScenes";

export interface ShotCameraConfig {
  shotId: number;
  startFrame: number;
  endFrame: number;
  startPos: [number, number, number];
  endPos: [number, number, number];
  target: [number, number, number];
  endTarget?: [number, number, number];
  fov: number;
  timeRange?: [number, number];
}

interface ThreeStageProps {
  shots: ShotCameraConfig[];
}

export const ThreeStage: React.FC<ThreeStageProps> = ({ shots }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const activeScenesRef = useRef<Map<number, SceneBundle>>(new Map());

  // Determine current active shot
  const currentShot =
    shots.find((s) => frame >= s.startFrame && frame < s.endFrame) || shots[0];

  useEffect(() => {
    if (!canvasRef.current) return;

    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      antialias: true,
      alpha: true,
      powerPreference: "high-performance",
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    rendererRef.current = renderer;

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    cameraRef.current = camera;

    return () => {
      renderer.dispose();
      rendererRef.current = null;
      cameraRef.current = null;
    };
  }, [width, height]);

  // Render on each Remotion frame change
  useEffect(() => {
    if (!rendererRef.current || !cameraRef.current || !currentShot) return;

    // Cache or load scene bundle for this shot
    let bundle = activeScenesRef.current.get(currentShot.shotId);
    if (!bundle) {
      bundle = buildSceneByShotId(currentShot.shotId);
      activeScenesRef.current.set(currentShot.shotId, bundle);
    }

    const rawProgress = Math.max(
      0,
      Math.min(
        1,
        (frame - currentShot.startFrame) /
          Math.max(1, currentShot.endFrame - currentShot.startFrame)
      )
    );
    // Smoothstep cubic easing: eliminates abrupt robotic stops and starts
    const shotProgress = rawProgress * rawProgress * (3 - 2 * rawProgress);

    // Smooth camera path interpolation
    const camX = interpolate(
      shotProgress,
      [0, 1],
      [currentShot.startPos[0], currentShot.endPos[0]]
    );
    const camY = interpolate(
      shotProgress,
      [0, 1],
      [currentShot.startPos[1], currentShot.endPos[1]]
    );
    const camZ = interpolate(
      shotProgress,
      [0, 1],
      [currentShot.startPos[2], currentShot.endPos[2]]
    );

    const tarX = currentShot.endTarget
      ? interpolate(shotProgress, [0, 1], [currentShot.target[0], currentShot.endTarget[0]])
      : currentShot.target[0];
    const tarY = currentShot.endTarget
      ? interpolate(shotProgress, [0, 1], [currentShot.target[1], currentShot.endTarget[1]])
      : currentShot.target[1];
    const tarZ = currentShot.endTarget
      ? interpolate(shotProgress, [0, 1], [currentShot.target[2], currentShot.endTarget[2]])
      : currentShot.target[2];

    const camera = cameraRef.current;
    camera.fov = currentShot.fov;
    camera.position.set(camX, camY, camZ);
    camera.lookAt(tarX, tarY, tarZ);
    camera.updateProjectionMatrix();

    // Update scene animations & character biomechanics & optional dynamic camera tracking
    const timeInSeconds = currentShot.timeRange
      ? interpolate(shotProgress, [0, 1], currentShot.timeRange)
      : frame / fps;
    bundle.update(timeInSeconds, camera);

    // Render frame
    rendererRef.current.setClearColor(0x0a0e17, 1.0);
    rendererRef.current.render(bundle.scene, camera);
  }, [frame, currentShot, fps]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        width: "100%",
        height: "100%",
        display: "block",
        backgroundColor: "#0A0E17",
      }}
    />
  );
};
