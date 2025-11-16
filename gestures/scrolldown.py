import pyautogui

def scroll_down():
  """
  Scrolls the mouse wheel down.
  The negative value (-30) with frame throttling provides smooth scrolling.
  """
  pyautogui.scroll(-30)
  print("Action: Scroll Down (Thumbs Down)") # For debugging