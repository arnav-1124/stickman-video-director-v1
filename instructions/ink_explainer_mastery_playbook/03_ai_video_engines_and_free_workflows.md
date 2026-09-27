# 03: AI Video Engines & Free Cloud Workflows

## 1. Engine Comparison for Ink Explainer Style

| Engine | Free Tier / Availability | 2D Line Art Adherence | Recommended Workflow |
| :--- | :--- | :--- | :--- |
| **Hailuo AI (MiniMax Video-01)** | Free daily credits (web UI) | ⭐⭐⭐⭐⭐ Exceptional at 2D physics | Text-to-Video directly using prompt packets |
| **Kling AI 1.5** | Free daily credits (66 credits/day) | ⭐⭐⭐⭐⭐ Sharp line control, high stability | Image-to-Video (Anchor image -> Kling) |
| **Google Flow / Veo (VideoFX)** | Free access via Google Labs | ⭐⭐⭐⭐ Smooth continuous motion | Text-to-Video with camera direction tags |
| **Luma Dream Machine** | 30 free video generations/month | ⭐⭐⭐⭐ Dynamic lighting, fast rendering | Text-to-Video or start/end keyframe |
| **Leonardo AI (Motion)** | 150 daily free fast tokens | ⭐⭐⭐⭐⭐ Perfect consistency for anchors | Generate anchor in Leonardo -> Animate |

---

## 2. Recommended Production Workflows

### Option A: Direct Text-to-Video (Fastest)
1. Run `python pipeline/automate_pipeline.py projects/<episode_name> --export-batch`
2. Open `projects/<episode_name>/quick_batch_copypaste.txt`
3. Go to **Hailuo AI** (`hailuoai.video`) or **Kling AI** (`klingai.com`)
4. Copy-paste prompt for Shot 1, Shot 2, Shot 3...
5. Download generated MP4s to your default `Downloads` folder
6. Run: `python pipeline/automate_pipeline.py projects/<episode_name> --ingest-videos`
   - Files are automatically moved into `projects/<episode_name>/raw/shot_1.mp4`, `shot_2.mp4`...
7. Run: `python pipeline/build_video.py projects/<episode_name>/build_manifest.json`

### Option B: Image-to-Video Anchor Workflow (Maximum Consistency)
1. Generate Shot 1 anchor image on **Leonardo AI** or **Midjourney** using the anchor prompts from `prompts.json`.
2. Feed anchor image into **Kling AI** or **Hailuo AI** as the starting frame.
3. Prompt with the motion instructions.
4. Ingest and assemble into final video.
