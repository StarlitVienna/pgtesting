





from control import Control
from tools import screen, screen_size
import pyautogui

fullscreen = False
print(screen_size)
monitor_size = (pyautogui.size()[0], pyautogui.size()[1])
game = Control(fullscreen, 'hard', screen_size, screen)
game.run()
