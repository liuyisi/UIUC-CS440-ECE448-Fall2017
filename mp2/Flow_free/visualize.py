# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 17:31:00 2017

@author: wrxru
"""

import pygame

colorMap = {'P':(255,153,204), 'R':(255,0,0), 'G':(0,255,0), 'B':(0,0,255), 'Y':(255,255,0),
            'O':(255,128,0), 'Q':(81,72,79), 'D':(1,50,32), 'K':(58,176,158), 'T':(210,180,140),
            'F':(136,6,206), 'V':(243,229,171), 'S':(188,184,138), 'N': (233,255,219), 
            'H':(102,56,84), 'A':(59,122,87), 'W':(255,255,255), 'C': (247,231,206)}


mazeFile = open('output1414.txt', 'r')
lines = mazeFile.readlines()
mazeFile.close()
rows = len(lines)
columns = len(lines[0]) - 1 #trim the ending '\n'
# Window dimensions
width = 40*columns
height = 40*rows

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

for i in range(rows):
    for j in range(columns):
        if lines[i][j] == '\n':
            continue
        else:
            for x in range(i*40, (i+1)*40):
                for y in range(j*40, (j+1)*40):
                    screen.set_at((y, x), colorMap[lines[i][j]])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(240)
