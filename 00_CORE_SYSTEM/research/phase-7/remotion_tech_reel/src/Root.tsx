import React from "react";
import { Composition } from "remotion";
import { TechDialogueReel } from "./TechDialogueReel";
import metadata from "./dialogue_metadata.json";

export const Root: React.FC = () => {
  const fps = 30;
  const durationInFrames = Math.ceil(metadata.total_duration * fps);

  return (
    <Composition
      id="TechDialogueReel"
      component={TechDialogueReel}
      durationInFrames={durationInFrames}
      fps={fps}
      width={1080}
      height={1920}
    />
  );
};
