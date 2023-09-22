import pygame
import pygame.freetype
from MainGame import game_constants
import hashlib
import os

class auth_constants:
    def __init__(self):
        self.background=(150, 192, 100)
class Auth:
    def __init__(self,screen,path):
        self.whitePlayer=None
        self.blackPlayer=None
        self.c=auth_constants()
        self.screen=screen
        self.width=screen.get_width()
        self.height=screen.get_width()
        self.encoding='utf-8'
        self.path='temp/'+path
        self.gc=game_constants()
        self.title_font=pygame.freetype.Font('assets/nexa-handmade.otf',self.gc.scale*5//8)
        self.subtitle_font=pygame.freetype.Font('assets/nexa-handmade.otf',self.gc.scale*3//8)
        self.data={}
        self.unsavedData={}
        self.createFile()
        self.readData()
    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                    
                self.render()
    def centreRect(self,rect,x,y):
        return (x-rect.width//2,y-rect.height//2)
    def render(self):
        self.screen.fill(self.c.background)
        self.renderTextCentred(self.title_font,(self.width//2,self.height//5),'Welcome to Project Chess')
        self.renderTextCentred(self.subtitle_font,(self.width//2,self.height//5+self.gc.scale),'User Authentication')
        self.renderTextCentred(self.subtitle_font,(self.width//2,self.height//5+2*self.gc.scale),'Enter Username')
        
        pygame.display.update()
    def renderTextCentred(self,font:pygame.freetype.Font,pos,text):
        rect=font.get_rect(text)
        font.render_to(self.screen,self.centreRect(rect,pos[0],pos[1]),text)
    def authorize(self,username,password):
        if username in self.data and self.data[username][1]==self.hash(password):
            return True
        return False
    def readData(self):
        file=open(self.path,'r',encoding='utf-8')
        data=[i[:-1].split(',') for i in file.readlines()]
        for i in range(len(data)-1):
            self.data[data[i][0]]=[data[i][1],data[i][2]]
        file.close()
    def createEntry(self,username,password,elo):
        h=self.hash(password)
        self.data[username]=[elo,h]
        self.unsavedData[username]=[str(elo),h]
    def saveData(self):
        tempfile=open(self.path+'.tmp','a',encoding='utf-8')
        file=open(self.path,'r',encoding='utf-8')
        for line in file.readlines():
            index=0#Find the index of the first separator
            for i in range(len(line)):
                if line[i]==',':
                    index=i
                    break
            username=line[:index]#Extract the username
            if username in self.unsavedData:#If it has been updated
                tempfile.write(self.convertDataToEntry(self.unsavedData,username))
                self.unsavedData.pop(username)
            else:
                tempfile.write(line)
        for i in self.unsavedData:
            tempfile.write(self.convertDataToEntry(self.unsavedData,i))
            tempfile.close()
            file.close()
        os.remove(self.path)
        os.rename(self.path+'.tmp',self.path) 
    def convertDataToEntry(self,dictionary,key):
        return str(key)+','+','.join(dictionary[key])+'\n'
    def createFile(self):
        f=open(self.path,'a',encoding='utf-8')#Opens the file in append mode, creating a file if not present
        f.close()
    def hash(self,x):
        return hashlib.sha3_512(bytes(x,self.encoding)).hexdigest()
class InputBox:
    def __init__(self,pos,size,font,text='') -> None:
        self.rect=pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.COLOUR_INACTIVE=(97, 201, 137)
        self.COLOUR_ACTIVE=(199, 201, 97)
        self.colour=self.COLOUR_INACTIVE
        self.text=text
        self.text_surface=font.render(text,True,self.colour)
        self.active=False
        self.font=font
    def handle_event(self,event):#returns if a change has been made
        if event==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.active:
                self.active=True
            self.colour = self.COLOUR_ACTIVE if self.active else self.COLOUR_INACTIVE
        if event==pygame.KEYDOWN and self.active:
            if event.key==pygame.K_RETURN:
                print(self.text)
                self.active=False
            elif event.key==pygame.K_BACKSPACE:
                self.text=self.text[:-1]
            else:
                self.text+=event.unicode
            self.text_surface=self.font.render(self.text,True,self.colour)
            return True
        return False
    def draw(self,screen):
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen,self.colour,self.rect)