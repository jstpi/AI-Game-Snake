import pygame
import data.dataUtils as data

class Square:
    '''square sprite forming the snake'''
    def __init__(self, pos, color):
        self.pos = pos
        self.dir = [0, 0]
        self.color = color

    def move(self, dir_x, dir_y):
        '''compute dir and pos'''
        self.dir[0] = dir_x
        self.dir[1] = dir_y
        self.pos[0] = self.pos[0] + dir_x
        self.pos[1] = self.pos[1] + dir_y

    def draw(self, surface):
        '''draw visual of the square'''
        dis = data.getConfig("width") // data.getConfig("rows")
        pygame.draw.rect(surface, self.color, (self.pos[0]*dis+1, self.pos[1]*dis+1, dis-2, dis-2))
    