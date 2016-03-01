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

	def init_click_vars(self):
		
		self.left_pressed = False
		self.right_pressed = False

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
		self.shape_types = ['bar','square','u','s']
		self.shape_colors = [(255,255,255),(51,153,255),(153,255,51),(153,51,255)]

		for i in range(1,15):
			shape_type_chosen = randint(1,len(self.shape_types) - 1)
			# shape_type_chosen = 1

			if shape_type_chosen == 1:
				shape = Shape_bar(i)
			elif shape_type_chosen == 2:
				shape = Shape_s(i)
			elif shape_type_chosen == 3:
				shape = Shape_square(i)
			else:				
				shape = Shape_u(i)

			self.shapes.append(shape)

		# Time Variables
		self.timecount_m = 0
		self.timecount = 0


		self.queue = deque(self.shapes)

		self.left_pressed = False
		self.right_pressed = False
		self.top_pressed = False

		self.border_left = False
		self.border_right = False

		self.top_pressed_count = 0
		self.start_new_object = False
		self.collision = False
		self.shape = self.queue.popleft()

		print("Init position :")
		print(self.shape.shape_list)

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
				if len(self.queue):
					self.shape = self.queue.popleft()
					self.top_pressed_count = 0
				else:
					self.shape = None
				self.start_new_object = False

			if self.shape is not None:

				if self.top_pressed:

					self.top_pressed_count += 1
					self.top_pressed_count = self.shape.move(self.top_pressed_count)

					self.top_pressed = False

				if len(self.tidy_shapes) > 0:

					for tidy_shape in self.tidy_shapes:

						for tidy_rect in tidy_shape.shape_list:

							for rect in self.shape.shape_list:
								if (rect.y == tidy_rect.y - (rect.height + 5)) and ( rect.x == tidy_rect.x ):
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

					shape_color_chosen = randint(1,len(self.shape_colors) - 1)
					pygame.draw.rect(self.screen,self.shape_colors[shape_color_chosen],rect_sh)

					if( rect_sh.y + rect_sh.height) == self.scr_height:
						self.start_new_object = True


				if self.start_new_object:
					self.tidy_shapes.append(self.shape)

				# Draw all shapes saved

				for sh in self.tidy_shapes:
					for rect in sh.shape_list:
						pygame.draw.rect(self.screen,(255,255,255),rect)

				# Check if line can be destroyed

				if self.start_new_object:

					abc = 450
					size_shapes_on_line = 0

					shape_to_remove = []
					for sh in self.tidy_shapes:

						for z,rect in enumerate(sh.shape_list):
							
							if abc == rect.y:
								size_shapes_on_line += rect.width
								print("shapes size :",size_shapes_on_line)
								shape_to_remove.append({'shape':sh.num,'shape_ind':z})
					if size_shapes_on_line == self.scr_width:
						print(self.tidy_shapes)

						shape_to_remove.sort(key=itemgetter('shape'))

						print(self.tidy_shapes)
						for shape, items in groupby(shape_to_remove, key=itemgetter('shape')):
							indice = shape - 1
							for i in items:
								del self.tidy_shapes[indice].shape_list[0]

						print(self.tidy_shapes)
					size_shapes_on_line = 0

				self.collision = False
				self.left_pressed = False
				self.right_pressed = False
				pygame.display.flip()

