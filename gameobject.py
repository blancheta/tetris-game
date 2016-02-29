#!/usr/bin/python3
import pygame,sys

class GameObject:

	def __init__(self):

		self.shape_rect = Rect(0,0,50,50)

	def init_pos(self,pos):

		# Init position
		self.shape_rect.x, self.shape_rect.y = pos



