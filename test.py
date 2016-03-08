#!/usr/bin/python3

from operator import itemgetter
from itertools import groupby

rows = [
	{ 'shape': 2, 'shape_ind': 0},
	{ 'shape': 2, 'shape_ind': 0},
	{ 'shape': 3, 'shape_ind': 0},
	{ 'shape': 1, 'shape_ind': 1}
]

rows.sort(key=itemgetter('shape'))

for row,items in groupby(rows,key=itemgetter('shape')):

	print(row)

	for i in items:
		print("		",i)
