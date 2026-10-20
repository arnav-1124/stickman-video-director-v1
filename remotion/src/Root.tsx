import React from "react";
import { Composition, Folder } from "remotion";
import { ConsistencyParadoxComposition } from "./compositions/long/ep02_the_consistency_paradox";
import { CLIPS_METADATA } from "./compositions/long/ep02_the_consistency_paradox/clips";
import * as Clips from "./compositions/long/ep02_the_consistency_paradox/clips";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 1. Full Master Video: THE CONSISTENCY PARADOX (158.84s / 4765 frames @ 30fps) */}
      <Composition
        id="ConsistencyParadoxLong"
        component={ConsistencyParadoxComposition}
        durationInFrames={4765}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* 2. Modular Clip-Wise Compositions (5s - 10s each, strict 0.25s pause) */}
      <Folder name="Consistency-Paradox-Clips">
        {CLIPS_METADATA.map((clip) => {
          const Component = (Clips as any)[`${clip.name}Composition`];
          return (
            <Composition
              key={clip.name}
              id={clip.name.replace(/_/g, "-")}
              component={Component}
              durationInFrames={clip.durationFrames}
              fps={30}
              width={1920}
              height={1080}
            />
          );
        })}
      </Folder>
    </>
  );
};
