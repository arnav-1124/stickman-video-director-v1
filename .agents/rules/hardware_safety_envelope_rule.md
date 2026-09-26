# Hardware Safety Envelope Rule (60-70% Capacity Cap)

## 1. Workload Limits
- Device Profile: 12th Gen Intel i5-12450H + NVIDIA RTX 2050 (4GB VRAM) + 16GB RAM.
- **Strict Cap**: Keep system load at or below 60%–70% of peak capacity.
  - Max target CPU usage: 50%.
  - Max target VRAM allocation: 2.0 GB (out of 4.0 GB).
  - Temperature goal: Laptop runs quiet and cool with zero thermal throttling.

## 2. NVENC Accelerated Encoding
- All FFmpeg encoding passes MUST utilize hardware acceleration:
  `-c:v h264_nvenc -preset p4 -cq 23 -pix_fmt yuv420p`
- Renders 1080x1920 @ 30fps at 150+ fps with under 25% GPU load.
