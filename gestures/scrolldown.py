import pyautogui

def scroll_down(speed=3):
  """
  Scrolls the mouse wheel down.
  The negative value with frame throttling provides smooth scrolling.
  """
  pyautogui.scroll(-speed * 10)