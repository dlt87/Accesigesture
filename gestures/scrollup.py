import pyautogui

def scroll_up():
  """
  Scrolls the mouse wheel up.
  The positive value (30) with frame throttling provides smooth scrolling.
  """
  pyautogui.scroll(30)
  print("Action: Scroll Up") # For debugging