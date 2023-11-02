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
        initialPiece = self._getPiece(initialPos[0],initialPos[1])
        finalPiece = self._getPiece(finalPos[0],finalPos[1])
        return initialPiece.colour != finalPiece.colour
      if not self._isEmpty(x,y):
        return False
      x,y=x+xDir,y+yDir
    return False
  
  def kingMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int) ->bool:
    xDiff = xInitial-xFinal
    yDiff = yInitial-yFinal
    if abs(xDiff*yDiff) in (0,1):
      initialPiece = self._getPiece(xInitial,yInitial)
      finalPiece = self._getPiece(xFinal,yFinal)
      return self._isEmpty(xFinal,yFinal) or initialPiece.colour!=finalPiece.colour
    return False
  
  def knightMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int) ->bool:
    xDiff = xInitial-xFinal
    yDiff = yInitial-yFinal
    if abs(xDiff*yDiff) == 2:
      initialPiece = self._getPiece(xInitial,yInitial)
      finalPiece = self._getPiece(xFinal,yFinal)
      return self._isEmpty(xFinal,yFinal) or initialPiece.colour!=finalPiece.colour
    return False
  def rookMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int) ->bool:
    for direction in -1,1:
      if self.beam((xInitial,yInitial),(xFinal,yFinal),0,direction):
        return True
      if self.beam((xInitial,yInitial),(xFinal,yFinal),direction,0):
        return True
    return False
  def bishopMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int) ->bool:
    for xDirection in -1,1:
      for yDirection in -1,1:
        if self.beam((xInitial,yInitial),(xFinal,yFinal),xDirection,yDirection):
          return True
    return False
  def queenMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int) ->bool:
    for xDirection in -1,0,1:
      for yDirection in -1,0,1:
        if self.beam((xInitial,yInitial),(xFinal,yFinal),xDirection,yDirection):
          return True
    return False
  def pawnMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int) ->bool:
    xDiff = xFinal-xInitial
    yDiff = yFinal-yInitial
    if self._getPiece(xInitial,yInitial).colour.value== 'White':
      if xDiff==0:
        if not self._isEmpty(xFinal,yFinal): return False
        if yDiff == 1:
          return True
        if yDiff == 2 and yInitial==1:
          return True
        return False
      elif abs(xDiff)==1 and yDiff==1:
        if self._isEmpty(xFinal,yFinal): return False
        return self._getPiece(xFinal,yFinal).colour.value=='Black'
    else:
      if xDiff==0:
        if not self._isEmpty(xFinal,yFinal): return False
        if yDiff == -1:
          return True
        if yDiff == -2 and yInitial==6:
          return True
        return False
      elif abs(xDiff)==1 and yDiff==-1:
        if self._isEmpty(xFinal,yFinal): return False
        return self._getPiece(xFinal,yFinal).colour.value=='White'
    return False
  def handleMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int) ->bool:
    if (xInitial,yInitial) == (xFinal,yFinal): return False
    if not self._boundsCheck(xInitial,yInitial): return False
    if not self._boundsCheck(xFinal,yFinal):return False
    if self._isEmpty(xInitial,yInitial):return False
    match self._getPiece(xInitial,yInitial).type.value:
      case 'King':
        return self.kingMove(xInitial,yInitial,xFinal,yFinal)
      case 'Knight':
        return self.knightMove(xInitial,yInitial,xFinal,yFinal)
      case 'Rook':
        return self.rookMove(xInitial,yInitial,xFinal,yFinal)
      case 'Bishop':
        return self.bishopMove(xInitial,yInitial,xFinal,yFinal)
      case 'Queen':
        return self.queenMove(xInitial,yInitial,xFinal,yFinal)
      case 'Pawn':
        return self.pawnMove(xInitial,yInitial,xFinal,yFinal)
  def makeMove(self,xInitial:int,yInitial:int,xFinal:int,yFinal:int):
    startingPiece = self._removePiece(xInitial,yInitial)
    endingPiece = self._removePiece(xFinal,yFinal)
    self._setPiece(xFinal,yFinal,startingPiece)
    return endingPiece
    
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