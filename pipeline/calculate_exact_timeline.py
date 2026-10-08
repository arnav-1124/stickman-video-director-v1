import json
from pathlib import Path

def get_exact_slide_cuts():
    # Exact slide boundaries based on word timestamps
    # Each entry: (filename, start_sec, end_sec, note)
    # Total: 62 cuts, seamlessly synchronized to audio words
    cuts = [
        ("slide_01.jpg", 0.000, 1.600, "Right now, you probably tell"),
        ("slide_02.jpg", 1.600, 5.070, "between two to five lies every single day. [Marker: 2 TO 5 LIES]"),
        ("slide_03.jpg", 5.070, 6.190, "I'm five minutes away."),
        ("slide_04.jpg", 6.190, 7.580, "Sorry, my phone died."),
        ("slide_05.jpg", 7.580, 8.750, "No, you look great."),
        ("slide_06.jpg", 8.750, 9.860, "It's so effortless, [Marker: EFFORTLESS]"),
        ("slide_07.jpg", 9.860, 11.160, "you don't even think about it."),
        ("slide_08.jpg", 11.160, 14.200, "In fact, you might even be lying to yourself right now"),
        ("slide_09.jpg", 14.200, 15.950, "about why you opened YouTube. [Doodle: YT Icon]"),
        ("slide_10.jpg", 15.950, 17.520, "Now, imagine a world [Marker: IMAGINE A WORLD]"),
        ("slide_11.jpg", 17.520, 20.230, "where lying is physically impossible,"),
        ("slide_12.jpg", 20.230, 22.300, "where every sound that comes out of your mouth"),
        ("slide_13.jpg", 22.300, 24.660, "is an unedited broadcast of reality, [Marker: UNEDITED REALITY]"),
        ("slide_14.jpg", 24.660, 27.590, "because for 99% of evolution, [Tally: 99% OF EVOLUTION]"),
        ("slide_15.jpg", 27.590, 29.840, "that was the only world that existed."),
        ("slide_16.jpg", 29.840, 32.150, "If a monkey shrieked, there was a leopard."),
        ("slide_17.jpg", 32.150, 34.300, "If a bird called, there was a hawk."),
        ("slide_18.jpg", 34.300, 36.490, "Honesty wasn't a moral virtue. [Marker: HARDWIRED SURVIVAL]"),
        ("slide_19.jpg", 36.490, 38.550, "It was hardwired survival. [Diagram: INPUT=OUTPUT]"),
        ("slide_20.jpg", 38.550, 41.270, "Until about 200,000 years ago, [Marker: 200,000 YEARS AGO]"),
        ("slide_21.jpg", 41.270, 43.540, "somewhere on the East African Savannah,"),
        ("slide_22.jpg", 43.540, 45.560, "an ancient human named Grog"),
        ("slide_23.jpg", 45.560, 48.140, "did something that permanently broke reality."),
        
        # --- Slide 24 Split (Was 4.38s -> Now two punchy cuts of 2.31s and 2.07s) ---
        ("slide_24A.jpg", 48.140, 50.450, "While foraging alone behind a rocky ridge,"),
        ("slide_24.jpg", 50.450, 52.520, "Grog found a wild beehive,"),
        
        ("slide_25.jpg", 52.520, 54.590, "overflowing with golden honey. [Prop: Honeycomb]"),
        ("slide_26.jpg", 54.590, 57.560, "Now, in a prehistoric tribe, the rule was unbreakable: [Marker: RULE #1]"),
        ("slide_27.jpg", 57.560, 58.720, "Whatever you find,"),
        ("slide_28.jpg", 58.720, 60.600, "you bring back and share equally."),
        ("slide_29.jpg", 60.600, 61.950, "Grog looked at the honey."),
        ("slide_30.jpg", 61.950, 63.580, "Then he looked back toward the cave,"),
        ("slide_31.jpg", 63.580, 66.900, "and his brain did something no living animal had ever done: [Prop: Brain Gears]"),
        ("slide_32.jpg", 66.900, 68.820, "It calculated the future. [Marker: CALCULATING THE FUTURE]"),
        ("slide_33.jpg", 68.820, 72.810, "If he shared it with 30 hungry tribe members, he got one sticky mouthful."),
        ("slide_34.jpg", 72.810, 75.920, "If he kept it secret, he feasted like a king for weeks."),
        ("slide_35.jpg", 75.920, 80.480, "There was only one problem: how could he return to the cave with completely empty hands?"),
        ("slide_36.jpg", 80.480, 85.220, "Until that second, words were only used to describe what was actually real. [Marker: WORDS=REALITY]"),
        ("slide_37.jpg", 85.220, 88.440, "Grog decided to describe something that didn't exist."),
        ("slide_38.jpg", 88.440, 90.710, "When he walked into the firelit cave at sunset,"),
        ("slide_39.jpg", 90.710, 93.300, "the tribe leader demanded to know where he had been."),
        ("slide_40.jpg", 93.300, 94.320, "Grog didn't panic."),
        
        # --- Slide 41 Split (Was 6.70s -> Now three dynamic cuts of 2.13s, 2.25s, and 2.32s) ---
        ("slide_41A.jpg", 94.320, 96.450, "He looked the leader dead in the eye,"),
        ("slide_41.jpg", 96.450, 98.700, "clutched his chest in fake terror,"),
        ("slide_41C.jpg", 98.700, 101.020, "and invented the very first lie: [Marker: THE VERY FIRST LIE]"),
        
        ("slide_42.jpg", 101.020, 103.240, "\"A pack of ferocious hyenas chased me"),
        ("slide_43.jpg", 103.240, 104.060, "off the ridge.\" [Marker: FEROCIOUS HYENAS!]"),
        ("slide_44.jpg", 104.060, 105.860, "The tribe gasped in horror."),
        ("slide_45.jpg", 105.860, 108.460, "The leader patted Grog's shoulder, relieved he survived."),
        ("slide_46.jpg", 108.460, 110.010, "Nobody questioned him,"),
        ("slide_47.jpg", 110.010, 112.140, "because nobody even knew what a lie was. [Marker: NOBODY KNEW]"),
        ("slide_48.jpg", 112.140, 115.560, "And in that single second, human history shifted forever."),
        ("slide_49.jpg", 115.560, 119.720, "Without throwing a single punch, Grog controlled the entire tribe."),
        ("slide_50.jpg", 119.720, 121.080, "Soon, deception started [Marker: THE BIOLOGICAL ARMS RACE]"),
        ("slide_51.jpg", 121.080, 123.680, "an unstoppable biological arms race."),
        
        # --- Slide 52 Split (Was 4.15s -> Now two punchy cuts of 2.82s and 1.33s) ---
        ("slide_52A.jpg", 123.680, 126.500, "To survive, human brains had to evolve rapidly—"),
        ("slide_52.jpg", 126.500, 127.830, "not to outsmart lions,"),
        
        ("slide_53.jpg", 127.830, 129.630, "but to outsmart each other. [Diagram: SKULL GROWTH]"),
        ("slide_54.jpg", 129.630, 131.280, "Our frontal lobes ballooned in size"),
        ("slide_55.jpg", 131.280, 133.550, "just to detect who was making things up. [Marker: WHY WE GOT SMART!]"),
        ("slide_56.jpg", 133.550, 135.560, "Which means the very reason you are smart"),
        ("slide_57.jpg", 135.560, 136.840, "enough to understand this video..."),
        ("slide_58.jpg", 136.840, 139.595, "Is because your ancestors were professional liars.")
    ]
    return cuts

if __name__ == "__main__":
    cuts = get_exact_slide_cuts()
    print(f"Total Cuts: {len(cuts)}")
    total_dur = 0.0
    for idx, (filename, st, en, note) in enumerate(cuts, 1):
        dur = en - st
        total_dur += dur
        print(f"[{idx:02d}] {filename:14s} [{st:7.3f}s -> {en:7.3f}s] ({dur:5.3f}s) | {note}")
    print(f"\nTotal Video Duration: {total_dur:.3f}s")
