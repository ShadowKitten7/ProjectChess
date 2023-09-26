import hashlib
import os

import pygame
import pygame.freetype

from MainGame import game_constants


class auth_constants:
    def __init__(self):
        self.background=(108, 108, 108)
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
        self.title_font=pygame.freetype.Font('assets/nexa-handmade.otf',self.gc.scale*3//4)
        self.subtitle_font=pygame.freetype.Font('assets/RobotoMono-SemiBold.ttf',self.gc.scale//2)
        self.auth_font=pygame.freetype.Font('assets/RobotoMono-Regular.ttf',self.gc.scale//3)
        self.data={}
        self.unsavedData={}
        self.createFile()
        self.readData()
        self.charHeight=30
        self.usernameBox=InputBox((self.width//2-self.gc.scale*2//3,self.height//2),(self.width//3,self.charHeight),self.auth_font)
        self.passwordBox=PasswordBox((self.width//2-self.gc.scale*2//3,self.height*3//5),(self.width//3,self.charHeight),self.auth_font)
        self.button=Button((self.width//2-self.gc.scale*3//2,self.height*3//4),(self.gc.scale*3,self.charHeight*3//2),self.auth_font,'Login')
        self.alert=''
        self.players=[]
    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.saveData()
                    return None
                if len(self.players)==2:
                    if self.button.handle_event(event):
                        return self.players
                self.login(event)
                self.render()
    def login(self,event):
        self.usernameBox.handle_event(event)
        self.passwordBox.handle_event(event)
        if self.button.handle_event(event):
            username=self.usernameBox.getText()
            password=self.passwordBox.getText()
            valid=True
            if username=='':
                self.usernameBox.error()
                valid=False
            if password=='':
                self.passwordBox.error()
                valid=False
            if valid:
                return self.authorize(username,password)
            else:
                return False        
    def centreRect(self,rect,x,y):
        return (x-rect.width//2,y-rect.height//2)
    def render(self):
        self.screen.fill(self.c.background)
        self.renderTextCentred(self.title_font,(self.width//2,self.height//5),'Welcome to Project Chess')
        self.renderTextCentred(self.subtitle_font,(self.width//2,self.height//5+self.gc.scale),'User Authentication')
        pygame.draw.line(self.screen,(0,0,0),(self.width//4,self.height//5+self.gc.scale*4//3),(self.width*3//4,self.height//5+self.gc.scale*4//3),width=3)
        if not len(self.players)==2:
            self.renderTextCentred(self.auth_font,(self.width//2,self.height*2//5),'Player #'+str(len(self.players)+1))
            self.renderTextCentred(self.auth_font,(self.width//3,self.height//2+self.charHeight//2),'Username')
            self.renderTextCentred(self.auth_font,(self.width//3,self.height*3//5+self.charHeight//2),'Password')
            self.usernameBox.draw(self.screen)
            self.passwordBox.draw(self.screen)
        self.button.draw(self.screen)
        self.renderTextCentred(self.auth_font,(self.width//2,self.height*7//10),self.alert)
        self.renderTextCentred(self.auth_font,(self.width//3,self.height*17//20),'Player 1')
        if len(self.players)>=1:
            self.renderTextCentred(self.auth_font,(self.width//3,self.height*9//10),self.players[0][0])
        self.renderTextCentred(self.auth_font,(self.width*2//3,self.height*17//20),'Player 2')
        if len(self.players)==2:
            self.renderTextCentred(self.auth_font,(self.width*2//3,self.height*9//10),self.players[1][0])
        pygame.display.update()
    def renderTextCentred(self,font:pygame.freetype.Font,pos,text):
        rect=font.get_rect(text)
        font.render_to(self.screen,self.centreRect(rect,pos[0],pos[1]),text)

    def authorize(self,username,password):
        if username not in self.data:
            self.alert='Invalid username'
            self.usernameBox.error()
            self.usernameBox.clear()
            self.passwordBox.clear()
            return False
        if not self.data[username][1]==self.hash(password):
            self.alert = 'Invalid password'
            self.passwordBox.clear()
            self.passwordBox.error()
            return False
        self.players.append((username,self.data[username][0]))
        self.usernameBox.clear()
        self.passwordBox.clear()
        self.alert=''
        if len(self.players)==2:
            self.button.text='Play'
        return True
    def readData(self):
        file=open(self.path,'r',encoding='utf-8')
        data=[i[:-1].split(',') for i in file.readlines()]
        for i in range(len(data)):
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
        self.COLOUR_INACTIVE=(118, 118, 118)
        self.COLOUR_ACTIVE=(138, 138, 138)
        self.COLOUR_ERROR=(219, 75, 75)
        self.border_colour=(0,0,0)
        self.border_width=1
        self.colour=self.COLOUR_INACTIVE
        self.text=text
        self.text_surface=font.render(text,True,self.colour)
        self.active=False
        self.font=font
    def handle_event(self,event):#returns if a change has been made
        c=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.active:
                self.active=True
                self.colour=self.COLOUR_ACTIVE
                c=True
            elif self.active:
                self.active=False
                self.colour=self.COLOUR_INACTIVE
        if event.type==pygame.KEYDOWN and self.active:
            if event.key==pygame.K_RETURN:
                self.active=False                
                self.colour=self.COLOUR_INACTIVE
            elif event.key==pygame.K_BACKSPACE:
                self.text=self.text[:-1]
            else:
                self.text+=event.unicode
        return event.type==pygame.MOUSEBUTTONDOWN and c
    def error(self):
        self.colour=self.COLOUR_ERROR
    def clear(self):
        self.text=''
    def getText(self):
        return self.text
    def centreRect(self,rect,x,y):
        return (x-rect.width//2,y-rect.height//2)
    def renderCentred(self,screen,pos,text):
        rect=self.font.get_rect(text)
        self.font.render_to(screen,self.centreRect(rect,pos[0],pos[1]),text)
    def drawBackground(self,screen):
        pygame.draw.rect(screen,self.border_colour,(self.rect[0]-self.border_width,self.rect[1]-self.border_width,self.rect.width+2*self.border_width,self.rect.height+2*self.border_width))
        pygame.draw.rect(screen,self.colour,self.rect)
    def draw(self,screen):
        self.drawBackground(screen)
        self.renderCentred(screen,(self.rect[0]+self.rect.width//2,self.rect[1]+self.rect.height//2),self.text)
class PasswordBox(InputBox):
    def __init__(self, pos, size, font, text='') -> None:
        super().__init__(pos, size, font, text)
    def draw(self,screen):
        self.drawBackground(screen)
        self.renderCentred(screen,(self.rect[0]+self.rect.width//2,self.rect[1]+self.rect.height//2),'*'*len(self.text))
class Button:
    def __init__(self,pos,size,font,text) -> None:
        self.rect=pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.border_colour=(0,0,0)
        self.border_width=1
        self.COLOUR_INACTIVE=(118, 118, 118)
        self.COLOUR_ACTIVE=(138, 138, 138)
        self.font=font
        self.text=text
        self.colour=self.COLOUR_INACTIVE
    def handle_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.colour=self.COLOUR_ACTIVE
            else:
                self.colour=self.COLOUR_INACTIVE
        elif event.type==pygame.MOUSEBUTTONUP:
            self.colour=self.COLOUR_INACTIVE
            if self.rect.collidepoint(event.pos):
                return True
        return False
    def centreRect(self,rect,x,y):
        return (x-rect.width//2,y-rect.height//2)
    def renderCentred(self,screen,pos,text):
        rect=self.font.get_rect(text)
        self.font.render_to(screen,self.centreRect(rect,pos[0],pos[1]),text)
    def draw(self,screen):
        pygame.draw.rect(screen,self.border_colour,(self.rect[0]-self.border_width,self.rect[1]-self.border_width,self.rect.width+2*self.border_width,self.rect.height+2*self.border_width))
        pygame.draw.rect(screen,self.colour,self.rect)
        self.renderCentred(screen,(self.rect[0]+self.rect.width//2,self.rect[1]+self.rect.height//2),self.text)