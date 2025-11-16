# import important libraries
import cv2
import mediapipe as mp
import math
import time
import pyautogui
import tkinter as tk # Import tkinter for the StringVar type

from gestures import rightclick
from gestures import openhand
from gestures import scrollup
from gestures import scrolldown
from gestures import leftclick
from settings_window import SettingsWindow

pyautogui.FAILSAFE = False

# create settings window
settings = SettingsWindow()
settings.create_window()

# --- Action Function Dictionary ---
AVAILABLE_ACTIONS = {
    "None": (lambda: None),
    "Left Click (Hold)": leftclick.left_click_down,
    "Left Click (Release)": leftclick.left_click_up, 
    "Right Click (Once)": rightclick.rightclick,
    "Scroll Up": (lambda: scrollup.scroll_up(settings.scroll_speed)),
    "Scroll Down": (lambda: scrolldown.scroll_down(settings.scroll_speed)),
    "Move Cursor": (lambda hand_landmarks: openhand.move_cursor(hand_landmarks, settings))
}

# --- Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=settings.min_detection_confidence, 
    min_tracking_confidence=settings.min_tracking_confidence
)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
pyautogui.PAUSE = 0 

# --- Gesture State Tracking ---
last_fist_action_time = 0
last_gesture = None 
scroll_frame_counter = 0 
SCROLL_EVERY_N_FRAMES = 2 
pinch_active = False 
debug = True
program_active = True 
pointer_was_up = False 
window_name = "accessiGesture"

# --- Helper Functions (No changes needed) ---
def get_distance(lm1, lm2):
    return math.hypot(lm1.x - lm2.x, lm1.y - lm2.y)

def get_hand_label(index, hand, results):
    label = None
    if results.multi_handedness:
        classification = results.multi_handedness[index]
        if classification.classification:
            label = classification.classification[0].label
    return label

