#!/usr/bin/python3
import os
import sys
import pygame
from random import randint
from shape import Shape
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

		self.font = pygame.font.SysFont(None,100)
		self.label_game_over = self.font.render("Game Over",1,(255,255,255))
		self.label_victory = self.font.render("Victory is yours",1,(255,255,255))

		#Clock
		self.clock = pygame.time.Clock()

		# Init Variables

		self.shapes = []
		self.tidy_shapes = []
		
		# Init Shapes

		mini_square = [Rect(0,0,50,50)]
		bar = [Rect(0,0,50,150)]
		z = [Rect(50,0,50,100),Rect(0,50,50,100)]

		for i in range(1,7):
			u = [Rect(0,0,50,100),Rect(50,0,50,50),Rect(100,0,50,100)]
			sha = Shape(i)
			sha.init_shape_list(u)
			self.shapes.append(sha)

		self.queue = deque(self.shapes)
		# Time Variables
		self.timecount_m = 0
		# self.shape_move_time = 2000
		self.timecount = 0

		self.left_pressed = False
		self.right_pressed = False
		self.border_left = False
		self.border_right = False

		self.start_new_object = False
		self.collision = False
		self.shape = self.queue.popleft()

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

			if self.start_new_object:
				if len(self.queue):
					self.shape = self.queue.popleft()
				else:
					self.shape = None
				self.start_new_object = False

			if self.shape is not None:

				if len(self.tidy_shapes) > 0:

					for tidy_shape in self.tidy_shapes:

						for tidy_rect in tidy_shape.shape_list:

							for rect in self.shape.shape_list:

								if (rect.y == tidy_rect.y - 105) and ( rect.x == tidy_rect.x):
									self.tidy_shapes.append(self.shape)

									self.start_new_object = True
									self.collision = True

				for rect in self.shape.shape_list:

					if rect.x == 0:
						self.border_left = True
						self.border_right = False

					elif rect.x + 50 == self.scr_width:
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
					if ((rect_sh.y + 100) <= self.scr_height):
						rect_sh.y += 5

					pygame.draw.rect(self.screen,(255,255,255),rect_sh)

					if( rect_sh.y +100) == self.scr_height:
						self.start_new_object = True


				if self.start_new_object:
					self.tidy_shapes.append(self.shape)

				# Draw all shapes saved

				for sh in self.tidy_shapes:
					for rect in sh.shape_list:
						pygame.draw.rect(self.screen,(255,255,255),rect)
				

				self.collision = False
				self.left_pressed = False
				self.right_pressed = False
				pygame.display.flip()

