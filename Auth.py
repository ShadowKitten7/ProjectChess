import pygame
import hashlib
import os


class Auth:
    def __init__(self, screen, path) -> None:
        self.white_player = None
        self.black_player = None
        self.screen = screen
        self.encoding = "utf-8"
        self.path = "temp/" + path
        self.data = {}
        self.unsaved_data = {}
        self.createFile()
        self.readData()

    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:  # If mouse pressed
                    return

    def authorize(self, username, password):
        if username in self.data:
            if self.data[username] == self.hash(password):
                return True
        return False

    def readData(self):
        file = open(self.path, "r")
        data = [i[:-1].split(",") for i in file.readlines()]
        for i in range(len(data) - 1):
            self.data[data[i][0]] = [data[i][1], data[i][2]]
        file.close()

    def createEntry(self, username, password, elo):
        h = self.hash(password)
        self.data[username] = [elo, h]
        self.unsaved_data[username] = [str(elo), h]

    def saveData(self):
        tempfile = open(self.path + ".tmp", "a",encoding='utf-8')
        file = open(self.path, "r",encoding='utf-8')
        for line in file.readlines():
            index = line.find(',')
            username = line[:index]  # Extract the username
            if username in self.unsaved_data:  # If it has been updated
                tempfile.write(self.convertDataToEntry(self.unsaved_data, username))
                self.unsaved_data.pop(username)
            else:
                tempfile.write(line)
        for i in self.unsaved_data:
            tempfile.write(self.convertDataToEntry(self.unsaved_data, i))
        tempfile.close()
        file.close()
        os.remove(self.path)
        os.rename(self.path + ".tmp", self.path)

    def convertDataToEntry(self, dictionary, key):
        return str(key) + "," + ",".join(dictionary[key]) + "\n"

    def createFile(self):
        f = open(self.path, "a",encoding='utf-8')
        f.close()

    def hash(self, x):
        return hashlib.sha3_512(bytes(x, self.encoding)).hexdigest()