def get_finger_states(hand_landmarks):
    if hand_landmarks is None: return None
    fingers = []
    lms = hand_landmarks.landmark
    wrist_lm = lms[mp_hands.HandLandmark.WRIST]
    tip_ids = [
        mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    pip_ids = [
        mp_hands.HandLandmark.THUMB_IP, mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP, mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]
    tip_dist = get_distance(lms[tip_ids[0]], wrist_lm)
    pip_dist = get_distance(lms[pip_ids[0]], wrist_lm)
    fingers.append(1 if tip_dist > pip_dist else 0)
    for i in range(1, 5):
        tip_dist = get_distance(lms[tip_ids[i]], wrist_lm)
        pip_dist = get_distance(lms[pip_ids[i]], wrist_lm)
        fingers.append(1 if tip_dist > pip_dist else 0)
    return fingers

def is_thumbs_up(hand_landmarks, fingers_list):
    if fingers_list != [1, 0, 0, 0, 0]: return False
    lms = hand_landmarks.landmark
    return lms[4].y < lms[2].y - 0.05

def is_thumbs_down(hand_landmarks, fingers_list):
    if fingers_list != [1, 0, 0, 0, 0]: return False
    lms = hand_landmarks.landmark
    return lms[4].y > lms[2].y + 0.05

def is_pinch(hand_landmarks, threshold=0.05):
    lms = hand_landmarks.landmark
    thumb_tip = lms[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = lms[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = get_distance(thumb_tip, index_tip)
    return distance < threshold

def is_pinch_mid(hand_landmarks, threshold=0.05):
    lms = hand_landmarks.landmark
    thumb_tip = lms[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = lms[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    distance = get_distance(thumb_tip, index_tip)
    return distance < threshold

# --- Main Loop ---
while cap.isOpened():
    success, image = cap.read()
    if not success: continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    gesture_detected = "None" 
    action_to_perform = "None" 

    if results.multi_hand_landmarks:
        for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_list = get_finger_states(hand_landmarks) 
            if fingers_list is None: continue
            
            lms = hand_landmarks.landmark
            current_time = time.time()
            
            # --- 1. DETECT GESTURE ---
            if is_pinch(hand_landmarks, settings.pinch_threshold):
                gesture_detected = "PINCH"
            elif is_pinch_mid(hand_landmarks, settings.pinch_threshold):
                gesture_detected = "PINCH_MID"
            elif is_thumbs_up(hand_landmarks, fingers_list):
                gesture_detected = "THUMBS_UP"
            elif is_thumbs_down(hand_landmarks, fingers_list):
                gesture_detected = "THUMBS_DOWN"
            elif fingers_list == [1, 1, 1, 1, 1]:
                gesture_detected = "OPEN"
            elif fingers_list == [1, 1, 0, 0, 1]:
                gesture_detected = "TOGGLE" 

            # --- 2. GET CURRENT MAPPINGS ---
            current_mappings = {}
            if settings.action_mappings: # Check if UI is ready
                for action, var in settings.action_mappings.items():
                    current_mappings[action] = var.get() # e.g., {"Left Click (Hold)": "PINCH", ...}
            
            # --- 3. HANDLE TOGGLE (ALWAYS) ---
            if gesture_detected == "TOGGLE":
                if not pointer_was_up:
                    program_active = not program_active
                    pointer_was_up = True
                    status = "ACTIVE" if program_active else "PAUSED"
                    print(f"Program {status}")
            else:
                pointer_was_up = False
                
            # --- 4. EXECUTE ACTIONS (if active) ---
            if program_active and gesture_detected != "TOGGLE":

                # --- THIS IS THE NEW LOGIC ---
                
                # We now check for actions separately to allow combos.
                
                # --- Part A: Check for Mouse Movement ---
                move_gesture = current_mappings.get("Move Cursor", "None")
                if gesture_detected == move_gesture:
                    action_function = AVAILABLE_ACTIONS.get("Move Cursor")
                    if action_function:
                        action_function(hand_landmarks)
                    action_to_perform = "Move Cursor" # For debug display

                # --- Part B: Check for Left Click (Hold/Drag) ---
                click_hold_gesture = current_mappings.get("Left Click (Hold)", "None")
                if gesture_detected == click_hold_gesture:
                    action_to_perform = "Left Click (Hold)" # For debug display
                    if not pinch_active:
                        # Call the action function
                        action_function = AVAILABLE_ACTIONS.get("Left Click (Hold)")
                        if action_function:
                            action_function()
                        pinch_active = True
                    
                    # *** THE FIX ***
                    # WHILE click is held, ALSO check for mouse movement
                    # This allows click-and-drag
                    move_action_func = AVAILABLE_ACTIONS.get("Move Cursor")
                    if move_action_func:
                        move_action_func(hand_landmarks)
                    # *** END FIX ***

                # --- Part C: Check for Other Discrete Actions ---
                # (This part handles actions that are *not* movement or click-hold)
                else:
                    # Find which action (if any) is mapped to our detected gesture
                    for action_name, gesture_name in current_mappings.items():
                        if gesture_name == gesture_detected:
                            # We only care about non-move, non-hold actions here
                            if action_name not in ["Move Cursor", "Left Click (Hold)"]:
                                action_to_perform = action_name
                                break
                    
                    action_function = AVAILABLE_ACTIONS.get(action_to_perform)
                    
                    if action_function:
                        if action_to_perform == "Right Click (Once)":
                            if current_time - last_fist_action_time > settings.fist_cooldown:
                                action_function()
                                last_fist_action_time = current_time
                                
                        elif action_to_perform in ["Scroll Up", "Scroll Down"]:
                            if scroll_frame_counter % SCROLL_EVERY_N_FRAMES == 0:
                                action_function()
                                
                        elif action_to_perform == "None":
                            pass
            
            # --- END OF NEW LOGIC ---

            # --- Display Debug Info ON SCREEN ---
            if debug:
                cv2.putText(image, f"Gesture: {gesture_detected}", (10, 50), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.putText(image, f"Action: {action_to_perform}", (10, 90), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.putText(image, f"Fingers: {fingers_list}", (10, 130), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                hand_label = get_hand_label(hand_index, hand_landmarks, results)
                cv2.putText(image, f"Hand: {hand_label}", (10, 250), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    # --- Part D: Handle Click Release ---
    # Get the gesture mapped to "Left Click (Hold)"
    if 'current_mappings' in locals(): # Ensure mappings are loaded
        click_hold_gesture = current_mappings.get("Left Click (Hold)", "None")
        if gesture_detected != click_hold_gesture and pinch_active:
            AVAILABLE_ACTIONS["Left Click (Release)"]()
            pinch_active = False

    # Increment frame counter
    scroll_frame_counter += 1
    
    # Display program state
    state_text = "ACTIVE" if program_active else "PAUSED"
    state_color = (0, 255, 0) if program_active else (0, 0, 255) 
    cv2.putText(image, f"Program: {state_text}", (10, 30), 
                cv2.FONT_HERSHEY_PLAIN, 2, state_color, 3)

    cv2.imshow(window_name, image)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    
    # Safer visibility check
    try:
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
    except cv2.error:
        break

cap.release()
cv2.destroyAllWindows()