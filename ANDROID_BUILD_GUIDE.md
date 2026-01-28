# 🤖 Android Build with GitHub Actions

## 🚀 Quick Start

### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit - Add Android video downloader"
```

### 2. Push to GitHub
```bash
# Create repository on GitHub first, then:
git remote add origin https://github.com/yourusername/lastic-productions.git
git branch -M main
git push -u origin main
```

### 3. Trigger Build
- Go to your repository on GitHub
- Click "Actions" tab
- Select "Build Android APK" workflow
- Click "Run workflow"

## 📱 Download APK

Once build completes:
1. Go to Actions → Build Android APK
2. Click on the latest run
3. Download "android-apk" artifact
4. Extract and install the APK on your Android device

## 🔧 Workflow Features

✅ **Automatic builds** on push to main branch  
✅ **Tag releases** create GitHub releases with APK  
✅ **Cached dependencies** for faster builds  
✅ **Multiple Python versions** support  
✅ **Artifact retention** for 30 days  

## 📋 Build Requirements

- Python 3.10
- Android NDK r25c
- Java 8 (Temurin)
- Buildozer
- FFmpeg for video processing

## 🛠️ Customization

### Change App Info
Edit `buildozer.spec`:
```ini
title = Your App Name
package.name = yourappname
version = 1.0.0
```

### Add Permissions
```ini
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
```

### Change Icon
Add icon.png to project root and update:
```ini
icon.filename = %(source.dir)s/icon.png
```

## 🚨 Troubleshooting

### Build Fails
- Check Actions logs for specific errors
- Ensure all dependencies in requirements.txt
- Verify buildozer.spec syntax

### APK Won't Install
- Enable "Unknown Sources" on Android
- Check Android version compatibility
- Verify required permissions

## 📱 Testing on Device

1. Download APK from GitHub Actions
2. Transfer to Android device
3. Enable "Install from unknown sources"
4. Install APK
5. Grant permissions when prompted
6. Test with Twitter/X video URLs

## 🔄 Automatic Releases

Create a tag to automatically release:
```bash
git tag v1.0.0
git push origin v1.0.0
```

This will:
- Build release APK
- Create GitHub release
- Attach APK to release
- Generate release notes

🎉 **Your Android app will be built automatically!**
