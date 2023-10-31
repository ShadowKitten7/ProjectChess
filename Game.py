from enum import Enum
class PieceType(Enum):
    Pawn = "Pawn"
    Bishop = "Bishop"
    Rook = "Rook"
    Knight = "Knight"
    King = "King"
    Queen = "Queen"
    
class PieceColour(Enum):
    Black = "Black"
    White = "White"
    
class Piece:  # Represents each piece, each piece has a colour and type
    def __init__(self, colour:PieceColour, type:PieceType):
        self.colour = colour
        self.type = type
    def __str__(self):  # Return a string representation of the piece, the colour and type
        return str(self.colour.name) + " " + str(self.type.name)

class Board:
  def __init__(self) -> None:
    self.boardSize=8
    #Empty board
    self.board=[[None for i in range(self.boardSize)] for j in range(self.boardSize)]
    # (0,0) is considered to be the A1 square
    self._populate()
    self.toPlay=PieceColour.White
  def _isEmpty(self,x:int,y:int)-> bool:
    return self.board[x][y] is None
  def _getPiece(self,x:int,y:int) ->Piece:
    return self.board[x][y]
  def _setPiece(self,x:int,y:int,piece:Piece):
    self.board[x][y]=piece
  def _removePiece(self,x:int,y:int)->Piece:
    piece=self.board[x][y]
    self.board[x][y]=None
    return piece
  def getCode(self,x:int,y:int):
    return chr(ord('A')+y)+chr(ord('1')+x)
  def _populate(self):
    #Piece types from A to H
    types=[PieceType.Rook,PieceType.Knight,PieceType.Bishop,PieceType.Queen,PieceType.King]
    types.extend([PieceType.Bishop,PieceType.Knight,PieceType.Rook])
    for i in range(self.boardSize):
      #Pawns
      self._setPiece(i,1,Piece(PieceColour.White,PieceType.Pawn))
      self._setPiece(i,6,Piece(PieceColour.Black,PieceType.Pawn))
      #White pieces
      self._setPiece(i,0,Piece(PieceColour.White,types[i]))
      #Black pieces
      self._setPiece(i,7,Piece(PieceColour.Black,types[i]))
  def _boundsCheck(self,x:int,y:int):
    return 0 <= x < self.boardSize and 0 <= y < self.boardSize
  
  def beam(self,initialPos:tuple,finalPos:tuple,xDir:int,yDir:int):
    x,y=initialPos[0]+xDir,initialPos[1]+yDir;
    while self._boundsCheck(x,y):
      if (x,y)==finalPos:
        if self._isEmpty(finalPos[0],finalPos[1]): return True
        finalPiece = self._getPiece(finalPos[0],finalPos[1])
        initialPiece = self._getPiece(initialPos[0],initialPos[1])
        return initialPiece.colour != finalPiece.colour
      if not self._isEmpty(x,y):
        return False
      x,y=x+xDir,y+yDir
    return False
  
  def handleMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int) ->bool:
    if not self._boundsCheck(xInitial,yInitial): return False
    if not self._boundsCheck(xFinal,yFinal):return False
    if self._isEmpty(xInitial,yInitial):return False
    match 
  def display(self):
    for y in range(self.boardSize):
      print(self.boardSize-y-1,end='\t')
      for x in range(self.boardSize):
        print(self._getPiece(x,-y-1),end='\t')
      print()
    print(end='\t')
    for i in range(self.boardSize):
      print(i,end='\t  ')
    print()
board=Board()
board.display()