class Square:  # Represents each square
    def __init__(
        self, x, y
    ):  # Each square knows its location (x,y), its colour and the piece on it
        self.x = x
        self.y = y
        self.colour = int((x + y) % 2 == 1)
        self.piece = None

    def addPiece(self, piece):  # Place the given piece on the square
        self.piece = piece

    def removePiece(self):  # remove and return the piece on the square
        piece = self.piece
        self.piece = None
        return piece

    def __str__(self):  # String representation of the square, displays location
        return str(self.x) + "," + str(self.y)
