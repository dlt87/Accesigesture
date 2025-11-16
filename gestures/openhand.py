import pyautogui
import numpy as np
import mediapipe as mp

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Smoothing variables
prev_x, prev_y = 0, 0

def move_cursor(hand_landmarks, settings):
    """
    Moves the cursor based on the position of the hand.
    Uses the wrist as the reference point.
    """
    global prev_x, prev_y
    
    # Get wrist position (landmark 0)
    lms = hand_landmarks.landmark
    wrist = lms[0]  # Wrist
    
    # Get ROI settings from settings window
    roi_x_min = settings.roi_x_min
    roi_x_max = settings.roi_x_max
    roi_y_min = settings.roi_y_min
    roi_y_max = settings.roi_y_max
    smoothing_factor = settings.smoothing_factor

    
    
    # Clamp values to ROI
    x_normalized = max(roi_x_min, min(roi_x_max, wrist.x))
    y_normalized = max(roi_y_min, min(roi_y_max, wrist.y))
    
    # Map ROI to full screen (0 to screen width/height)
    x = int((x_normalized - roi_x_min) / (roi_x_max - roi_x_min) * screen_width)
    y = int((y_normalized - roi_y_min) / (roi_y_max - roi_y_min) * screen_height)
    
    # Apply smoothing to reduce jitter
    if prev_x == 0 and prev_y == 0:
        # First frame - initialize
        prev_x, prev_y = x, y
    
    # Smooth the movement using exponential moving average
    smooth_x = prev_x * (1 - smoothing_factor) + x * smoothing_factor
    smooth_y = prev_y * (1 - smoothing_factor) + y * smoothing_factor
    
    # Update previous position
    prev_x, prev_y = smooth_x, smooth_y
    
    # Move the cursor directly without integer conversion until the end
    # This preserves sub-pixel precision for smoother movement
    pyautogui.moveTo(int(smooth_x), int(smooth_y), duration=0, _pause=False)
