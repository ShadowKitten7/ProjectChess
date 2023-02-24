import enum


class Piece:  # Represents each piece, each piece has a colour and type
    def __init__(self, colour, type):
        self.colour = colour
        self.type = type

    def __str__(
        self,
    ):  # Return a string representation of the piece, the colour and type
        return str(self.colour.name) + " " + str(self.type.name)


class PieceType(enum.Enum):
    Pawn = "Pawn"
    Bishop = "Bishop"
    Rook = "Rook"
    Knight = "Knight"
    King = "King"
    Queen = "Queen"


class PieceColour(enum.Enum):
    Black = "Black"
    White = "White"
