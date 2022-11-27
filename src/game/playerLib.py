#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Contributors:
#    Steffen Reichert - initial implementation  
#    Ondrej Kyjanek <ondrej.kyjanek@gmail.com>

import pygame

def drawRectPlayer(screen,color,posX,posY,sizeX,sizeY):
    return pygame.draw.rect(screen, color, (posX, posY, sizeX, sizeY))


# Wall Setup
def drawWalls(screen, color, width, height, size):
    upperWall = pygame.draw.rect(screen, color, (0, 0, width, size))
    lowerWall = pygame.draw.rect(screen, color, (0, height-size, width, size))
    leftWall = pygame.draw.rect(screen, color, (0, 0, size, height))
    rightWall = pygame.draw.rect(screen, color, (width-size, 0, size, height))
    return (upperWall, lowerWall, leftWall, rightWall)

print("imported playerLib")
