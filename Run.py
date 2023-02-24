from MainGame import MainGame, constants
import pygame
pygame.display.set_caption("Chess")
whitePlayer = ["White_Player",'', 1000]
blackPlayer = ["Black_Player",'', 1520]
pygame.init()
screen=pygame.display.set_mode(constants().screenSize())
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

moves=[('d2', 'd4'), ('e7', 'e5'), ('d4', 'e5'), ('f7', 'f6'), ('e5', 'f6'), ('f8', 'e7'), ('f6', 'g7'), ('g8', 'f6'), ('g7', 'h8'), ('f6', 'e4')]
#playMoves(moves)
game.playGame()
