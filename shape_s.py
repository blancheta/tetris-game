#!/usr/bin/python3

from pygame import Rect
from shape import Shape

class Shape_s(Shape):

	def __init__(self,num,name,color):
		super(Shape_s,self).__init__(num,name,color)
		self.shape_list = [Rect(50,0,50,50),Rect(100,0,50,50),Rect(0,50,50,50),Rect(50,50,50,50)]
	def rota180(self):

		new_form = self.shape_list

		new_form[0].x -= 50

		new_form[1].x -= 50
		new_form[1].y += 100

		self.shape_list = new_form

	def rota360(self):

		new_form = self.shape_list

		new_form[0].x += 50

		new_form[1].x += 50
		new_form[1].y -= 100

		self.shape_list = new_form

	def move(self,up_push_count):

			if up_push_count == 1:
				self.rota180()
			else:
				up_push_count = 0
				self.rota360()

			return up_push_count