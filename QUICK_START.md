# 🚀 Quick Start Guide

## Android Installation
This project is ready to be compiled into an APK using Buildozer.

1. **Setup Buildozer** (on Linux/WSL):
   ```bash
   pip install buildozer
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

2. **Build the APK**:
   ```bash
   cd /path/to/project
   buildozer android debug
   ```

3. **Install on Device**:
   The APK will be in the `bin/` folder. Transfer it to your phone or use:
   ```bash
   buildozer android deploy run
   ```

## Desktop Testing
To test the UI and logic before building:
1. `pip install -r requirements.txt`
2. `python TEST_DESKTOP.py`

## Troubleshooting
- **Download fails?** Check your internet connection. Some sites throttle non-browser downloads.
- **App crashes on startup?** Use `buildozer android logcat` to debug.
