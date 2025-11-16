import pyautogui

def scroll_up(speed=3):
  """
  Scrolls the mouse wheel up.
  The positive value with frame throttling provides smooth scrolling.
  """
  pyautogui.scroll(speed * 10)
  print("Action: Scroll Up") # For debugging