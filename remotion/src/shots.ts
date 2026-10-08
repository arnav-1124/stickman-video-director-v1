export interface Shot {
  id: number;
  image: string;
  start: number;
  end: number;
  zoomStart: number;
  zoomEnd: number;
  cx1: number;
  cy1: number;
  cx2: number;
  cy2: number;
  title: string;
}

export const SHOTS: Shot[] = [
  { id: 1, image: "slides/slide_37.jpg", start: 0.08, end: 2.16, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Title Card Subtle Push" },
  { id: 2, image: "slides/slide_37.jpg", start: 2.16, end: 4.22, zoomStart: 1.06, zoomEnd: 1.18, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.60, title: "Push into slot machine reels" },
  { id: 3, image: "slides/slide_38.jpg", start: 4.22, end: 6.60, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.46, cy1: 0.50, cx2: 0.54, cy2: 0.50, title: "Tracking pan across retro lab" },
  { id: 4, image: "slides/slide_38.jpg", start: 6.60, end: 9.00, zoomStart: 1.25, zoomEnd: 1.34, cx1: 0.50, cy1: 0.55, cx2: 0.50, cy2: 0.52, title: "Close-up cut on center chamber" },
  { id: 5, image: "slides/slide_39.jpg", start: 9.00, end: 11.50, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.48, title: "Wide view of Skinner at clipboard" },
  { id: 6, image: "slides/slide_39.jpg", start: 11.50, end: 13.90, zoomStart: 1.28, zoomEnd: 1.36, cx1: 0.52, cy1: 0.42, cx2: 0.52, cy2: 0.40, title: "Push past glasses to observation window" },
  { id: 7, image: "slides/slide_40.jpg", start: 13.90, end: 17.60, zoomStart: 1.02, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.52, cy2: 0.50, title: "Profile creep towards pigeon and brass lever" },
  { id: 8, image: "slides/slide_41.jpg", start: 17.60, end: 19.80, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Wide tap action" },
  { id: 9, image: "slides/slide_41.jpg", start: 19.80, end: 21.84, zoomStart: 1.32, zoomEnd: 1.38, cx1: 0.52, cy1: 0.58, cx2: 0.52, cy2: 0.60, title: "Punch-in on food pellet dropping into bowl" },
  { id: 10, image: "slides/slide_41.jpg", start: 21.84, end: 24.76, zoomStart: 1.10, zoomEnd: 1.18, cx1: 0.50, cy1: 0.50, cx2: 0.52, cy2: 0.52, title: "Rhythmic mechanical repetition push" },
  { id: 11, image: "slides/cards/card_what_happened.jpg", start: 24.76, end: 26.50, zoomStart: 1.00, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "High-impact punch card pop" },
  { id: 12, image: "slides/slide_42.jpg", start: 26.50, end: 29.18, zoomStart: 1.12, zoomEnd: 1.00, cx1: 0.50, cy1: 0.50, cx2: 0.48, cy2: 0.50, title: "Pull-back: pigeon turns back on lever" },
  { id: 13, image: "slides/cards/card_100_predictable.jpg", start: 29.18, end: 31.02, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Predictability flatline card" },
  { id: 14, image: "slides/cards/card_reliable_safe_boring.jpg", start: 31.02, end: 33.34, zoomStart: 1.00, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Triple stamp card pop" },
  { id: 15, image: "slides/slide_44.jpg", start: 33.34, end: 35.42, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.48, title: "Skinner changes the rules" },
  { id: 16, image: "slides/cards/card_variable_ratio.jpg", start: 35.42, end: 38.00, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Variable-ratio schedule card" },
  { id: 17, image: "slides/slide_44.jpg", start: 38.00, end: 40.32, zoomStart: 1.25, zoomEnd: 1.34, cx1: 0.54, cy1: 0.42, cx2: 0.54, cy2: 0.40, title: "Punch-in on blinking amber indicator" },
  { id: 18, image: "slides/slide_45.jpg", start: 40.32, end: 44.20, zoomStart: 1.04, zoomEnd: 1.12, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.54, title: "Tension push on empty food bowl" },
  { id: 19, image: "slides/slide_46.jpg", start: 44.20, end: 45.54, zoomStart: 1.00, zoomEnd: 1.05, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "1 press rapid beat" },
  { id: 20, image: "slides/slide_46.jpg", start: 45.54, end: 47.34, zoomStart: 1.08, zoomEnd: 1.15, cx1: 0.50, cy1: 0.50, cx2: 0.52, cy2: 0.50, title: "5 presses rapid beat" },
  { id: 21, image: "slides/cards/card_reward_unpredictable.jpg", start: 47.34, end: 49.62, zoomStart: 1.00, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "12 presses nothing card" },
  { id: 22, image: "slides/slide_46.jpg", start: 49.62, end: 51.92, zoomStart: 1.26, zoomEnd: 1.35, cx1: 0.50, cy1: 0.58, cx2: 0.50, cy2: 0.60, title: "Detail cut: 2 pellets drop at once" },
  { id: 23, image: "slides/cards/card_reward_unpredictable.jpg", start: 51.92, end: 53.76, zoomStart: 1.04, zoomEnd: 1.10, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Reward unpredictable card" },
  { id: 24, image: "slides/cards/card_what_happened.jpg", start: 53.76, end: 54.92, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Pigeon reaction question card" },
  { id: 25, image: "slides/slide_47.jpg", start: 54.92, end: 56.88, zoomStart: 1.10, zoomEnd: 1.25, cx1: 0.50, cy1: 0.48, cx2: 0.50, cy2: 0.45, title: "Dramatic punch-in on obsessive dilated pupils" },
  { id: 26, image: "slides/slide_48.jpg", start: 56.88, end: 59.80, zoomStart: 1.02, zoomEnd: 1.10, cx1: 0.48, cy1: 0.50, cx2: 0.52, cy2: 0.50, title: "Tracking pan across frantic tapping" },
  { id: 27, image: "slides/slide_48.jpg", start: 59.80, end: 62.50, zoomStart: 1.20, zoomEnd: 1.30, cx1: 0.52, cy1: 0.48, cx2: 0.52, cy2: 0.46, title: "Detail cut: stickman ignoring sleep" },
  { id: 28, image: "slides/slide_49.jpg", start: 62.50, end: 64.50, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Wide brain circuitry" },
  { id: 29, image: "slides/slide_49.jpg", start: 64.50, end: 66.66, zoomStart: 1.25, zoomEnd: 1.35, cx1: 0.50, cy1: 0.45, cx2: 0.50, cy2: 0.42, title: "Deep push into glowing synapses" },
  { id: 30, image: "slides/slide_50.jpg", start: 67.03, end: 70.15, zoomStart: 1.00, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Neuroscientists explanation wide" },
  { id: 31, image: "slides/slide_51.jpg", start: 70.15, end: 73.25, zoomStart: 1.02, zoomEnd: 1.09, cx1: 0.48, cy1: 0.50, cx2: 0.52, cy2: 0.50, title: "Dopamine is not pleasure drift" },
  { id: 32, image: "slides/cards/card_dopamine_anticipation.jpg", start: 73.25, end: 75.93, zoomStart: 1.00, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Dopamine is anticipation card" },
  { id: 33, image: "slides/slide_52.jpg", start: 75.93, end: 78.10, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Brain scan prize baseline" },
  { id: 34, image: "slides/slide_52.jpg", start: 78.10, end: 80.31, zoomStart: 1.28, zoomEnd: 1.35, cx1: 0.50, cy1: 0.48, cx2: 0.50, cy2: 0.45, title: "Detail cut on flatline baseline spark" },
  { id: 35, image: "slides/slide_53.jpg", start: 80.31, end: 83.00, zoomStart: 1.00, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Massive volcanic dopamine eruption" },
  { id: 36, image: "slides/slide_53.jpg", start: 83.00, end: 85.61, zoomStart: 1.25, zoomEnd: 1.35, cx1: 0.50, cy1: 0.45, cx2: 0.50, cy2: 0.40, title: "Zoom on glowing question mark core" },
  { id: 37, image: "slides/slide_54.jpg", start: 85.61, end: 88.80, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.48, cy1: 0.50, cx2: 0.52, cy2: 0.50, title: "Slot machines, lottery, notifications wide" },
  { id: 38, image: "slides/slide_54.jpg", start: 88.80, end: 91.95, zoomStart: 1.26, zoomEnd: 1.35, cx1: 0.62, cy1: 0.50, cx2: 0.62, cy2: 0.48, title: "Detail zoom on glowing red notification badge" },
  { id: 39, image: "slides/slide_55.jpg", start: 91.95, end: 94.20, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Pull lever on slot machine" },
  { id: 40, image: "slides/slide_55.jpg", start: 94.20, end: 96.57, zoomStart: 1.25, zoomEnd: 1.35, cx1: 0.46, cy1: 0.50, cx2: 0.54, cy2: 0.50, title: "Horizontal tracking across spinning reels" },
  { id: 41, image: "slides/cards/card_unresolved_gap.jpg", start: 96.57, end: 99.91, zoomStart: 1.00, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Will 3 cherries align tension card" },
  { id: 42, image: "slides/slide_56.jpg", start: 99.91, end: 103.71, zoomStart: 1.05, zoomEnd: 1.15, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.48, title: "Unresolved gap between hope and fear" },
  { id: 43, image: "slides/cards/card_aloof_casino.jpg", start: 104.24, end: 105.74, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Shift to human interaction card" },
  { id: 44, image: "slides/slide_57.jpg", start: 105.74, end: 109.46, zoomStart: 1.02, zoomEnd: 1.09, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Available person as the first lever" },
  { id: 45, image: "slides/slide_58.jpg", start: 109.46, end: 111.78, zoomStart: 1.28, zoomEnd: 1.35, cx1: 0.52, cy1: 0.50, cx2: 0.52, cy2: 0.48, title: "Detail: text reply in 30 seconds" },
  { id: 46, image: "slides/slide_58.jpg", start: 111.78, end: 114.40, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Wide: showered with praise" },
  { id: 47, image: "slides/slide_58.jpg", start: 114.40, end: 116.66, zoomStart: 1.15, zoomEnd: 1.25, cx1: 0.50, cy1: 0.55, cx2: 0.50, cy2: 0.52, title: "Instant YES calendar invite" },
  { id: 48, image: "slides/cards/card_100_predictable.jpg", start: 116.66, end: 119.22, zoomStart: 1.00, zoomEnd: 1.08, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "100% predictable card" },
  { id: 49, image: "slides/slide_59.jpg", start: 119.22, end: 120.32, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "There is no mystery" },
  { id: 50, image: "slides/slide_59.jpg", start: 120.32, end: 121.32, zoomStart: 1.10, zoomEnd: 1.18, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.48, title: "There is no tension bored detail" },
  { id: 51, image: "slides/slide_60.jpg", start: 121.32, end: 124.56, zoomStart: 1.04, zoomEnd: 1.12, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "No anticipation no dopamine" },
  { id: 52, image: "slides/cards/card_zero_pull.jpg", start: 124.56, end: 126.80, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Zero gravitational pull card" },
  { id: 53, image: "slides/slide_61.jpg", start: 126.80, end: 128.82, zoomStart: 1.05, zoomEnd: 1.14, cx1: 0.50, cy1: 0.50, cx2: 0.48, cy2: 0.50, title: "Floating weightless stickman" },
  { id: 54, image: "slides/cards/card_aloof_casino.jpg", start: 128.82, end: 131.00, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "The aloof slot machine card" },
  { id: 55, image: "slides/slide_62.jpg", start: 131.00, end: 133.36, zoomStart: 1.04, zoomEnd: 1.12, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.48, title: "Aloof sovereign in dark hoodie leaning" },
  { id: 56, image: "slides/slide_63.jpg", start: 133.36, end: 136.84, zoomStart: 1.05, zoomEnd: 1.15, cx1: 0.50, cy1: 0.50, cx2: 0.52, cy2: 0.48, title: "Rare meaningful glance creep" },
  { id: 57, image: "slides/slide_64.jpg", start: 136.84, end: 140.10, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Compliment sticks for 3 weeks calendar" },
  { id: 58, image: "slides/slide_64.jpg", start: 140.10, end: 143.54, zoomStart: 1.25, zoomEnd: 1.35, cx1: 0.50, cy1: 0.48, cx2: 0.50, cy2: 0.45, title: "Rare golden coin in locked vault" },
  { id: 59, image: "slides/slide_65.jpg", start: 143.54, end: 146.98, zoomStart: 1.08, zoomEnd: 1.18, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.48, title: "Phone lights up screen flash" },
  { id: 60, image: "slides/cards/card_unresolved_gap.jpg", start: 146.98, end: 149.30, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Didn't know if they'd reply card" },
  { id: 61, image: "slides/slide_65.jpg", start: 149.30, end: 151.70, zoomStart: 1.22, zoomEnd: 1.30, cx1: 0.50, cy1: 0.48, cx2: 0.50, cy2: 0.46, title: "Stickman staring at glowing phone" },
  { id: 62, image: "slides/slide_66.jpg", start: 151.70, end: 154.22, zoomStart: 1.00, zoomEnd: 1.07, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Not in love with person wide" },
  { id: 63, image: "slides/slide_66.jpg", start: 154.22, end: 158.22, zoomStart: 1.08, zoomEnd: 1.18, cx1: 0.50, cy1: 0.48, cx2: 0.50, cy2: 0.45, title: "In love with unpredictability cocktail" },
  { id: 64, image: "slides/slide_67.jpg", start: 158.99, end: 161.60, zoomStart: 1.00, zoomEnd: 1.06, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Chapter 3 teaser wide" },
  { id: 65, image: "slides/slide_67.jpg", start: 161.60, end: 164.33, zoomStart: 1.20, zoomEnd: 1.30, cx1: 0.52, cy1: 0.48, cx2: 0.52, cy2: 0.45, title: "Stickman walking out the door" },
  { id: 66, image: "slides/slide_67.jpg", start: 164.33, end: 165.69, zoomStart: 1.12, zoomEnd: 1.20, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.48, title: "Economy of availability punch" },
  { id: 67, image: "slides/slide_67.jpg", start: 165.69, end: 169.13, zoomStart: 1.05, zoomEnd: 1.15, cx1: 0.50, cy1: 0.50, cx2: 0.50, cy2: 0.50, title: "Subscribe to Sticky in Dark hold" },
];
