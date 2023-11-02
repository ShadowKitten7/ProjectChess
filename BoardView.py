import pygame
import pygame.freetype
class BoardView:
  def __init__(self,screen,position,positiveDirections) -> None:
    self.screen = screen
    self.position=position
    self.positiveDirections=positiveDirections
    self.font = self.font = pygame.freetype.Font("assets/sf-cartoonist-regular.ttf",20)
    self.height=8*70
    self.width =8*70
  def render(self):
    self.renderSquares()
    
    pygame.display.update()
  def renderSquares(self):
    white=(255, 253, 208)
    black=(14, 119, 14)
    for i in range(8):
      for j in range(8):
        colour = (i+j)%2
        x,y=self.position[0]+i*70*self.positiveDirections[0],self.position[1]+j*70*self.positiveDirections[1]
        if colour:
          pygame.draw.rect(self.screen,white,(x,y,70,70))
        else:
          pygame.draw.rect(self.screen,black,(x,y,70,70))

pygame.init()
screen=pygame.display.set_mode((600,600))
d = BoardView(screen,(500,10),(-1,1))
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()
  d.render()
  