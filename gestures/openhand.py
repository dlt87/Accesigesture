import pyautogui
import numpy as np
import mediapipe as mp

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Smoothing variables
prev_x, prev_y = 0, 0
smoothing_factor = 0.2  # Lower = smoother but slower response (0-1)

def move_cursor(hand_landmarks):
    """
    Moves the cursor based on the position of the hand.
    Uses the wrist as the reference point.
    """
    global prev_x, prev_y
    
    # Get wrist position (landmark 0)
    lms = hand_landmarks.landmark
    wrist = lms[0]  # Wrist
    
    # Define a region of interest (ROI) for hand tracking
    # This maps a smaller hand movement area to the full screen
    roi_x_min, roi_x_max = 0.2, 0.8 
    roi_y_min, roi_y_max = 0.2, 0.8

    
    
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
    else:
        # Smooth the movement
        x = int(prev_x * (1 - smoothing_factor) + x * smoothing_factor)
        y = int(prev_y * (1 - smoothing_factor) + y * smoothing_factor)
    
    # Update previous position
    prev_x, prev_y = x, y
    
    # Move the cursor
    pyautogui.moveTo(x, y, duration=0)
    
    print(f"Cursor moved to: ({x}, {y})")
