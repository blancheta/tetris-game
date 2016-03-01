#!/usr/bin/python3
import os
import sys
import pygame
from game import Game
from gamemenu import GameMenu

pygame.init()

screen = pygame.display.set_mode((300,500),0,32)

# Game Menu
pygame.display.set_caption('Game Menu')
menu_items = ('Start','Settings','Quit')
gm = GameMenu(screen,menu_items)

# Settings
bg_color = (0,0,0)

mainloop = True
while mainloop:
	screen.fill(bg_color)
	g = None
	# if gm.quit_select == False or gm.start_selected == False :
	# 	gm.run()
	# 	if g is not None:
	# 		g.escape_selected = False

	# if gm.start_selected:
	# 	g = Game(screen)
	# 	g.run()
	# 	gm.start_selected = False
	# 	gm.quit_select = False

	# if gm.settings_selected:
	# 	gm.settings_selected = False
		
	# if gm.quit_select == True:
	# 	mainloop = False

	g = Game(screen)
	g.run()
	gm.start_selected = False
	gm.quit_select = False

	pygame.display.flip()