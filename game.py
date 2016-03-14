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
		self.bg = pygame.transform.scale(self.bg,(300,500))
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
		self.game_stop = False
		self.collision = False
		self.shape = None

		self.ylines = [{'y':450,'cc':0},{'y':400,'cc':0},{'y':350,'cc':0},{'y':300,'cc':0},{'y':250,'cc':0},{'y':200,'cc':0},{'y':150,'cc':0},{'y':100,'cc':0},{'y':50,'cc':0},{'y':0,'cc':0}]

		self.created_id = 0

		self.score = 0

		# Menu right
		self.font = pygame.font.SysFont(None,25)
		self.label_score = self.font.render("SCORE",1,(255,255,255))
		self.value_score = self.font.render("000",1,(255,255,255))
		self.label_next = self.font.render("NEXT",1,(255,255,255))

	def create_new_shape(self):

		shape_color_chosen = randint(1,len(self.shape_colors) - 1)
		# shape_chosen = randint(0,3)
		shape_chosen = 3

		self.super_indice = len(self.tidy_shapes)

		creation_shape_params = [self.super_indice,"Bar"+str(self.created_id),self.shape_colors[shape_color_chosen]]
		if shape_chosen == 0:
			self.shape = Shape_u(*creation_shape_params)
		elif shape_chosen == 1:
			self.shape = Shape_s(*creation_shape_params)
		elif shape_chosen == 2:
			self.shape = Shape_square(*creation_shape_params)
		elif shape_chosen == 3:
			self.shape = Shape_bar(*creation_shape_params)

		self.created_id += 1
		self.start_new_object = False
		self.top_pressed_count = 0

	def detect_keyboard_event(self,events):

		for event in events:
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.left_pressed = True
				if event.key == pygame.K_RIGHT:
					self.right_pressed = True
				if event.key == pygame.K_UP:
					self.top_pressed = True
	
	def detect_collision_with_other_shapes(self):

		for tidy_shape in self.tidy_shapes:

			for tidy_rect in tidy_shape.shape_list:

				for rect in self.shape.shape_list:
					if (rect.y == tidy_rect.y - (rect.height)) and ( rect.x == tidy_rect.x ):

						if self.shape not in self.tidy_shapes:
							self.tidy_shapes.append(self.shape)
							self.start_new_object = True
							self.collision = True

						if tidy_rect.y == 50 and rect.y + rect.height == 50:
							self.game_stop = True
							break

					if ((rect.y >= tidy_rect.y) and (rect.y <= tidy_rect.y+ tidy_rect.y + tidy_rect.height)) or ((rect.y + rect.height >= tidy_rect.y) and (rect.y + rect.height <= tidy_rect.y + tidy_rect.height)):
						if rect.x == tidy_rect.x + tidy_rect.width:
							self.left_pressed = False
						elif rect.x + rect.width == tidy_rect.x:
							self.right_pressed = False

	def draw_current_shape(self):

		for i,rect_sh in enumerate(self.shape.shape_list):
			if ((rect_sh.y + rect_sh.height) <= self.bg_rect.height):
				rect_sh.y += 5
			
			pygame.draw.rect(self.screen,self.shape.color,rect_sh)

			if( rect_sh.y + rect_sh.height ) == self.bg_rect.height:
				self.start_new_object = True

		if self.start_new_object:
			if self.shape not in self.tidy_shapes:
				self.tidy_shapes.append(self.shape)

	def draw_tidy_shapes(self):
		for sh in self.tidy_shapes:
			for rect in sh.shape_list:
				pygame.draw.rect(self.screen,sh.color,rect)

	def draw_score_box(self):

		score_rect = Rect(self.bg_rect.width + 20,20,160,80)
		pygame.draw.rect(self.screen,(255,255,255),score_rect,1)
		self.screen.blit(self.label_score,(self.bg_rect.width + 20 +score_rect.width/2 - self.label_score.get_rect().width/2,40))

		score_3_digits = "{:03}".format(self.score)

		self.value_score = self.font.render(score_3_digits,1,(255,255,255))

		self.screen.blit(self.value_score,(self.bg_rect.width + 20 +score_rect.width/2 - self.value_score.get_rect().width/2,60))

	def draw_queue_box(self):
		queue_rect = Rect(self.bg_rect.width + 20,180,160,250)
		pygame.draw.rect(self.screen,(255,255,255),queue_rect,1)
		self.screen.blit(self.label_next,(self.bg_rect.width + 20 +queue_rect.width/2 - self.label_next.get_rect().width/2,200))

	def delete_empty_shapes(self,shape_remove_list):
		for e in reversed(shape_remove_list):
			self.tidy_shapes.remove(self.tidy_shapes[e])

	def delete_rects_on_break_line(self,abc):

		self.shape_to_remove.sort(key=itemgetter('shape'))

		for shape, items in groupby(self.shape_to_remove, key=itemgetter('shape')):

			for i in items:

				for n,sha in reversed(list(enumerate(self.tidy_shapes[shape].shape_list))):
					if i['y'] == abc and i['shape_ind'] == n:
						del self.tidy_shapes[shape].shape_list[n]

			if len(self.tidy_shapes[shape].shape_list) == 0:
				self.shape_remove.append(shape)

	def forbid_to_go_over_screen_border(self,rect):
		# Forbid to go over the left border

		if rect.x == 0:
			self.border_left = True
			self.border_right = False

		# Forbid to go over the right border

		elif rect.x + rect.width == self.bg_rect.width:
			self.border_right = True
			self.border_left = False

	def move_down_left_shapes(self,tidy_shapes,abc):
		for enum,left_shape in enumerate(tidy_shapes):
			left_shape.num = enum
			for left_sh in left_shape.shape_list:
				if left_sh.y < abc:
					left_sh.y += 50

	def move_shape_on_the_left(self,rect):
		rect.x -= 50
		self.border_right = False

	def move_shape_on_the_right(self,rect):
		rect.x += 50
		self.border_left = False

	def reset_values_end_loop(self):
		self.shape_to_remove.clear()
		self.shape_remove.clear()

		self.collision = False
		self.left_pressed = False
		self.right_pressed = False

	def run(self):
		mainloop = True
		while mainloop:

			self.clock.tick(20)
			self.screen.fill([0, 0, 0])
			self.screen.blit(self.bg,self.bg_rect)

			self.detect_keyboard_event(pygame.event.get())

			if self.start_new_object and not self.game_stop:

				self.create_new_shape()
				
			if self.shape is not None:

				if self.top_pressed:

					self.top_pressed_count += 1
					self.top_pressed_count = self.shape.move(self.top_pressed_count)

					self.top_pressed = False

				if not self.game_stop:
					self.draw_current_shape()

				self.draw_score_box()
				self.draw_queue_box()

				for rect in self.shape.shape_list:

					self.forbid_to_go_over_screen_border(rect)

					if rect.x >= 0 and rect.x < self.bg_rect.width:

						if self.left_pressed and not self.border_left:
		
							self.move_shape_on_the_left(rect)

						if self.right_pressed and not self.border_right:

							self.move_shape_on_the_right(rect)

				if len(self.tidy_shapes) > 0:

					self.detect_collision_with_other_shapes()

				if len(self.tidy_shapes) > 0:

					self.draw_tidy_shapes()					

					# Check if line can be destroyed

					if self.start_new_object:

						for yline in self.ylines:
							abc = yline['y']

							yline['cc'] = 0

							for sh in reversed(self.tidy_shapes):
								for z,rect in reversed(list(enumerate(sh.shape_list))):			
									if abc == rect.y:
										yline['cc'] +=1
										self.shape_to_remove.append({'y':abc,'shape':sh.num,'shape_ind':z})

							if yline['cc'] == 6:

								self.score += 10

								self.delete_rects_on_break_line(abc)
								self.delete_empty_shapes(self.shape_remove)
								self.move_down_left_shapes(self.tidy_shapes,abc)						

								# Reset case_on_line					
								yline['cc'] = 0

				self.reset_values_end_loop()
				pygame.display.flip()