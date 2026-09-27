# Cloud Video Generation Roadmap: Google Colab & RunPod Integration

> **Document Purpose:** Architectural blueprint and setup guide for scaling video generation beyond closed web quotas (Google Veo) using cloud GPU infrastructure (Google Colab Pro & RunPod).

---

## 1. Current Active Workflow vs Future Roadmap

| Tier | Engine / Hardware | Status | Best Use Case | Cost / Tokens |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (Current Active)** | **Google Veo 3.1 + Kling AI + Hailuo AI** | **Active Production** | Native 1080p, pristine cinematic lighting, zero RAM bottlenecks, fast 60s renders. | Free daily tiers & Google tokens. |
| **Tier 2 (Future Scale)** | **RunPod On-Demand (RTX 4090)** | **Roadmap (Post-Payment Setup)** | Unlimited high-speed Wan 2.1 (14B) rendering via ComfyUI. 45-60s per clip. | ~$0.25 to $0.34 / hour. |
| **Tier 3 (Future Scale)** | **Google Colab (High-RAM / A100)** | **Roadmap (Via Google Play UPI)** | Headless batch rendering directly syncing into Google Drive. | $10 for 100 Compute Units. |

---

## 2. Technical Findings from Free Google Colab (Tesla T4)

During testing on free Google Colab (Tesla T4 15GB VRAM + 12.7GB System RAM), the following hard bottlenecks were verified:
1. **System RAM Exhaustion (`OOM Kill`):**  
   Modern open-source video models like **Wan 2.1** utilize `google/umt5-xxl` (4.8 billion parameters) as their text encoder. Instantiating this encoder requires ~10–11 GB of host CPU RAM, hitting the free tier's 12.7 GB ceiling at 99% progress and causing kernel crashes.
2. **Older Compute Architecture (2018 Turing):**  
   The Tesla T4 lacks modern FP8/BF16 tensor cores. In ComfyUI with GGUF quantization, a single 4-second clip takes **20 to 28 minutes** to render on a T4, making multi-shot production unviable on free tiers.
3. **Requirement for Future Colab Use:**  
   Colab requires the **High-RAM tier (51 GB System RAM)** + **A100 GPU**, accessible via Colab Pay-As-You-Go units (which can be purchased in India via Google Play balance using UPI).

---

## 3. RunPod RTX 4090 Deployment Blueprint (For Future Activation)

When international card, virtual debit card (via Fi/Jupiter/Airtel Bank), or crypto is ready:

### Step-by-Step Setup:
1. **Account & Credits:**
   * Go to [runpod.io](https://www.runpod.io) $\to$ **Billing** $\to$ Load $5 or $10.
2. **Deploy Pod:**
   * **GPU:** 1x NVIDIA RTX 4090 (24GB VRAM, 61GB System RAM).
   * **Template:** Select official **RunPod ComfyUI** (or `comfyanonymous/ComfyUI`).
   * **Disk Allocation:** 50 GB Container Disk + 50 GB Volume.
3. **Workflow Execution:**
   * Open the ComfyUI web interface directly through RunPod's HTTP service port `8188`.
   * Load Wan 2.1 I2V workflow (`Wan2.1-I2V-14B`).
   * Drop scene anchor images $\to$ Input motion prompt $\to$ Render 4s clip in ~50 seconds.
   * Download batch clips directly to `projects/<episode>/raw/`.

---

## 4. Local Studio Post-Production Pipeline (Always Active)

Regardless of whether clips come from **Veo**, **Kling**, **Hailuo**, or **RunPod**:
1. Drop downloaded clips into `projects/<episode>/raw/shot_1.mp4`, `shot_2.mp4`...
2. Run Voiceover: `python pipeline/generate_audio.py projects/<episode> --voice christopher`
3. Run Subtitles: `python pipeline/generate_subtitles.py projects/<episode> --aspect 9:16`
4. Assemble Video: `python pipeline/build_video.py projects/<episode>/build_manifest.json`
   * Hardware accelerated via local NVIDIA RTX 2050 NVENC (`p4 -cq 23`).
   * Ducked BGM (-14 LUFS broadcast standard).
   * Render completes in under 30 seconds locally.
