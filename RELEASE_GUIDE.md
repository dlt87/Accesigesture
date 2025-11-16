# How to Create a GitHub Release

## Automatic Release (Recommended)

### Step 1: Build the Installer Locally
```bash
.\build_release.bat
```

This creates: `release\AccesiGesture-Setup-v1.0.0.exe`

### Step 2: Create a GitHub Release

1. Go to your GitHub repository: https://github.com/dlt87/Accesigesture
2. Click on "Releases" (right sidebar)
3. Click "Create a new release"
4. Create a new tag: `v1.0.0`
5. Release title: `AccesiGesture v1.0.0`
6. Upload the installer: `release\AccesiGesture-Setup-v1.0.0.exe`
7. Add description:

```markdown
## AccesiGesture v1.0.0

Hand gesture control for Windows - Control your computer with hand gestures!

### 🚀 Installation
1. Download `AccesiGesture-Setup-v1.0.0.exe` below
2. Run the installer
3. Launch from Start Menu or Desktop icon

### ✨ Features
- 🖱️ Control cursor with open hand
- 👆 Click with pinch gesture
- 📜 Scroll with thumbs up/down
- ⚙️ Real-time settings adjustment
- 🎯 Low latency tracking

### 📋 Requirements
- Windows 10 or 11 (64-bit)
- Webcam
- ~200MB disk space

### 🎮 Quick Start
1. Allow camera permissions on first run
2. Show your open hand to move cursor
3. Pinch (thumb+index) to click
4. Thumbs up/down to scroll
5. Use settings window to customize

### 🔧 First Time Setup
- All settings are in the Settings window
- Adjust smoothing for your preference
- Map gestures to different actions
- Toggle (thumb+index+pinky) to pause/resume
```

8. Click "Publish release"

### Step 3: Share the Link
Users can now download from: `https://github.com/dlt87/Accesigesture/releases/latest`

---

## Automatic Releases with GitHub Actions

The `.github/workflows/release.yml` file is already set up!

### To trigger automatic build:
1. Commit your code
2. Create and push a tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will automatically:
- Build the application
- Create the installer
- Upload to GitHub Releases

---

## User Experience

When users visit your GitHub:
1. They see "Releases" section
2. Click on latest release
3. Download `AccesiGesture-Setup-v1.0.0.exe`
4. Double-click to install
5. App launches - ready to use!

**One-click install, zero configuration needed!**

---

## Updating the App

For version 1.0.1:
1. Update version in `installer.iss` (line 5)
2. Run `build_release.bat`
3. Create new GitHub release with tag `v1.0.1`
4. Upload new installer

---

## Tips

### Professional Release Page
- Add screenshots to release description
- Include a video demo
- List known issues
- Add changelog

### File Naming
- Keep consistent: `AccesiGesture-Setup-v1.0.0.exe`
- Include version number
- Users know what they're downloading

### Release Frequency
- Bug fixes: Patch version (1.0.1)
- New features: Minor version (1.1.0)
- Major changes: Major version (2.0.0)

---

## Troubleshooting

### "Inno Setup not found"
Install from: https://jrsoftware.org/isdl.php

### Build fails
Check that all dependencies are installed:
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Installer too large
Normal size is 150-250MB due to MediaPipe and OpenCV

---

## What Users Get

✅ Professional Windows installer
✅ Start Menu shortcuts
✅ Desktop icon (optional)
✅ Proper uninstaller
✅ No Python required
✅ No manual setup
✅ One-click install

**Perfect for GitHub Releases!** 🎉
