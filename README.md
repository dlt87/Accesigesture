# Accesigesture

Hand gesture control system with real-time adjustable settings.

## Features

- **Settings Window**: Real-time control panel for all important parameters
- **Cursor Control**: Move cursor with open hand gesture
- **Click Gestures**: Pinch for left-click, fist for right-click
- **Scroll Gestures**: Thumbs up/down for scrolling
- **Program Toggle**: Custom gesture to pause/resume

## Settings Window Controls

The settings window opens automatically when you run the program and includes:

### Cursor Settings
- **Smoothing Factor** (0.0 - 1.0): Higher = more responsive, Lower = smoother
- **ROI X/Y Min/Max**: Define the tracking area bounds

### Gesture Settings
- **Pinch Threshold**: Distance to trigger left-click
- **Fist Cooldown**: Time between right-click actions
- **Scroll Speed**: Speed of scroll gestures

### Hand Detection
- **Detection Confidence**: Confidence to detect hand initially
- **Tracking Confidence**: Confidence to track hand continuously

## Usage

```bash
python main.py
```

The settings window will appear alongside the gesture detector window. Adjust settings in real-time while the program runs!