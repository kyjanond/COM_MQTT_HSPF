#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Contributors:
#    Ondrej Kyjanek <ondrej.kyjanek@gmail.com> - initial implementation

import paho.mqtt.client as mqttc
import paho.mqtt.properties as properties
import logging
import pygame
from threading import Event
from collections import deque

logging.basicConfig(level=logging.INFO)

HOST = "broker.hivemq.com"
PORT = 1883
TOPIC = "hspf/sensornode/oky/#"
MODIFIER = 10

x = 0
y = 0
z = 0

def on_message(client, userdata, msg:mqttc.MQTTMessage):
    global x,y,z
    #payload is utf-8 encoded string so we need to decode it first
    try:
        payoad = msg.payload.decode('utf-8')
        if msg.topic.endswith('Accelerometer/x'):
            x = float(payoad)
        elif msg.topic.endswith('Accelerometer/y'):
            y = float(payoad)
        elif msg.topic.endswith('Accelerometer/z'):
            z = float(payoad)
    except Exception as e:
        logging.error(e)

def main():
    quit_event = Event()
    pygame.init()
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)
    black = 0, 0, 0
    ball = pygame.image.load("resources/intro_ball.gif")
    ballrect = ball.get_rect()
    ballrect.center = [width*0.5,height*0.5]
    velocity = [0,0]
    position = list(ballrect.center)

    font = pygame.font.SysFont(None, 16)

    client = mqttc.Client(protocol=mqttc.MQTTv5)

    client.on_message = on_message

    client.enable_logger(logging.getLogger())
    client.connect(HOST,PORT)
    client.loop_start()
    logging.info("Loop started")
    client.subscribe(TOPIC)

    clk = pygame.time.Clock()
    while not quit_event.is_set():
        s_tick = clk.tick()*0.001
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                quit_event.set()
        #render text
        x_val = font.render("{:5>.3f}".format(x), True, pygame.Color(255,0,0))
        y_val = font.render("{:5>.3f}".format(y), True, pygame.Color(0,255,0))
        z_val = font.render("{:5>.3f}".format(z), True, pygame.Color(100,100,255))
        #ball
        #velocity[0]+=y*MODIFIER*(s_tick**2)
        #velocity[1]+=-z*MODIFIER*(s_tick**2)
        velocity[0]=y*MODIFIER*s_tick
        velocity[1]=-z*MODIFIER*s_tick
        position[0]+=velocity[0]
        position[1]+=velocity[1]
        ballrect.center = position
        if ballrect.left < 0:
            ballrect.left = 0
            velocity[0] = 0
        elif ballrect.right > width:
            ballrect.right = width
            velocity[0] = 0
        if ballrect.top < 0:
            ballrect.top = 0
            velocity[1] = 0
        elif ballrect.bottom > height:
            ballrect.bottom = height
            velocity[1] = 0
        vel_text = font.render("x:{0[0]:5>.3f} | y:{0[1]:5>.3f}".format(velocity), True, pygame.Color(255,255,255))

        screen.fill(black)
        screen.blit(ball, ballrect)
        screen.blit(x_val, (20, 20))
        screen.blit(y_val, (20, 40))
        screen.blit(z_val, (20, 60))
        screen.blit(vel_text, (20, 80))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    logging.info("Closing")