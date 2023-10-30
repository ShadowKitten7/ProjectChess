from MainGame import MainGame, game_constants,checkRequirements
import pygame
import random
from Auth import Auth
pygame.display.set_caption("Chess")
pygame.init()
checkRequirements()
screen=pygame.display.set_mode(game_constants().screenSize())
auth = Auth(screen,'users.txt')
def convert(x, y):
    return (ord(x) - ord("a"), int(y) - 1)


def convertMove(p1, p2):
    return convert(p1[0], p1[1]) + convert(p2[0], p2[1])

def playMoves(moves,game):
    game.turbo()
    for move in moves:
        m = convertMove(move[0], move[1])
        game.makeMove((m[0], 7 - m[1]), (m[2], 7 - m[3]))
    game.turbo(False)
users=auth.mainLoop()

if users is not None:
    r=random.randint(0,1)
    game = MainGame(screen, users[r], users[1-r])
    moves=[('d2', 'd4'), ('e7', 'e5'), ('d4', 'e5'), ('g8', 'f6')]
    moves=game.playGame()
    for move in moves:
        print('\t'.join(move))
