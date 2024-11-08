import json
import random
import sys
import itertools
import time
from board import Board
from cell import Cell
from move import Move

start = time.time()

with open("config.json", "r") as read_content:
	spec = json.load(read_content)

def main():

	board = Board(spec["width"], spec["height"], spec["origin_x"], spec["origin_y"], spec["target_x"], spec["target_y"])
	board.find_solution(spec["steps"])
	board.print()
	board.print_formatted()

	'''
	"width" : 11,
	"height" : 21,
	"blockers" : 10,
	"origin_x" : 6,
	"origin_y" : 0,
	"steps" : 15
	'''

main()