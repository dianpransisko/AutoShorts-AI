![Preview Program](https://raw.githubusercontent.com/dianpransisko/AutoShorts-AI/main/preview.png)

# 🎥 AutoShorts AI 
> **High-Performance Neural Engine for Automated Ecclesiastical Content Repurposing**

**AutoShorts AI** is a professional-grade desktop suite engineered for church multimedia departments. It streamlines the conversion of long-form liturgical recordings into high-impact vertical content (Shorts, Reels, TikTok) using localized AI processing.

---

## 🛠 Prerequisites & Dependencies
To ensure optimal rendering and transcription performance, please verify the following components:

1. **ImageMagick (Required for Subtitles):**
   - **Download:** [ImageMagick v7.1.x](https://imagemagick.org/script/download.php)
   - **CRITICAL:** During Windows installation, you **MUST** check the box **"Install legacy utilities (e.g. convert)"** to enable subtitle rasterization within the MoviePy engine.
   
2. **AI Model Weights:**
   - Manual download is not required. The application will automatically fetch the **Faster-Whisper (Small)** and **Silero VAD** weights from Hugging Face upon the first execution. Please ensure a stable internet connection for the initial launch.

---

## 🚀 Key Features
* **Zero-Cloud Dependency:** 100% offline processing ensures congregational data privacy and zero recurring subscription costs.
* **Automated Watch-Directory:** Background monitoring system that triggers the processing pipeline upon file detection.
* **Vertical Reframing:** Automatic 9:16 aspect ratio adjustment with intelligent speaker centering.
* **Neural Subtitling:** Dynamic, time-synced captions utilizing high-readability typography for maximum engagement.

---

## 📦 Installation & Deployment

### For End-Users (Executable)
1. Navigate to the **[Releases](https://github.com/dianpransisko/AutoShorts-AI/releases/tag/v1.0.0)** page.
2. Download the latest `.zip` distribution.
3. Extract and execute `AutoShortsAI.exe` as **Administrator**.

### For Developers (Source Code)
1. Clone the repository: `git clone https://github.com/dianpransisko/AutoShorts-AI.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the application: `python main.py`

---

## ⚙️ Post-Installation Configuration
To sync the rendering engine with the subtitle rasterizer:

1. **Binary Mapping:** Click the **Search** icon next to the `Magick.exe` field in the application settings.
2. **Pathing:** Navigate to your local ImageMagick installation, typically located at:
   `C:\Program Files\ImageMagick-7.1.x-Q16-HDRI\magick.exe`
3. **Persistence:** Click **SAVE** to write the configuration to the environment (`.env`) file.

---

## 💻 Hardware Specifications
| Component | Minimum Requirement | Recommended Specification |
| :--- | :--- | :--- |
| **Processor** | Intel Core i3 / AMD Ryzen 3 | Intel Core i5 / AMD Ryzen 5 or higher |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 5 GB available HDD space | 10 GB+ available SSD space |
| **Graphics** | Integrated Graphics | NVIDIA GeForce (for AI acceleration) |

---

## 🚀 Roadmap & Upcoming Features
* **Intelligent Speaker Tracking (MediaPipe):** Automated tracking of the speaker's movement to maintain focus during sermons.
* **Multi-Speaker Diarization:** AI logic to distinguish between the Preacher, Worship Leader, and congregational responses.
* **Batch GPU Acceleration:** Support for NVIDIA CUDA to drastically reduce processing times for high-volume content.

---

## 🔍 Troubleshooting
| Issue | Diagnostic | Resolution |
| :--- | :--- | :--- |
| **I/O Error [WinError 2]** | ImageMagick binary path mismatch. | Re-map `magick.exe` in the Settings menu. |
| **VAD Initialization Failure** | Missing `.onnx` weights. | Ensure internet connectivity during the first run. |
| **Write Permission Denied** | Locked `/temp` or `/outputs` folder. | Run the application as **Administrator**. |

---

## 🏗 Stack Summary
* **Core:** Python 3.10
* **AI Engine:** Faster-Whisper, Silero VAD
* **Graphics Architecture:** MoviePy, ImageMagick 7.1.x
* **UI Framework:** CustomTkinter (Modern Dark Theme)

---

## 👤 Developer & Support
**Dian Pransisko Harahap** **Copyright © 2026 - All Rights Reserved**

----
** Manual book download : **Download:** [ImageMagick v7.1.x](https://zenodo.org/records/19312037)
----
