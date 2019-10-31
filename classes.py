import pygame

from pygame.locals import *

import os

import mysql.connector

import random

from itertools import chain



class player(object):


    def __init__(self, x, y, width, height,skin):

        self.x = x

        self.y = y

        self.width = width

        self.height = height

        self.jumping = False

        self.sliding = False

        self.slideCount = 0

        self.jumpCount = 0

        self.runCount = 0

        self.slideUp = False

        self.falling = False

        self.skin = skin
        self.run = [pygame.image.load(os.path.join('images', self.skin + str(x) + '.png')) for x in range(8, 16)]

        self.jump = [pygame.image.load(os.path.join('images', self.skin + str(x) + '.png')) for x in range(1, 8)]
        self.fall = pygame.image.load(os.path.join('images', self.skin + '0.png'))
        self.slide = [pygame.image.load(os.path.join('images', self.skin + 'S1.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S2.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S2.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S2.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S2.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S2.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S2.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S2.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S3.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S4.png')),
                 pygame.image.load(os.path.join('images', self.skin + 'S5.png'))]


    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x,self.y+30))
        elif self.jumping:

            self.y -= self.jumpList[self.jumpCount] * 1.2

            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))

            self.jumpCount += 1

            if self.jumpCount > 108:
                self.jumpCount = 0

                self.jumping = False

                self.runCount = 0
            self.hitbox = (self.x + 6,self.y,self.width -26,self.height - 10)
        elif self.sliding or self.slideUp:

            if self.slideCount < 20:

                self.y += 1

            elif self.slideCount == 80:

                self.y -= 19

                self.sliding = False

                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x,self.y+3,self.width-8,self.height-35)

            if self.slideCount >= 110:
                self.slideCount = 0

                self.slideUp = False

                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 26, self.height - 10)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))

            self.slideCount += 1



        else:

            if self.runCount > 42:
                self.runCount = 0

            win.blit(self.run[self.runCount // 6], (self.x, self.y))

            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)


class saw(object):

    img = [pygame.image.load(os.path.join('images','SAW0.png')),pygame.image.load(os.path.join('images','SAW1.png')),pygame.image.load(os.path.join('images','SAW2.png')),pygame.image.load(os.path.join('images','SAW3.png'))]

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x,y,width,height)
        self.count = 0

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
    def draw(self,win):
        self.hitbox = (self.x + 7, self.y+5,self.width - 13,self.height)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.img[self.count//2],(64,64)),(self.x,self.y))
        self.count += 1
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)


class spike(saw):
    img = pygame.image.load(os.path.join('images','spike.png'))
    def draw(self,win):
        self.hitbox = (self.x + 13, self.y,22,470)
        self.hitbox2 =(self.x,self.y,47,420)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox2, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        if rect[0] + rect[2] > self.hitbox2[0] and rect[0] < self.hitbox2[0] + self.hitbox2[2]:
            if rect[1] < self.hitbox2[3]:
                return True
        return False


class button():
    def __init__(self, color, x, y, width, height, text='',filled=0,fontScale= 50,colorFont = (0,0,0)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.filled = filled
        self.fontScale = fontScale
        self.colorFont = colorFont
    def draw(self, win, outline=None):

        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), self.filled)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), self.filled)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.fontScale)
            text = font.render(self.text, 1, self.colorFont)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):

        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class database(object):

    def __init__(self,user,password,host,db):
        self.user = user
        self.password = password
        self.host = host
        self.db = db

    def connect(self):
        return mysql.connector.connect(user=self.user, password=self.password,host=self.host,database=self.db)

