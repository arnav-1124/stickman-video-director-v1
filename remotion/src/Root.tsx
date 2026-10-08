import React from "react";
import { Composition } from "remotion";
import { z } from "zod";
import { Chapter02Composition } from "./compositions/long/ep01/chapter_02";

export const chapter02Schema = z.object({
  zoomStart: z.number().min(1.0).max(1.8).step(0.01),
  zoomEnd: z.number().min(1.0).max(1.8).step(0.01),
  panCenterX: z.number().min(0).max(100).step(1),
  panCenterY: z.number().min(0).max(100).step(1),
  showOnScreenHUD: z.boolean(),
});

export type Chapter02Props = z.infer<typeof chapter02Schema>;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Long-Form Episode 01: Chapter 02 (The Casino Effect) */}
      <Composition
        id="Chapter02"
        component={Chapter02Composition}
        schema={chapter02Schema}
        defaultProps={{
          zoomStart: 1.08,
          zoomEnd: 1.25,
          panCenterX: 50,
          panCenterY: 50,
          showOnScreenHUD: true,
        }}
        durationInFrames={5031} // 167.70s @ 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
