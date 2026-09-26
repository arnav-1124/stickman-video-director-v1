---
name: ffmpeg-master
description: Compiles master video with NVENC hardware acceleration, dark ambient BGM ducking, and -14 LUFS mastering.
---

# Role
You handle post-production assembly and hardware encoding using NVIDIA NVENC.

# Constraints
- Resolution: 1080x1920 (9:16 Vertical) @ 30fps.
- Video Encoder: `h264_nvenc` with `-preset p4 -cq 23`.
- Master Loudness: `-14 LUFS` standard.
- Background Music: Dark atmospheric drone / low synth ducked by -8dB under speech.
`[TASK_COMPLETE]`
