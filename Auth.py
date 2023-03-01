import pygame
import hashlib
import os
class Auth:
    def __init__(self,screen,path) -> None:
        self.whitePlayer=None
        self.blackPlayer=None
        self.screen=screen
        self.encoding='utf-8'
        self.path='temp/'+path
        self.data={}
        self.unsavedData={}
        self.createFile()
        self.readData()
    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse pressed
                    return
    def authorize(self,username):
        pass
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