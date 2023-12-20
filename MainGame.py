from Game import Board
import pygame
import time
import io
import os
from datetime import timedelta
import pickle
import pygame.freetype
class game_constants:
    def __init__(self) -> None:
        self.scale = 70  # Size of each square(pixels)
        self.timeToMove = 0.2  # seconds
        self.white = (255, 253, 208)  # colour to display for white squares
        self.black = (14, 119, 14)  # colour to display for black squares
        self.border = (192, 192, 192)  # Border colour
        self.highlight = (255, 0, 0)  # colour of highlight for squares in focus
        self.padding = self.scale//8  # spacing between screen edge and board(pixels)
        self.piece_size = 0.8 * self.scale
        self.label_space = self.scale // 2
        self.right_panel = self.scale * 3 // 2
        self.icon = (self.scale//4, self.scale//4, (0, 0, 0), self.white)
        self.nameSpace = self.scale*5//8
        self.icon_border = (self.scale//40, (255, 165, 0))
        self.promote_colour = (160, 160, 100)
        self.gameOver_colour=(150,150,150)
        self.turbo_amount = 0.6

    def screenSize(self):
        return (
            self.scale * 8 + 2 * self.padding + self.label_space + self.right_panel,
            self.scale * 8 + 2 * self.padding + self.label_space + 2 * self.nameSpace,
        )

class State:
    def __init__(self,gameObject):
        self.board=gameObject.board.board
        self.whitePlayer=gameObject.whitePlayer
        self.blackPlayer=gameObject.blackPlayer
        self.moveList=gameObject.moveList
        self.whiteToPlay=gameObject.whiteToPlay
    def unwrap(self,gameObject):
        gameObject.board.board=self.board
        gameObject.whitePlayer=self.whitePlayer
        gameObject.blackPlayer=self.blackPlayer
        gameObject.moveList=self.moveList
        gameObject.whiteToPlay=self.whiteToPlay
    def saveState(self):
        with open('temp/state.bin','wb') as file:
            pickle.dump(self,file)
def checkRequirements():
    if not os.path.isdir('temp/'):
        os.mkdir('temp/')
        with open('temp/users.txt','x'):
            pass
        
def retrieveState(gameObject):
    try:
        with open('temp/state.bin','rb') as file:
            pickle.load(file).unwrap(gameObject)
        with open('temp/state.bin','wb') as file:
            pass
    except FileNotFoundError:
        return
    except EOFError:
        return
    
class MainGame:
    def __init__(self, screen, whitePlayer, blackPlayer) -> None:
        self.board = Board()
        self.c = game_constants()
        self.pieceIcons = []
        self.font = pygame.freetype.Font("assets/sf-cartoonist-regular.ttf", self.c.scale*3//8)
        self.namefont = pygame.freetype.Font("assets/sf-cartoonist-bold.ttf", self.c.scale*3//8)
        self.screen = screen
        self.whitePlayer = whitePlayer
        self.blackPlayer = blackPlayer
        self.startPos = [-1, -1]  # start position for each piece, defualt is -1,-1
        self.endPos = [-1, -1]
        self.scaleFactor = self.c.piece_size / 45
        self.moveList = []
        self.loadPieces()  # load piece resources
        self.whiteToPlay = True
        self.promotionOngoing = False
        self.t = 300
        self.promotionSquare = [-1, -1]
        self.done=False
        self.render()

    def convertMove(self, startPos, endPos):
        x1, y1 = startPos[0], 7 - startPos[1]
        x2, y2 = endPos[0], 7 - endPos[1]
        p1 = chr(ord("a") + x1) + str(y1 + 1)
        p2 = chr(ord("a") + x2) + str(y2 + 1)
        self.moveList.append((p1, p2))

    def convertResource(self, src, scale=1.0):  # Resize and load each image
        svg_string = open(src, "rt",encoding='utf-8').read()
        start = svg_string.find("<svg")
        if start > 0:
            svg_string = (
                svg_string[: start + 4]
                + f' transform="scale({scale})" width="{45*scale}" height="{45*scale}"'
                + svg_string[start + 4 :]
            )
        return pygame.image.load(io.BytesIO(svg_string.encode()))

    def loadPieces(self):
        white = []
        white.append(self.convertResource("assets/White Pawn.svg", self.scaleFactor))
        white.append(self.convertResource("assets/White Knight.svg", self.scaleFactor))
        white.append(self.convertResource("assets/White Bishop.svg", self.scaleFactor))
        white.append(self.convertResource("assets/White Rook.svg", self.scaleFactor))
        white.append(self.convertResource("assets/White Queen.svg", self.scaleFactor))
        white.append(self.convertResource("assets/White King.svg", self.scaleFactor))
        self.pieceIcons.append(white)
        black = []
        black.append(self.convertResource("assets/Black Pawn.svg", self.scaleFactor))
        black.append(self.convertResource("assets/Black Knight.svg", self.scaleFactor))
        black.append(self.convertResource("assets/Black Bishop.svg", self.scaleFactor))
        black.append(self.convertResource("assets/Black Rook.svg", self.scaleFactor))
        black.append(self.convertResource("assets/Black Queen.svg", self.scaleFactor))
        black.append(self.convertResource("assets/Black King.svg", self.scaleFactor))
        self.pieceIcons.append(black)

    def xOffset(self, x=0):
        return x + self.c.padding + self.c.label_space
    def yOffset(self, y=0):
        return y + self.c.padding + self.c.nameSpace

    def showPiece(self, piece, x, y):
        colour = int(piece.colour.name != "White")
        img = None
        if piece.type.name == "Pawn":
            img = self.pieceIcons[colour][0]
        elif piece.type.name == "Knight":
            img = self.pieceIcons[colour][1]
        elif piece.type.name == "Bishop":
            img = self.pieceIcons[colour][2]
        elif piece.type.name == "Rook":
            img = self.pieceIcons[colour][3]
        elif piece.type.name == "Queen":
            img = self.pieceIcons[colour][4]
        elif piece.type.name == "King":
            img = self.pieceIcons[colour][5]
        else:
            return
        rect = img.get_rect()
        rect.center = (x, y)
        self.screen.blit(img, rect)  # Draw onto the screen
    def convertRect(self,rect,x,y):
        w,h=rect.width,rect.height
        return (self.xOffset(x-w//2),self.yOffset(y-h//2))
    def WinBanner(self):
        self.drawScreen()
        x,y=self.c.scale*5,self.c.scale*5//2
        pygame.draw.rect(self.screen,self.c.gameOver_colour,(self.xOffset((self.c.scale*8-x)//2),self.yOffset((self.c.scale*8-y)//2),x,y),x,x//35)
        text_rect=self.namefont.get_rect('GAME OVER')
        self.namefont.render_to(self.screen,self.convertRect(text_rect,self.c.scale*4,self.c.scale*4-y//4),'GAME OVER')
        winner='White' if self.whiteToPlay else 'Black'
        text_rect=self.namefont.get_rect(winner+' wins')
        self.namefont.render_to(self.screen,self.convertRect(text_rect,self.c.scale*4,self.c.scale*4),winner+' wins')
        
        pygame.display.update()
    def displayBoard(self):  # Show the board squares
        self.screen.fill(self.c.border)
        for x in range(8):
            for y in range(8):
                yPos = self.yOffset((7 - y) * self.c.scale)
                squareColour = (x+y)%2
                if squareColour == 1:
                    pygame.draw.rect(
                        self.screen,
                        self.c.white,
                        (
                            self.xOffset(x * self.c.scale),
                            yPos,
                            self.c.scale,
                            self.c.scale,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        self.c.black,
                        (
                            self.xOffset(x * self.c.scale),
                            yPos,
                            self.c.scale,
                            self.c.scale,
                        ),
                    )

    def xnor(self, a, b):
        return (a and b) or ((not a) and (not b))

    def snap(self, x, scale):
        return round(x * scale) / scale

    def displayPieces(self):  # Show the piecesf
        for x in range(8):
            for y in range(8):
                if self.board._isEmpty(x,y): continue
                yPos = self.yOffset((7 - y) * self.c.scale)
                self.showPiece(
                        self.board._getPiece(x,y),
                        self.xOffset(x * self.c.scale) + self.c.scale // 2,
                        yPos + self.c.scale // 2,
                    )

    def drawScreen(self):
        self.displayBoard()
        if self.startPos[0] != -1:
            pygame.draw.rect(
                self.screen,
                self.c.highlight,
                (
                    self.xOffset(self.startPos[0] * self.c.scale),
                    self.yOffset(self.startPos[1] * self.c.scale),
                    self.c.scale,
                    self.c.scale,
                ),
            )
        self.displayPieces()
        x = self.c.label_space // 2
        for i in range(8):
            y = self.yOffset(self.c.scale * (7 - i) + self.c.scale // 2)
            self.font.render_to(self.screen, (x, y), chr(49 + i))
        y = self.yOffset(self.c.scale * 8 + self.c.label_space // 2)
        for i in range(8):
            x = self.xOffset(i * self.c.scale + self.c.scale // 2)
            self.font.render_to(self.screen, (x, y), chr(65 + i))
        self.font.render_to(
            self.screen,
            (
                self.xOffset(8 * self.c.scale + self.c.padding),
                self.yOffset(self.c.scale * 4),
            ),
            "To Play:",
        )
        w = self.font.get_rect("To Play:").width
        pygame.draw.rect(
            self.screen,
            self.c.icon_border[1],
            (
                self.xOffset(
                    self.c.scale * 8 + 2 * self.c.padding + w - self.c.icon_border[0]
                ),
                self.yOffset(self.c.scale * 4 - self.c.icon_border[0]),
                self.c.icon[0] + 2 * self.c.icon_border[0],
                self.c.icon[1] + 2 * self.c.icon_border[0],
            ),
        )
        pygame.draw.rect(
            self.screen,
            self.c.icon[3] if self.whiteToPlay else self.c.icon[2],
            (
                self.xOffset(8 * self.c.scale + 2 * self.c.padding + w),
                self.yOffset(self.c.scale * 4),
                self.c.icon[0],
                self.c.icon[1],
            ),
        )
        t = self.whitePlayer[0] + "  [" + str(self.whitePlayer[1]) + "]"
        self.namefont.render_to(
            self.screen,
            (
                self.xOffset(self.c.scale),
                self.yOffset(8 * self.c.scale + self.c.padding + self.c.label_space),
            ),
            t,
        )
        t = self.blackPlayer[0] + "  [" + str(self.blackPlayer[1]) + "]"
        self.namefont.render_to(
            self.screen, (self.xOffset(self.c.scale), self.c.padding), t
        )

    def turbo(self, on=True):
        if on:
            self.c.timeToMove *= self.c.turbo_amount
        else:
            self.c.timeToMove /= self.c.turbo_amount
        self.c.timeToMove = round(self.c.timeToMove * 100) / 100

    def render(self):
        self.drawScreen()
        pygame.display.update()

    def promotionBanner(self, pos):
        colour = int(self.board._getPiece(pos[0], 7 - pos[1]).colour.name == "White")
        x, y = self.xOffset(pos[0] * self.c.scale + self.c.scale // 2), \
            self.yOffset(pos[1] * self.c.scale + self.c.scale //2
        )
        if colour == 0:
            y -= self.c.scale * 4
        for i in range(4):
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                (
                    x,
                    y + self.c.scale * i,
                    self.c.scale,
                    self.c.scale + self.c.icon_border[0],
                ),
            )
            pygame.draw.rect(
                self.screen,
                self.c.promote_colour,
                (
                    x + self.c.icon_border[0],
                    y + self.c.scale * i + self.c.icon_border[0],
                    self.c.scale - 2 * self.c.icon_border[0],
                    self.c.scale - self.c.icon_border[0],
                ),
            )
            px, py = x + self.c.scale // 2, y + self.c.scale * i + self.c.scale // 2
            self.showPiece(
                self.board.promotionOptions[colour][3 - i if colour == 1 else i], px, py
            )

    def Transition(self, startPos, endPos):
        startTime = time.monotonic()
        done = False
        speed = round(self.c.timeToMove * self.t)
        startPiece = self.board._removePiece(startPos[0], 7 - startPos[1])
        pos = [
            self.xOffset(startPos[0] * self.c.scale + self.c.scale // 2),
            self.yOffset(startPos[1] * self.c.scale + self.c.scale // 2),
        ]
        target = [
            self.xOffset(endPos[0] * self.c.scale + self.c.scale // 2),
            self.yOffset(endPos[1] * self.c.scale + self.c.scale // 2),
        ]
        dir = [(target[0] - pos[0]) / speed, (target[1] - pos[1]) / speed]
        while not done:
            self.drawScreen()
            self.showPiece(startPiece, pos[0], pos[1])
            pos[0] = self.snap(pos[0] + dir[0], speed)
            pos[1] = self.snap(pos[1] + dir[1], speed)

            pygame.display.update()
            if pos[0] == target[0] and pos[1] == target[1]:
                done = True
        self.board._setPiece(startPos[0], 7 - startPos[1],startPiece)
        endTime = time.monotonic()
        self.t = round(speed / timedelta(seconds=endTime - startTime).total_seconds())

    def end(self):
        if self.done:
            with open('temp/state.bin','wb'):
                pass
        else:
            state=State(self)
            state.saveState()
        
        return self.moveList

    def makeMove(self, startPos, endPos):
        piece = self.board._getPiece(
            startPos[0], 7 - startPos[1]
        )  # Piece at starting location
        if piece != None and self.xnor(
            piece.colour.name == "White", self.whiteToPlay
        ):  # Either white to move, and white selected or
            valid = self.board.handleMove(
                startPos[0], 7 - startPos[1], endPos[0], 7 - endPos[1]
            )  # Check for move validity after converting coordinates to board
            if valid:
                self.convertMove(startPos, endPos)
                self.Transition(startPos, endPos)
                p = self.board.makeMove(
                    startPos[0], 7 - startPos[1], endPos[0], 7 - endPos[1]
                )
                if p != None and p.type.name == "King":  # King captured
                    self.WinBanner()
                    self.done=True
                    return
                if self.board.promotionCheck(endPos[0], 7 - endPos[1]):
                    self.promotionOngoing = True
                    self.promotionSquare = endPos
                    self.drawScreen()
                    self.promotionBanner(self.promotionSquare)
                    pygame.display.update()
                else:
                    self.whiteToPlay = not self.whiteToPlay
        if not self.promotionOngoing and not self.done:
            self.render()

    def playGame(self,reload=False):
        if reload:
            retrieveState(self)
        self.render()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.end()
                if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse pressed
                    if self.done:
                        break
                    if self.promotionOngoing:
                        self.promotionBanner(self.promotionSquare)
                        pos = event.pos
                        x, y = pos[0] -self.xOffset()- self.c.scale // 2, pos[1] -self.yOffset()- self.c.scale // 2
                        y = abs(
                            y - self.c.padding - self.promotionSquare[1] * self.c.scale
                        )
                        if x > 0 and y > 0:
                            yIndex = y // self.c.scale
                            self.board.promote(
                                self.promotionSquare[0],
                                7 - self.promotionSquare[1],
                                yIndex
                            )
                            self.whiteToPlay = not self.whiteToPlay
                            self.promotionOngoing = False
                            self.startPos = [
                                -1,
                                -1,
                            ]  # Reset start and end positions, whether or not move was valid
                            self.endPos = [-1, -1]
                        self.drawScreen()
                        pygame.display.update()
                        break
                    if self.startPos[0] == -1:  # If first click after reset
                        self.startPos = list(event.pos)
                        self.startPos[0] = (
                            self.startPos[0] - self.xOffset()
                        ) // self.c.scale
                        self.startPos[1] = (
                            self.startPos[1] - self.yOffset()
                        ) // self.c.scale
                        if not (7>=self.startPos[0]>=0 and 7>=self.startPos[1]>=0):
                            self.startPos = [-1, -1]
                        # Set startPos to hold square coordinates according to representation on screen
                    else:
                        self.endPos = list(event.pos)
                        self.endPos[0] = (
                            self.endPos[0] - self.xOffset()
                        ) // self.c.scale
                        self.endPos[1] = (
                            self.endPos[1] - self.yOffset()
                        ) // self.c.scale
                        if self.endPos[0] < 0 or self.endPos[1] < 0:
                            self.endPos = [-1, -1]
                            break
                        # set endPos to hold square coordinates according to representation on screen
                        self.makeMove(self.startPos, self.endPos)
                        self.startPos = [-1, -1]  # Reset start and end positions, whether or not move was valid
                        self.endPos = [-1, -1]
                    if not self.promotionOngoing and not self.done:
                        self.render()
