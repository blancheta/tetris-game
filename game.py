#!/usr/bin/python3
import os
import sys
import pygame
from random import randint

from operator import itemgetter
from itertools import groupby

from shape_s import Shape_s
from shape_bar import Shape_bar
from shape_square import Shape_square
from shape_u import Shape_u

from threading import Thread
from collections import deque
from pygame import Rect
import time

pygame.init()

class Game:

	def __init__(self,screen):

		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height
		self.size = self.scr_width, self.scr_height

		# Background Game
		self.bg = pygame.image.load("images/starsbackground.jpg")
		self.bg_rect = self.bg.get_rect()

		# Life Bar
		self.lifes = []

		self.game_over = False
		self.victory = False

		#Clock
		self.clock = pygame.time.Clock()

		self.shapes = []
		self.tidy_shapes = []
		
		# Init Shapes
		self.shape_colors = [(255,255,255),(51,153,255),(153,255,51),(153,51,255)]

		self.shape_to_remove = []
		self.shape_remove = []

		# Time Variables
		self.timecount_m = 0
		self.timecount = 0

		# Init Variables
		self.super_indice = 0

		self.left_pressed = False
		self.right_pressed = False
		self.top_pressed = False

		self.border_left = False
		self.border_right = False

		self.top_pressed_count = 0
		self.start_new_object = True
		self.collision = False
		self.shape = None

		self.memo_left = 0
		self.created_id = 0
	def run(self):
		mainloop = True
		while mainloop:

			self.clock.tick(20)
			self.screen.fill([0, 0, 0])
			self.screen.blit(self.bg,self.bg_rect)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.left_pressed = True
					if event.key == pygame.K_RIGHT:
						self.right_pressed = True
					if event.key == pygame.K_UP:
						self.top_pressed = True
			if self.start_new_object:

				shape_color_chosen = randint(1,len(self.shape_colors) - 1)
				self.super_indice = len(self.tidy_shapes)
				self.shape = Shape_bar(self.super_indice,"Bar"+str(self.created_id),self.shape_colors[shape_color_chosen])
				self.created_id += 1
				self.start_new_object = False
				self.top_pressed_count = 0
				
			if self.shape is not None:

				if self.memo_left != len(self.tidy_shapes):
					# print("Nb de Shapes restantes :",len(self.tidy_shapes))
					self.memo_left = len(self.tidy_shapes)

				if self.top_pressed:

					self.top_pressed_count += 1
					self.top_pressed_count = self.shape.move(self.top_pressed_count)

					self.top_pressed = False

				if len(self.tidy_shapes) > 0:

					for tidy_shape in self.tidy_shapes:

						for tidy_rect in tidy_shape.shape_list:

							for rect in self.shape.shape_list:
								if (rect.y == tidy_rect.y - (rect.height + 5)) and ( rect.x == tidy_rect.x ):
									
									if self.shape not in self.tidy_shapes:
										self.tidy_shapes.append(self.shape)
										self.start_new_object = True
										self.collision = True

				for rect in self.shape.shape_list:

					if rect.x == 0:
						self.border_left = True
						self.border_right = False

					elif rect.x + rect.width == self.scr_width:
						self.border_right = True
						self.border_left = False

					if rect.x >= 0 and rect.x < self.scr_width:
						if self.left_pressed and not self.border_left:
							rect.x -= 50
							self.border_right = False		

						if self.right_pressed and not self.border_right:
							rect.x += 50
							self.border_left = False

				for i,rect_sh in enumerate(self.shape.shape_list):
					if ((rect_sh.y + rect_sh.height) <= self.scr_height):
						rect_sh.y += 5
					
					pygame.draw.rect(self.screen,self.shape.color,rect_sh)

					if( rect_sh.y + rect_sh.height ) == self.scr_height:
						self.start_new_object = True
						# print("self.shape =",self.shape.num," shape_list elem:",i)
				if self.start_new_object:
					if self.shape not in self.tidy_shapes:
						self.tidy_shapes.append(self.shape)

				# Draw all shapes saved

				if len(self.tidy_shapes) > 0:

					for sh in self.tidy_shapes:
						for rect in sh.shape_list:
							pygame.draw.rect(self.screen,sh.color,rect)

					# Check if line can be destroyed

					if self.start_new_object:

						abc = 450

						case_on_line = 0
						for sh in reversed(self.tidy_shapes):
							for z,rect in reversed(list(enumerate(sh.shape_list))):			
								if abc == rect.y:
									case_on_line +=1
									self.shape_to_remove.append({'shape':sh.num,'shape_ind':z})

						if case_on_line == 6:
							self.shape_to_remove.sort(key=itemgetter('shape'))

							for shape, items in groupby(self.shape_to_remove, key=itemgetter('shape')):

								for i in items:

									for n,sha in reversed(list(enumerate(self.tidy_shapes[shape].shape_list))):
										if i['shape_ind'] == n:
											del self.tidy_shapes[shape].shape_list[n]

								if len(self.tidy_shapes[shape].shape_list) == 0:
									# print("shape_list de Shape ",shape," est vide donc dans shape_remove ")
									self.shape_remove.append(shape)

							for e in reversed(self.shape_remove):
								self.tidy_shapes.remove(self.tidy_shapes[e])

							case_on_line = 0
							# On décale toutes les formes présentes dans tidy_shapes de 50 vers le bas

							for enum,left_shape in enumerate(self.tidy_shapes):
								print(left_shape.name," num :",left_shape.num)
								left_shape.num = enum
								for left_sh in left_shape.shape_list:
									if left_sh.y < abc:
										left_sh.y += 50

				self.shape_to_remove.clear()
				self.shape_remove.clear()

				self.collision = False
				self.left_pressed = False
				self.right_pressed = False
				pygame.display.flip()

