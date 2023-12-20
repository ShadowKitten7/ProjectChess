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
    self.promotionOptions = [[],[]]
    #Empty board
    self.board=[[None for i in range(self.boardSize)] for j in range(self.boardSize)]
    # (0,0) is considered to be the A1 square
    self._populate()
    # Create and store the Piece objects into promotionOptions
    # In the order Rook,Knight,Bishop,Queen for both black and white
    for i in[PieceType.Rook,PieceType.Knight,PieceType.Bishop,PieceType.Queen]:
            self.promotionOptions[0].append(Piece(PieceColour.Black, i))
            self.promotionOptions[1].append(Piece(PieceColour.White, i))
    self.toPlay=PieceColour.White
  def _isEmpty(self,x:int,y:int)-> bool:
    return self.board[x][y] is None
  def _getPiece(self,x:int,y:int):
    return self.board[x][y]
  def _setPiece(self,x:int,y:int,piece):
    self.board[x][y]=piece
  def _removePiece(self,x:int,y:int):
    piece=self.board[x][y]
    self.board[x][y]=None
    return piece
  def promotionCheck(self,x,y):
    p = self._getPiece(x,y)
    return (p.colour.name == "White" and p.type.name == "Pawn" and y == 7) or (
            p.colour.name == "Black" and p.type.name == "Pawn" and y == 0)
  def promote(self, x, y,pieceType):
        p = self._removePiece(x,y)
        match pieceType:
            case 0:
                self._setPiece(x,y,Piece(p.colour,PieceType.Queen))
            case 1:
                self._setPiece(x,y,Piece(p.colour,PieceType.Bishop))
            case 2:
                self._setPiece(x,y,Piece(p.colour,PieceType.Knight))
            case 3:
                self._setPiece(x,y,Piece(p.colour,PieceType.Rook))
        return not self._isEmpty(x,y)
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
  
  def drawCheck(self):
    whiteKnights,whiteBishops,blackKnights,blackBishops=0,0,0,0
    for x in range(8):
      for y in range(8):
        if self._isEmpty(x,y): continue
        piece = self._getPiece(x,y)
        if piece.type.value in ('Pawn','Queen','Rook'):
          return False
        if piece.type.value=='Bishop':
          if piece.colour.value == 'Black':
            blackBishops+=1
          else:
            whiteBishops+=1
        if piece.type.value == 'Knight':
          if piece.colour.value == 'Black':
            blackKnights+=1
          else:
            whiteKnights+=1
    if whiteKnights==0 and whiteBishops==0:#white is lone king
      if blackBishops==1 and blackKnights==0:
        return True
      if blackKnights==2 and blackBishops==0:
        return True
      if blackBishops==0 and blackKnights==0:
        return True
    elif blackBishops==0 and blackKnights==0:
      if whiteBishops==1 and whiteKnights==0:
        return True
      if whiteKnights==2 and whiteBishops==0:
        return True
    return False