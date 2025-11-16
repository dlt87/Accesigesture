# gestures/leftclick.py
import pyautogui

def left_click_down():
    """Presses and holds the left mouse button."""
    pyautogui.mouseDown(button='left')


def left_click_up():
    """Releases the left mouse button."""
    pyautogui.mouseUp(button='left')
 

def left_click_single():
    """Performs a single click."""
    pyautogui.click(button='left')
    