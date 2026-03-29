![Preview Program](<https://github.com/dianpransisko/AutoShorts-AI/blob/main/preview.png>)
# 🎥 AutoShorts AI 
> **High-Performance Neural Engine for Automated Ecclesiastical Content Repurposing**

**AutoShorts AI** is a professional-grade desktop suite engineered for church multimedia departments. It streamlines the conversion of long-form liturgical recordings into high-impact vertical content (Shorts, Reels, TikTok) using localized AI processing.

---

## 🚀 Roadmap & Upcoming Features
We are committed to continuous innovation. The following features are currently in active development:

* **Intelligent Speaker Tracking (MediaPipe):** Integration of MediaPipe Pose Landmark Detection to automatically track the speaker's movement, ensuring perfect 9:16 framing even when the preacher moves across the pulpit.
* **Multi-Speaker Diarization:** Enhancing AI logic to distinguish between different speakers (e.g., Preacher vs. Worship Leader).
* **Batch GPU Acceleration:** Support for NVIDIA CUDA to further decrease rendering times for high-volume content.

---

## 💻 Hardware Specifications
To ensure stable performance during AI transcription and video rendering, the following specifications are recommended:

| Component | Minimum Requirement | Recommended Specification |
| :--- | :--- | :--- |
| **OS** | Windows 10/11 (64-bit) | Windows 10/11 (64-bit) |
| **Processor** | Intel Core i3 / AMD Ryzen 3 | Intel Core i5 / AMD Ryzen 5 or higher |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 5 GB available HDD space | 10 GB+ available SSD space |
| **Graphics** | Integrated Graphics | NVIDIA GeForce (for AI acceleration) |

*Note: Using an SSD is highly recommended to significantly reduce rendering times.*

---

## 🛠 Technical Architecture
AutoShorts AI integrates several industry-standard engines to ensure a seamless, offline-first workflow:
* **Neural Transcription:** Powered by the **Faster-Whisper (Small)** model for low-latency, high-accuracy speech-to-text.
* **VAD Logic:** Implements **Silero VAD v6** for precise voice activity detection and noise gating.
* **Audio Engineering:** Integrated **Deep-Learning Denoiser** to isolate vocal frequencies and eliminate ambient sanctuary noise.
* **Rendering Pipeline:** High-speed processing via **MoviePy** and **FFmpeg** with **ImageMagick** for dynamic subtitle rasterization.

---

## 🚀 Key Features
* **Zero-Cloud Dependency:** 100% offline processing ensures data privacy and zero subscription costs.
* **Automated Watch-Directory:** Background monitoring system that triggers the pipeline upon file detection.
* **Vertical Reframing:** Automatic 9:16 aspect ratio adjustment with intelligent centering.
* **Neural Subtitling:** Dynamic, time-synced captions with high-readability fonts.
* **Custom Branding:** Seamless integration of church logos and watermarks.

---

## 📦 Installation & Deployment
1. Navigate to the `/installer_result` directory.
2. Execute `AutoShortsAIv1.exe` as **Administrator**.
3. Follow the deployment wizard to finalize the installation.
4. Launch the application via the **Desktop Shortcut**.

---

## ⚙️ Post-Installation Configuration
To ensure the rendering engine communicates correctly with the subtitle rasterizer:

1. **Binary Mapping:** Click the **Search** icon next to the `Magick.exe` field.
2. **Pathing:** Navigate to the local installation directory:
   `C:\Program Files (x86)\AutoShorts AI\imagemagick\magick.exe`
3. **Persistence:** Click **SAVE** to write the configuration to the environment (`.env`) file.

---

## 📖 Operational Workflow
1. **Ingestion:** Deposit raw `.mp4` sermon recordings into your designated **Watch Directory**.
2. **Execution:** Click **Start** to initialize the multi-stage pipeline.
3. **Stages:**
   * `Stage 1`: Audio Isolation & Denoising.
   * `Stage 2`: Neural Transcription (Whisper).
   * `Stage 3`: Subtitle Rasterization (ImageMagick).
   * `Stage 4`: Final Rendering & Export.
4. **Retrieval:** Access finalized content in the `/outputs` directory.

---

## 🔍 Troubleshooting & Maintenance
| Issue | Diagnostic | Resolution |
| :--- | :--- | :--- |
| **I/O Error [WinError 2]** | ImageMagick binary path mismatch. | Re-map `Magick.exe` in settings. |
| **VAD Initialization Failure** | Missing `.onnx` weights in `_internal`. | Verify `silero_vad_v6.onnx` presence. |
| **Write Permission Denied** | Insufficient privileges for `/temp` folder. | Run application as **Administrator**. |

---

## 🏗 Stack Summary
* **Core:** Python 3.10
* **AI:** Faster-Whisper, Silero VAD, MediaPipe (Planned)
* **Graphics:** MoviePy, ImageMagick 7.1.2
* **UI:** CustomTkinter (Modern Dark Theme)

---

## 👤 Developer & Support
**Dian Pransisko Harahap**  **Copyright © 2026 - All Rights Reserved**