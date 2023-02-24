from Square import Square
from Piece import Piece, PieceColour, PieceType

"""
The Board holds the 64 squares, and all the pieces
It controls piece movements, and decides whether a given move is valid or not, taking into account the piece in question
It handles all the logistics of the movements and positions of pieces, promotion etc
"""


class Board:
    def __init__(self):
        self.board = []  # 2D list with 8 rows and 8 columns, holds squares
        self.promotionOptions = [
            [],
            [],
        ]  # Holds the set of Piece objects that are options for pawn promotion
        # First sublist is for the black pieces, second for the white
        # Used in the MainGame class
        for x in range(8):  # create the sqares
            l = []
            for y in range(8):
                l.append(Square(x, y))
            self.board.append(l)
        # Set up the pawns
        for x in range(8):
            self.addPiece(x, 1, PieceColour.White, PieceType.Pawn)
            self.addPiece(x, 6, PieceColour.Black, PieceType.Pawn)
        pieceTypes = [
            PieceType.Rook,
            PieceType.Knight,
            PieceType.Bishop,
            PieceType.Queen,
        ]
        # Set up the Rook, Bishop and Knight
        for i in range(3):
            self.addPiece(i, 0, PieceColour.White, pieceTypes[i])
            self.addPiece(7 - i, 0, PieceColour.White, pieceTypes[i])
            self.addPiece(i, 7, PieceColour.Black, pieceTypes[i])
            self.addPiece(7 - i, 7, PieceColour.Black, pieceTypes[i])
        # Set up the Kings and Queens
        self.addPiece(3, 0, PieceColour.White, PieceType.Queen)
        self.addPiece(4, 0, PieceColour.White, PieceType.King)
        self.addPiece(3, 7, PieceColour.Black, PieceType.Queen)
        self.addPiece(4, 7, PieceColour.Black, PieceType.King)
        # Create and store the Piece objects into promotionOptions
        # In the order Rook,Knight,Bishop,Queen for both black and white
        for i in pieceTypes:
            self.promotionOptions[0].append(Piece(PieceColour.Black, i))
            self.promotionOptions[1].append(Piece(PieceColour.White, i))

    def getPiece(self, x, y):  # returns the piece on the square at x,y
        return self.board[x][y].piece

    def getSquare(self, x, y):  # Returns the square at x,y
        return self.board[x][y]

    def addPiece(
        self, x, y, colour, type
    ):  # Adds a piece of the specified colour and type on the square at x,y
        self.board[x][y].addPiece(Piece(colour, type))

    def removePiece(self, x, y):  # Removes and returns the piece at x,y
        return self.board[x][y].removePiece()

    def validSquare(
        self, x, y
    ):  # checks whether the position x,y is within the board or not
        return 0 <= x < 8 and 0 <= y < 8

    """
    Once a move has been judged valid, executes the move
    
    starting location = (x1,y1)
    ending location = (x2,y2)
    """

    def makeMove(self, x1, y1, x2, y2):
        startPos = self.getSquare(x1, y1)
        endPos = self.getSquare(x2, y2)
        p = startPos.removePiece()  # Pick up the piece at starting location
        p2 = endPos.removePiece()  # Pick up the piece at ending location(if present)
        endPos.addPiece(
            p
        )  # Place the piece that was on the starting location on the ending location
        return p2  # Return the captured piece

    def promotionCheck(
        self, x, y
    ):  # Check if the move that ends at x,y qualifies for promotion
        # i.e if a pawn has been moved to the opposite side
        # Called after the move has been made
        p = self.getPiece(x, y)
        return (p.colour.name == "White" and p.type.name == "Pawn" and y == 7) or (
            p.colour.name == "Black" and p.type.name == "Pawn" and y == 0
        )

    """
    Starting from startPos, moves along the specified direction one square at a time
    If the search reaches endPos, return True
    Else, if there is some obstruction, or endPos is occupied by a piece that cannot be captured,
    return False
    
    xDir,yDir specify how much the search moves along x and y in one step
    Eg: if both are 1, the search proceeds towards the top right
    """

    def beam(self, startPos, endPos, xDir, yDir):
        if self.validSquare(startPos.x, startPos.y):
            p = [startPos.x + xDir, startPos.y + yDir]
            while self.validSquare(p[0], p[1]):
                if (p[0] == endPos.x and p[1] == endPos.y) and (
                    endPos.piece == None or startPos.piece.colour != endPos.piece.colour
                ):
                    return True
                if self.getPiece(p[0], p[1]) != None:
                    return False
                p[0] += xDir
                p[1] += yDir
        return False

    """
    Once the position x,y has been determined to be a promotion square, and the user has picked the promotion piece
    Replace the pawn with the required piece of the same colour
    """

    def promote(self, x, y, type):
        p = self.getSquare(x, y).removePiece()
        match type:
            case 0:
                self.addPiece(x,y,p.colour,PieceType.Queen)
            case 1:
                self.addPiece(x,y,p.colour,PieceType.Bishop)
            case 2:
                self.addPiece(x,y,p.colour,PieceType.Knight)
            case 3:
                self.addPiece(x,y,p.colour,PieceType.Rook)
        return self.getPiece(x,y)!=None
    """
    Main entry point for checking validity of a proposed move
    x1,y1 is starting position
    x2,y2 is ending position
    """


    def validMove(self, x1, y1, x2, y2):
        startPos = self.getSquare(x1, y1)
        endPos = self.getSquare(x2, y2)
        if startPos.piece == None:  # If startin square is empty, invalid
            return False
        return self.validityHandler(startPos, endPos)


    """
    Directs flow of control towards the appropriate function depending on piece type
    """


    def validityHandler(self, startPos, endPos):
        match startPos.piece.type.name:
            case 'Bishop':
                return self.BishopMove(startPos,endPos)
            case 'Rook':
                return self.RookMove(startPos,endPos)
            case 'Knight':
                return self.KnightMove(startPos,endPos)
            case 'Queen':
                return self.QueenMove(startPos,endPos)
            case 'King':
                return self.KingMove(startPos,endPos)
            case 'Pawn':
                return self.PawnMove(startPos,endPos)
        return False#If none of the cases activate
    """
    Checks in all 4 diagonals using beam
    If the move is found to be valid, True, else False is returned
    """


    def BishopMove(self, startPos, endPos):
        for xDir in -1, 1:
            for yDir in -1, 1:
                if self.beam(startPos, endPos, xDir, yDir):
                    return True
        return False


    """
    Checks in all 4 straight lines(vertical and horizontal)
    If the move is found to be valid, True, else False is returned
    """


    def RookMove(self, startPos, endPos):
        for dir in -1, 1:
            if self.beam(startPos, endPos, dir, 0):
                return True
            if self.beam(startPos, endPos, 0, dir):
                return True
        return False


    def KnightMove(self, startPos, endPos):
        # First taking absolute of difference in x and y of start and end
        # If either one is 1 and the other is 2, it is a valid knight move
        # Hence, multiply the absolute differences and check if its equal to 2
        d = abs(startPos.x - endPos.x) * abs(startPos.y - endPos.y)
        if d == 2:
            return (endPos.piece == None) or (endPos.piece.colour != startPos.piece.colour)
        return False


    def KingMove(self, startPos, endPos):
        # Taking absolute difference of x and y between start and end
        # Either both are 1, or one is 1 and the other is 0
        # hence either product is 1 or sum is 1
        xDiff = abs(startPos.x - endPos.x)
        yDiff = abs(startPos.y - endPos.y)
        if xDiff + yDiff == 1 or xDiff * yDiff == 1:
            return endPos.piece == None or endPos.piece.colour != startPos.piece.colour
        return False


    """
    Checks in all 4 straight lines(vertical and horizontal) as well as all 4 diagonals using beam
    If the move is found to be valid, True, else False is returned
    """


    def QueenMove(self, startPos, endPos):
        for xDir in -1, 0, 1:
            for yDir in -1, 0, 1:
                if self.beam(startPos, endPos, xDir, yDir):
                    return True
        return False


    def PawnMove(self, startPos, endPos):
        xDiff = endPos.x - startPos.x
        yDiff = endPos.y - startPos.y
        if (
            startPos.piece.colour == PieceColour.White
        ):  # If white, can only move in +ve y dir
            if xDiff == 0:  # Straight
                if (
                    yDiff == 1 and endPos.piece == None
                ):  # moving one square, target square empty
                    return True
                if (
                    yDiff == 2
                    and startPos.y == 1
                    and endPos.piece == None
                    and self.getPiece(startPos.x, startPos.y + 1) == None
                ):
                    # At starting position, moving 2 squares, both squares one ahead and target square empty
                    return True
            elif abs(xDiff) == 1 and yDiff == 1:  # Capturing diagonally
                if endPos.piece == None:  # Invalid if the target is empty
                    return False
                if (
                    endPos.piece.colour == PieceColour.Black
                ):  # Valid only if the target has a Black piece
                    return True

        else:  # Black, can only move in -ve y dir
            if xDiff == 0:  # Straight
                if yDiff == -1 and endPos.piece == None:  # Moving 1 step
                    return True
                if (
                    yDiff == -2
                    and startPos.y == 6
                    and endPos.piece == None
                    and self.getPiece(startPos.x, startPos.y - 1) == None
                ):
                    # 2 steps at starting location, both squares one ahead and the target square are empty
                    return True
            elif abs(xDiff) == 1 and yDiff == -1:  # Capturing
                if endPos.piece == None:  # Invalid if target is empty
                    return False
                if (
                    endPos.piece.colour == PieceColour.White
                ):  # Valid only if the target has a black piece
                    return True
        return False  # No check was successful, invalid move
