from instrument import Player
from pyo import Server, Metro
import pygame

players = []

ESC = 27
PLUS = 43
MINUS = 45

notes1 = ['a', 'b', 'c']
notes2 = ['d', 'g', 'h']
notes3 = ['e', 'f', 'i', 'j']

screen = pygame.display.set_mode((800,600))


run = True

server = Server().boot()
server.start()

met = Metro(.125, 12).play()

players.append(Player(met, notes1))
players.append(Player(met, notes2))
players.append(Player(met, notes3))

while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            for player in players:
                player.note_off(chr(event.key))
            
            if event.key == ESC:
                run = False
                break
            if event.key == PLUS:
                met.time = min(.5, met.time + .01)
            if event.key == MINUS:
                met.time = max(.07, met.time - .01)

        if event.type == pygame.KEYDOWN:
            for player in players:
                player.note_on(chr(event.key))

server.stop()
