#!/usr/bin/python3

from pygame import Rect
from shape import Shape

class Shape_square(Shape):

	def __init__(self,num,name,color):
		super(Shape_s,self).__init__(num,name,color)
		self.shape_list = [Rect(0,50,50,50)]

	def move(self,up_push_count):
		return up_push_count