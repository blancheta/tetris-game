#!/usr/bin/python3

from pygame import Rect
from shape import Shape

class Shape_u(Shape):

	def __init__(self,num):
		super(Shape_u,self).__init__(num)
		self.shape_list = [Rect(0,0,50,50),Rect(100,0,50,50),Rect(0,50,50,50),Rect(50,50,50,50),Rect(100,50,50,50)]
	
	def move(self,up_push_count):

		if up_push_count == 1:
			self.rota90()

		elif up_push_count == 2:
			self.rota180()

		elif up_push_count == 3:
			self.rota270()

		elif up_push_count == 4:
			self.rota360()
			up_push_count = 0

		return up_push_count


	def rota90(self):

		new_form = self.shape_list

		new_form[1].x -= 50

		new_form[3].x -= 50
		new_form[3].y += 50

		new_form[4].x -= 50
		new_form[4].y += 50

		self.shape_list = new_form

	def rota180(self):

		new_form = self.shape_list

		new_form[3].x += 100
		new_form[3].y -= 100

		new_form[4].x += 50
		new_form[4].y -= 50

		self.shape_list = new_form

	def rota270(self):

		new_form = self.shape_list

		new_form[2].y += 50

		new_form[3].x -= 50
		new_form[3].y += 50

		new_form[4].x -= 50
		new_form[4].y += 50


		self.shape_list = new_form

	def rota360(self):

		new_form = self.shape_list

		# 0
		new_form[1].x += 50
		new_form[2].y -= 50
		# 3
		new_form[4].x += 50
		new_form[4].y -= 50
		
		self.shape_list = new_form
