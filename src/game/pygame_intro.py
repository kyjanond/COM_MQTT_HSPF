#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Contributors:
#    Steffen Reichert - initial implementation  
#    Ondrej Kyjanek <ondrej.kyjanek@gmail.com> 

# UPDATE DIRECTORY
import os
directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory)

# Import libraries
import pygame
import playerLib
import random

#MQTT setup
import paho.mqtt.client as mqttc
import json

HOST = "broker.hivemq.com"
PORT = 1883
USERNAME = "oky"
#IPHONE = "/iphone"
IPHONE = ""
TOPIC = "hspf/sensornode/"+USERNAME+IPHONE+"/#"
MODIFIER = 10
DEBUG = True
print(TOPIC)

acc_x = acc_y = acc_z = 0

def parse_android(msg:mqttc.MQTTMessage):
    global acc_x, acc_y, acc_z
    payload = msg.payload.decode('utf-8')
    if msg.topic.endswith("Accelerometer/x"):
        acc_x = float(payload) #'9.90000'
    elif msg.topic.endswith("Accelerometer/y"):
        acc_y = float(payload)
    elif msg.topic.endswith("Accelerometer/z"):
        acc_z = float(payload)

def parse_iphone(msg:mqttc.MQTTMessage):
    global acc_x, acc_y, acc_z
    payload = msg.payload.decode('utf-8')
    json_payload = json.loads(payload)
    
    if "Acceleration" in json_payload:
        acc_x = json_payload["Orientation"]["Yaw"]
        acc_y = json_payload["Orientation"]["Roll"]
        acc_z = json_payload["Orientation"]["Pitch"]

def on_message(client, userdata, msg:mqttc.MQTTMessage):
    try:
        if msg.topic.endswith("iphone"): #msg/blabla/iphone
            parse_iphone(msg)
        else:
            parse_android(msg)
    except Exception as e:
        print(e)

client = mqttc.Client(protocol=mqttc.MQTTv5)
client.on_message = on_message
client.connect(HOST,PORT)
client.loop_start()
client.subscribe(TOPIC)

# GAME SETUP
pygame.init()

# SET CAPTION
pygame.display.set_caption("Basketball Game")

# SCREEN SETUP
width = 800         # ADD FULLSCREEN
height = 600        # ADD SCREEN
fps = 60
timer = pygame.time.Clock()
#screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height))


# PLAYER SETUP
size = 50
x = width/2 - size/2
y = height/2 - size/2
speed = 10

# SPRITE SETUP
spriteSize = 100
spriteX = random.randrange(0,width-spriteSize)
spriteY = random.randrange(0,height-spriteSize)

# ENEMY SETUP
enemySize = 100
enemyX = random.randrange(0,width-enemySize)
enemyY = random.randrange(0,height-enemySize)


# LOAD IMAGES
playerImage = pygame.image.load("images/basketball50x50_2.png").convert_alpha()
#playerImage = pygame.transform.scale(playerImage,(100,10))
#playerImage = pygame.transform.rotate(playerImage, -45.0)
spriteImage = pygame.image.load("images/cage100x100.png").convert_alpha()


# LOAD CUSTOM FONT
font = pygame.font.SysFont('Roboto', 48)
font_debug = pygame.font.SysFont('Roboto', 24)

# SCORE DATA
score = 0

# DRAW WALLS
walls = playerLib.drawWalls(screen,'red', width, height, 5)


vel_x = 0
vel_y = 0

# ACTIVE LOOP
run = True
while run:

    # SET FRAME RATE
    s_tick = timer.tick(fps)*0.001 # SET REFRESH LIMIT

    # Draw Player Collision Box
    player = playerLib.drawRectPlayer(screen, 'yellow', x, y, size, size)

    # Draw Sprite Collision Box
    spriteCollide = playerLib.drawRectPlayer(screen, 'red', spriteX+40, spriteY+40, 20, 20)

    # Draw Background Fill
    screen.fill('white') # RESET IMAGE WITH WHITE

    # Draw Sprite
    customSurface = pygame.Surface((width,height),pygame.SRCALPHA, 32)
    customSurface.blit(spriteImage, (spriteX, spriteY)) # Draw Image
    customSurface.set_alpha(40)         # set Transparency of surface to 40%
    screen.blit(customSurface, (0,0))

    # Draw a Player Image
    screen.blit(playerImage, (x,y)) # Draw Image

    # Draw Score Board
    fontImage = font.render('score: ' + str(score), True, 'black') # MAKE TEXT TO IMAGE
    screen.blit(fontImage, (width/2-100, height-100)) # BAKE IMAGE

    # PLAYER SPRITE INTERACTION
    if player.colliderect(spriteCollide):
        score += 1
        spriteX = random.randrange(0,width-spriteSize)
        spriteY = random.randrange(0,height-spriteSize)


    # MOUSE INTERACTION
    # mousePosition = pygame.mouse.get_pos()
    # print(mousePosition)
    # mouseLeftClick = pygame.mouse.get_pressed()[0]
    # mouseMiddleClick = pygame.mouse.get_pressed()[1]
    # mouseRightClick = pygame.mouse.get_pressed()[2]
    # if mouseLeftClick: pygame.draw.circle(screen, 'red', mousePosition, 100) # DRAW CIRCLE
    # if mouseMiddleClick: pygame.draw.circle(screen, 'green', mousePosition, 100) # DRAW CIRCLE
    # if mouseRightClick: pygame.draw.circle(screen, (30,30,255), mousePosition, 100) # DRAW CIRCLE

    # PLAYER MOVEMENT
    vel_y = -(acc_y+90)*MODIFIER*s_tick
    vel_x = acc_z*MODIFIER*s_tick
    if (vel_y<0 and not player.colliderect(walls[0])):
        y += vel_y                      # (y = y - speed)
    if (vel_y>0 and not player.colliderect(walls[1])):
        y += vel_y 
    if (vel_x<0 and not player.colliderect(walls[2])):
        x += vel_x 
    if (vel_x>0 and not player.colliderect(walls[3])):
        x += vel_x 

    # pressedKeys = pygame.key.get_pressed()
    # if pressedKeys[pygame.K_UP] and not player.colliderect(walls[0]):
    #     y -= speed                      # (y = y - speed)
    # if pressedKeys[pygame.K_DOWN] and not player.colliderect(walls[1]):
    #     y += speed 
    # if pressedKeys[pygame.K_LEFT] and not player.colliderect(walls[2]):
    #     x -= speed 
    # if pressedKeys[pygame.K_RIGHT] and not player.colliderect(walls[3]):
    #     x += speed 

    # EVENT LOOP
    for event in pygame.event.get():      
        # EXIT STATEMENT
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode([width, height])
            if event.key == pygame.K_f:
                screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
    
    #debug info
    if DEBUG:
        acc_x_str = font_debug.render("{:5>.3f}".format(acc_x),True,pygame.Color(255,0,0))
        acc_y_str = font_debug.render("{:5>.3f}".format(acc_y),True,pygame.Color(0,255,0))
        acc_z_str = font_debug.render("{:5>.3f}".format(acc_z),True,pygame.Color(0,0,255))
        screen.blit(acc_x_str, (20,20))
        screen.blit(acc_y_str, (20,40))
        screen.blit(acc_z_str, (20,60))
    # DISPLAY SCREEN
    pygame.display.flip()

pygame.quit()