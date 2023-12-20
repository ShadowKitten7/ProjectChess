from GameGUI import MainGame, game_constants,checkRequirements
import pygame
import random
from Auth import Auth
pygame.display.set_caption("Chess")
pygame.init()
checkRequirements()
screen=pygame.display.set_mode(game_constants().screenSize())
auth = Auth(screen,'users.txt')
users=auth.mainLoop()

if users is not None:
    r=random.randint(0,1)
    game = MainGame(screen, users[r], users[1-r])
    game.playGame()
