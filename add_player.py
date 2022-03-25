





import pygame
import functools
from player import Character

pygame.init()

def func1():
    print("ok")

def funcneed(number):
    print(number)

dictr = {
        'funcs': func1,
        'funcr': functools.partial(funcneed, 10) 
        }

for i in dictr:
    print(dictr[i]())

