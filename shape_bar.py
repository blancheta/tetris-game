#!/usr/bin/python3

from pygame import Rect
from shape import Shape

class Shape_bar(Shape):

	def __init__(self,num,name,color):
		super(Shape_bar,self).__init__(num,name,color)
		self.init_shape_list()
	
	def init_shape_list(self):
		self.shape_list = [Rect(0,-50,50,50),Rect(50,-50,50,50),Rect(100,-50,50,50)]

	def rota180(self):

		new_form = self.shape_list

		new_form[1].x -= 50
		new_form[1].y += 50

		new_form[2].x -= 100
		new_form[2].y += 100

		self.shape_list = new_form

	def rota360(self):

		new_form = self.shape_list

		new_form[1].x += 50
		new_form[1].y -= 50

		new_form[2].x += 100
		new_form[2].y -= 100

		self.shape_list = new_form

	def move(self,up_push_count):

		if up_push_count == 1:
			self.rota180()
		else:
			self.rota360()
			up_push_count = 0
		return up_push_count