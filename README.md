# AccesiGesture - Hand Gesture Control for Windows

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()
[![Latest Release](https://img.shields.io/github/v/release/dlt87/Accesigesture)](https://github.com/dlt87/Accesigesture/releases)
[![HackCamp 2025](https://img.shields.io/badge/HackCamp-2025-orange.svg)](https://www.nwplus.io/)

Control your computer with hand gestures using your webcam! A low-latency, customizable gesture control system powered by MediaPipe.

> 🏆 **Built at HackCamp 2025** by [nwPlus](https://www.nwplus.io/) - A hackathon project focused on accessibility and hands-free computing.

## ✨ Features

- 🖱️ **Move Cursor** - Control cursor with open hand
- 👆 **Click Actions** - Pinch for left click, configurable hold duration  
- 🖱️ **Right Click** - Custom gesture for right-click
- ⬆️⬇️ **Scroll** - Thumbs up/down for scrolling
- ⏸️ **Toggle Control** - Pause/resume gestures on the fly
- 🎛️ **Real-time Settings** - Adjust all parameters without restarting
- 🔄 **Gesture Remapping** - Assign any gesture to any action
- 🔒 **Window Lock** - Click-through camera overlay option
- ⚡ **Low Latency** - Optimized for real-time performance (~30-50ms)

## 📋 Requirements

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.11 or higher (for source)
- **Webcam**: Any USB or built-in camera
- **RAM**: 4GB minimum, 8GB recommended

## 🚀 Quick Start

### Option 1: Portable Executable (Recommended)
1. Download the latest release from [Releases](https://github.com/dlt87/Accesigesture/releases/latest)
2. Extract `AccesiGesture-vX.X.X-Portable.zip`
3. Run `AccesiGesture.exe`
4. Allow camera access when prompted

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/dlt87/Accesigesture.git
cd Accesigesture

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🎮 Gesture Guide

| Gesture | Default Action | Description |
|---------|----------------|-------------|
| ✋ **Open Hand** | Move Cursor | All fingers extended |
| 👌 **Pinch** | Left Click | Thumb + Index finger touch |
| 🤌 **Pinch Middle** | Right Click | Thumb + Middle finger touch |
| 👍 **Thumbs Up** | Scroll Up | Only thumb extended, pointing up |
| 👎 **Thumbs Down** | Scroll Down | Only thumb extended, pointing down |
| 🤙 **Toggle** | Pause/Resume | Thumb + Index + Pinky extended |

**Pro Tip**: Hold pinch for 0.15s (adjustable) to enable click-and-drag mode!

## ⚙️ Settings

Access the settings panel to customize:

### 🖱️ Cursor Settings
- **Smoothing Factor** (0.0-1.0): Higher = more responsive, lower = smoother
- **Presets**: Quick options (Smooth, Balanced, Responsive)
- **ROI Boundaries**: Define tracking area on screen

### 👆 Gesture Thresholds
- **Pinch Threshold**: Sensitivity for click detection
- **Pinch Duration**: Hold time before drag mode activates (default: 0.15s)
- **Fist Cooldown**: Delay between right-click actions
- **Scroll Speed**: Adjust scroll distance

### 🔍 Hand Detection
- **Detection Confidence**: Initial hand detection threshold
- **Tracking Confidence**: Continuous tracking sensitivity

### 🔄 Action Mapping
Customize any gesture to perform any action via dropdown menus in the settings window.



## 🐛 Troubleshooting

### Camera Not Working
- Check camera permissions in Windows Settings
- Ensure no other app is using the camera
- Try changing `cv2.VideoCapture(0)` to `(1)` in main.py

### High Latency / Lag
- Lower camera resolution (already optimized to 320x240)
- Increase smoothing factor in settings
- Close other resource-heavy applications
- Ensure good lighting conditions

### Gestures Not Detected
- Ensure good lighting conditions
- Position hand within camera frame
- Adjust detection confidence sliders
- Keep hand between 30-60cm from camera
- Use plain background for better detection

### Window Overlap Issues
- Windows are automatically positioned on startup
- Camera window: Top-left (20, 20)
- Settings window: Top-right with margins
- Use "Lock Window" feature for click-through camera view

## 📊 Performance Tips

- **Optimal Distance**: 30-60cm from camera
- **Lighting**: Bright, even lighting works best
- **Background**: Plain backgrounds improve detection
- **Hand Position**: Keep entire hand visible in frame
- **CPU Usage**: ~5-10% on modern processors

## 🗺️ Roadmap

- [ ] Multi-hand gesture support
- [ ] Custom gesture recording
- [ ] Gesture profiles/presets
- [ ] Cross-platform support (Linux, macOS)
- [ ] Voice command integration
- [ ] Eye tracking integration
- [ ] Accessibility features for motor disabilities

## 🙏 Acknowledgments

- **HackCamp 2025** - Created during the [nwPlus HackCamp 2025](https://www.nwplus.io/) hackathon
- [MediaPipe](https://mediapipe.dev/) - Hand tracking and gesture recognition
- [OpenCV](https://opencv.org/) - Computer vision processing
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Mouse and keyboard control
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/dlt87/Accesigesture/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dlt87/Accesigesture/discussions)
- **Latest Release**: [Download](https://github.com/dlt87/Accesigesture/releases/latest)

## 🌟 Version History

- **v1.0.1** - (Official Hackathon Submission) UI improvements, pinch duration slider, window positioning
- **v1.0.0** - Initial release with core gesture control features

---

**Made with ❤️ for accessibility and hands-free computing**  
**Built at HackCamp 2025 by [nwPlus](https://www.nwplus.io/)**
