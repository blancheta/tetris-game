#!/usr/bin/python3

from pygame import Rect

class Shape:

	def __init__(self,num,name,color):

		self.num = num
		self.name = name
		self.color = color
		self.shape_list = []


	def init_shape_list(self,shape_list):

		self.shape_list = shape_list
