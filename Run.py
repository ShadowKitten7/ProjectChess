from MainGame import MainGame, game_constants,checkRequirements
import pygame
from Auth import Auth
pygame.display.set_caption("Chess")
whitePlayer = ["White_Player",'', 1000]
blackPlayer = ["Black_Player",'', 1520]
pygame.init()
checkRequirements()
screen=pygame.display.set_mode(game_constants().screenSize())
auth = Auth(screen,'users.txt')
auth.mainLoop()
game = MainGame(screen, whitePlayer, blackPlayer)

def convert(x, y):
    return (ord(x) - ord("a"), int(y) - 1)


def convertMove(p1, p2):
    return convert(p1[0], p1[1]) + convert(p2[0], p2[1])

def playMoves(moves):
    game.turbo()
    for move in moves:
        m = convertMove(move[0], move[1])
        game.makeMove((m[0], 7 - m[1]), (m[2], 7 - m[3]))
    game.turbo(False)

moves=[('d2', 'd4'), ('e7', 'e5'), ('d4', 'e5'), ('g8', 'f6')]
playMoves(moves)
game.playGame()
