# 🎬 Lastic Productions - Multi-Platform Video Downloader

## 🎯 Key Features
- **Multi-Platform Support**: YouTube, Instagram, Twitter/X, Facebook, TikTok, and more.
- **Quality Options**: Best, 1080p, 720p, 480p, 360p, Audio Only (MP3).
- **Professional UI**: Clean dark mode interface with real-time progress tracking.
- **Android Optimized**: Handles permissions and downloads to external storage.

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- `pip`
- `ffmpeg` (for merging audio/video)

### Installation on Desktop (Testing)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the desktop test runner:
   ```bash
   python TEST_DESKTOP.py
   ```

### Building for Android
1. Ensure you are on Linux (or WSL) with Buildozer prerequisites installed.
2. Connect your Android device.
3. Run:
   ```bash
   buildozer android debug deploy run
   ```

## 📁 Project Structure
- `main.py`: Core application code.
- `buildozer.spec`: Buildozer configuration.
- `requirements.txt`: Python dependencies.
- `TEST_DESKTOP.py`: Helper script for desktop testing.
- `INSTALL.sh`: Helper script for dependency installation.

## ⚖️ License
MIT License
