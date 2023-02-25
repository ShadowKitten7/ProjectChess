import pygame
import hashlib
class Auth:
  def __init__(self,screen,path) -> None:
    self.whitePlayer=None
    self.blackPlayer=None
    self.screen=screen
    self.encoding='utf-8'
    self.path='temp/'+path
    print(hash('hi'))
    self.createFile()
    self.mainLoop()
  def mainLoop(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.end()
        if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse pressed
          return
  def createFile(self):
    f=open(self.path,'a')#Opens the file in append mode, creating a file if not present
    f.close()
  def hash(self,x):
    return hashlib.sha3_512(bytes(x,self.encoding)).hexdigest()