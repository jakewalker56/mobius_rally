import random
from cell import Cell
from move import Move

class Board:

	def __init__(self, width, height, origin_x, origin_y, target_x, target_y):
	    self.cells = [[Cell(i, j) for j in range(height)] for i in range(width)]
	    self.width = width
	    self.height = height
	    self.origin = self.cells[origin_x][origin_y]
	    self.target = self.cells[target_x][target_y]
	    self.vertical_wrapping = True
	    self.horizontal_wrapping = True
	    #random.seed(random_seed)

	def uncovered_cell_blockers(self, move):
		# return a set of cells, at least one of which must contain a blocker in order for associated move to remain valid
		# Specifically, a move in a given direction is only valid if a blocker is eventually placed between the source cell and the nearest already accessed cell in the opposite direction
		# of the source->target move
		blocker_list = []
		uncovered_path = False
		if move.direction == 'L':
			# look for untraversed cells between here and the nearest (possibly implied) blocker to the right that have already been accessed
			steps = move.source.x - move.target.x
			if self.horizontal_wrapping == True and steps < 0:
				steps = steps + self.width
			if steps < 1:
				# attempted to move outside of boundaries
				print("something went wrong - out of bounds move attempt")
			#steps is the number of steps in the move itself; we traverse a maximum of self.width - steps in the opposite direction
			for x in range(1, self.width - steps):
				i = move.source.x + x
				if self.horizontal_wrapping == True and i >= self.width:
					i = i - self.width
				if i >= self.width or self.cells[i][move.source.y].times_used_as_blocker > 0:
					#found a blocker, don't need to keep checking
					break
				if not self.cells[i][move.source.y].path_to_cell and self.cells[i][move.source.y].traversal_count == 0:
					#found an empty cell that can be filled with a blocker 
					blocker_list.append(self.cells[i][move.source.y])
				if self.cells[i][move.source.y].path_to_cell or (self.origin.x == i and self.origin.y == move.source.y):
					#found a previously visited cell with no blocker in between.  Set the bool and bail out with the current blocker list
					uncovered_path = True
					break
				
		elif move.direction == 'R':
			steps = move.target.x - move.source.x
			if self.horizontal_wrapping == True and steps < 0:
				steps = steps + self.width
			if steps < 1:
				print("something went wrong - out of bounds move attempt")
			for x in range(1, self.width - steps):
				i = move.source.x - x
				if self.horizontal_wrapping == True and i < 0:
					i = i + self.width
				if i < 0 or self.cells[i][move.source.y].times_used_as_blocker > 0:
					#found a blocker, don't need to keep checking
					break
				if not self.cells[i][move.source.y].path_to_cell and self.cells[i][move.source.y].traversal_count == 0:
					#found an empty cell that can be filled with a blocker 
					blocker_list.append(self.cells[i][move.source.y])
				if self.cells[i][move.source.y].path_to_cell or (self.origin.x == i and self.origin.y == move.source.y):
					#found a previously visited cell with no blocker in between.  Set the bool and bail out with the current blocker list
					uncovered_path = True
					break
				
		elif move.direction == 'U':
			steps = move.source.y - move.target.y
			if self.vertical_wrapping == True and steps < 0:
				steps = steps + self.height
			if steps < 1:
				print("something went wrong - out of bounds move attempt")
			for y in range(1, self.height - steps):
				j = move.source.y + y
				if self.vertical_wrapping == True and j >= self.height:
					j = j - self.height
				if j >= self.height or self.cells[move.source.x][j].times_used_as_blocker > 0:
					#found a blocker, don't need to keep checking
					break
				if not self.cells[move.source.x][j].path_to_cell and self.cells[move.source.x][j].traversal_count == 0:
					#found an empty cell that can be filled with a blocker 
					blocker_list.append(self.cells[move.source.x][j])
				if self.cells[move.source.x][j].path_to_cell or (self.origin.x == move.source.x and self.origin.y == j):
					#found a previously visited cell with no blocker in between.  Set the bool and bail out with the current blocker list
					uncovered_path = True
					break
				
		elif move.direction == 'D':
			steps = move.target.y - move.source.y
			if self.vertical_wrapping == True and steps < 0:
				steps = steps + self.height
			if steps < 1:
				print("something went wrong - out of bounds move attempt")
			for y in range(1, self.height - steps):
				j = move.source.y - y
				if self.vertical_wrapping == True and j < 0:
					j = j + self.height
				if j < 0 or self.cells[move.source.x][j].times_used_as_blocker > 0:
					#found a blocker, don't need to keep checking
					break
				if not self.cells[move.source.x][j].path_to_cell and self.cells[move.source.x][j].traversal_count == 0:
					#found an empty cell that can be filled with a blocker 
					blocker_list.append(self.cells[move.source.x][j])
				if self.cells[move.source.x][j].path_to_cell or (self.origin.x == move.source.x and self.origin.y == j):
					#found a previously visited cell with no blocker in between.  Set the bool and bail out with the current blocker list
					uncovered_path = True
					break

		return uncovered_path, blocker_list


	def is_valid_move(self, move):
		#if a move passes through a cell that has already been accessed, then that move is invalid (because it could have been accomplished already)
		if move.source.x == move.target.x and move.source.y == move.target.y:
			print("invalid self move attempted")
		if move.direction == 'L':
			# check there are no blockers while traveling left
			steps = move.source.x - move.target.x
			if self.horizontal_wrapping == True and steps < 0:
				steps = steps + self.width
			if steps < 1:
				# attempted to move outside of boundaries
				return False
			#validate no blockers between source and target
			for x in range(1, steps + 1):
				i = move.source.x - x
				if self.horizontal_wrapping == True and i < 0:
					i = i + self.width
				if self.cells[i][move.source.y].times_used_as_blocker > 0 or self.cells[i][move.source.y].path_to_cell:
					return False
			#validate that we can place a blocker in the next cell
			if move.target.x == 0:
				if self.horizontal_wrapping == True:
					next_cell = self.cells[move.target.x - 1 + self.width][move.target.y]
				else:
					# if we're not horizontal wrapping, edges count as blockers, so nothing to do here
					return True
			else:
				next_cell = self.cells[move.target.x - 1][move.target.y]
		elif move.direction == 'R':
			# check there are no blockers while traveling right
			steps = move.target.x - move.source.x
			if self.horizontal_wrapping == True and steps < 0:
				steps = steps + self.width
			if steps < 1:
				return False
			#validate no blockers between source and target
			for x in range(1, steps + 1):
				i = move.source.x + x
				if self.horizontal_wrapping == True and i >= self.width:
					i = i - self.width
				if self.cells[i][move.source.y].times_used_as_blocker > 0 or self.cells[i][move.source.y].path_to_cell:
					return False
			#validate that we can place a blocker in the next cell
			if move.target.x + 1 == self.width:
				if self.horizontal_wrapping == True:
					next_cell = self.cells[move.target.x + 1 - self.width][move.target.y]
				else:
					# if we're not horizontal wrapping, edges count as blockers, so nothing to do here
					return True
			else:
				next_cell = self.cells[move.target.x + 1][move.target.y]
		elif move.direction == 'U':
			# check there are no blockers while traveling up
			steps = move.source.y - move.target.y
			if self.vertical_wrapping == True and steps < 0:
				steps = steps + self.height
			if steps < 1:
				return False
			#validate no blockers between source and target
			for y in range(1, steps + 1):
				j = move.source.y - y
				if self.vertical_wrapping == True and j < 0:
					j = j + self.height
				if self.cells[move.source.x][j].times_used_as_blocker > 0 or self.cells[move.source.x][j].path_to_cell:
					return False
			#validate that we can place a blocker in the next cell
			if move.target.y == 0:
				if self.vertical_wrapping == True:
					next_cell = self.cells[move.target.x][move.target.y - 1 + self.height]
				else:
					# if we're not vertical wrapping, edges count as blockers, so nothing to do here
					return True
			else:
				next_cell = self.cells[move.target.x][move.target.y - 1]
		elif move.direction == 'D':
			# check there are no blockers while traveling down
			steps = move.target.y - move.source.y
			if self.vertical_wrapping == True and steps < 0:
				steps = steps + self.height
			if steps < 1:
				return False
			#validate no blockers between source and target
			for y in range(1, steps + 1):
				j = move.source.y + y
				if self.vertical_wrapping == True and j >= self.height:
					j = j - self.height
				if self.cells[move.source.x][j].times_used_as_blocker > 0 or self.cells[move.source.x][j]:
					return False
			#validate that we can place a blocker in the next cell
			if move.target.y + 1 == self.height:
				if self.vertical_wrapping == True:
					next_cell = self.cells[move.target.x][move.target.y + 1 - self.height]
				else:
					# if we're not vertical wrapping, edges count as blockers, so nothing to do here
					return True
			else:
				next_cell = self.cells[move.target.x][move.target.y + 1]
		if next_cell.traversal_count > 0:
			#this cell must remain clear because it has been traversed by previous moves
			return False

		# Even if the move itself is valid, there may be an already accessed cell in the opposite direction.  
		# In this case, a move in the target direction is only valid if a blocker is eventually placed between the source cell and the already accessed cell.
		move.spanning_blocker_required, move.spanning_blocker_list = self.uncovered_cell_blockers(move)

		#if there are no remaining valid places to place a blocker AND a blocker is needed, this is not a valid move
		if move.spanning_blocker_required and not move.spanning_blocker_list:
			return False
	
		return True

	def valid_moves(self, current_cell, direction):
		print("finding valid moves from:", end="")
		current_cell.print()

		valid_moves = []
		if direction == 'L':
			for i in range(1, self.width):
				target_cell = []
				if current_cell.x - i < 0:
					if self.horizontal_wrapping == True:
						target_cell = self.cells[current_cell.x - i + self.width][current_cell.y]
				else:
					target_cell = self.cells[current_cell.x - i][current_cell.y]
				if target_cell:
					move = Move(current_cell, target_cell, direction)
					if self.is_valid_move(move):
						valid_moves.append(move)
		elif direction == 'R':
			for i in range(1, self.width):
				target_cell = []
				if current_cell.x + i >= self.width:
					if self.horizontal_wrapping == True:
						target_cell = self.cells[current_cell.x + i - self.width][current_cell.y]
				else:
					target_cell = self.cells[current_cell.x + i][current_cell.y]
				if target_cell:
					move = Move(current_cell, target_cell, direction)
					if self.is_valid_move(move):
						valid_moves.append(move)
		elif direction == 'U':
			for j in range(1, self.height):
				target_cell = []
				if current_cell.y - j < 0:
					if self.vertical_wrapping == True:
						target_cell = self.cells[current_cell.x][current_cell.y - j + self.height]
				else:
					target_cell = self.cells[current_cell.x][current_cell.y - j]
				if target_cell:
					move = Move(current_cell, target_cell, direction)
					if self.is_valid_move(move):
						valid_moves.append(move)
		elif direction == 'D':
			for j in range(1, self.height):
				target_cell = []
				if current_cell.y + j >= self.height:
					if self.vertical_wrapping == True:
						target_cell = self.cells[current_cell.x][current_cell.y + j - self.height]
				else:
					target_cell = self.cells[current_cell.x][current_cell.y + j]
				if target_cell:
					move = Move(current_cell, target_cell, direction)
					if self.is_valid_move(move):
						valid_moves.append(move)

		print("returning " + str(len(valid_moves)) + " valid " + str(direction) + " moves")
		return valid_moves


	def update_with_move(self, move):
		print("updating board with move")
		move.print()
		
		if move.source.path_to_cell:
			move.target.path_to_cell = move.source.path_to_cell[:]
			move.target.path_to_cell.append(move)
		else:
			move.target.path_to_cell = [move]
		

		if move.direction == 'L':
			steps = move.source.x - move.target.x
			if self.horizontal_wrapping == True and steps < 0:
				steps = steps + self.width
			if steps < 1:
				# something went wrong
				print("unexpected number of steps: " + str(steps))	
			for x in range(steps + 1):
				i = move.source.x - x
				if self.horizontal_wrapping == True and i < 0:
					i = i + self.width
				self.cells[i][move.source.y].traversal_count = self.cells[i][move.source.y].traversal_count + 1		
			#place a blocker in the next cell
			if move.target.x == 0:
				if self.horizontal_wrapping == True:
					next_cell = self.cells[move.target.x - 1 + self.width][move.target.y]
				else:
					# if we're not horizontal wrapping, edges count as blockers, so nothing to do here
					return
			else:
				next_cell = self.cells[move.target.x - 1][move.target.y]
		elif move.direction == 'R':
			steps = move.target.x - move.source.x
			if self.horizontal_wrapping == True and steps < 0:
				steps = steps + self.width
			if steps < 1:
				# something went wrong
				print("unexpected number of steps: " + str(steps))	
			for x in range(steps + 1):
				i = move.source.x + x
				if self.horizontal_wrapping == True and i >= self.width:
					i = i - self.width
				self.cells[i][move.source.y].traversal_count = self.cells[i][move.source.y].traversal_count + 1		
			#place a blocker in the next cell
			if move.target.x +1 == self.width:
				if self.horizontal_wrapping == True:
					next_cell = self.cells[move.target.x + 1 - self.width][move.target.y]
				else:
					# if we're not horizontal wrapping, edges count as blockers, so nothing to do here
					return
			else:
				next_cell = self.cells[move.target.x + 1][move.target.y]
		elif move.direction == 'U':
			steps = move.source.y - move.target.y
			if self.vertical_wrapping == True and steps < 0:
				steps = steps + self.height
			if steps < 1:
				# something went wrong
				print("unexpected number of steps: " + str(steps))	
			for y in range(steps + 1):
				j = move.source.y - y
				if self.vertical_wrapping == True and j < 0:
					j = j + self.height
				self.cells[move.source.x][j].traversal_count = self.cells[move.source.x][j].traversal_count + 1		
			#place a blocker in the next cell
			if move.target.y == 0:
				if self.vertical_wrapping == True:
					next_cell = self.cells[move.target.x][move.target.y - 1 + self.height]
				else:
					# if we're not vertical wrapping, edges count as blockers, so nothing to do here
					return
			else:
				next_cell = self.cells[move.target.x][move.target.y - 1]
		elif move.direction == 'D':
			steps = move.target.y - move.source.y
			if self.vertical_wrapping == True and steps < 0:
				steps = steps + self.height
			if steps < 1:
				# something went wrong
				print("unexpected number of steps: " + str(steps))	
			for y in range(steps + 1):
				j = move.source.y + y
				if self.vertical_wrapping == True and j >= self.height:
					j = j - self.height
				self.cells[move.source.x][j].traversal_count = self.cells[move.source.x][j].traversal_count + 1		
			#place a blocker in the next cell
			if move.target.y + 1 == self.height:
				if self.vertical_wrapping == True:
					next_cell = self.cells[move.target.x][move.target.y  + 1 - self.height]
				else:
					# if we're not vertical wrapping, edges count as blockers, so nothing to do here
					return
			else:
				next_cell = self.cells[move.target.x][move.target.y + 1]

		next_cell.times_used_as_blocker = next_cell.times_used_as_blocker + 1

		#if there is exactly one available place to put a spanning blocker, we can place it now, but we must track it so that we can roll it back if we eventually rescind this move
		if move.spanning_blocker_required and len(move.spanning_blocker_list) == 1:
			move.spanning_blocker_list[0].times_used_as_blocker = move.spanning_blocker_list[0].times_used_as_blocker + 1
			move.blocker_placed = move.spanning_blocker_list[0]
		#there is more than one valid way to place a blocker currently, we must enforce this as a final processing stage

		return


	def rescind_move(self, move):
		print("rescinding most recent move: ")
		move.print()
		move.target.path_to_cell = ()

		if move.direction == 'L':
			steps = move.source.x - move.target.x
			if self.horizontal_wrapping == True and steps < 0:
				steps = steps + self.width
			if steps < 1:
				# something went wrong
				print("unexpected number of steps: " + str(steps))	
			#validate no blockers between source and target
			for x in range(steps + 1):
				i = move.source.x - x
				if self.horizontal_wrapping == True and i < 0:
					i = i + self.width
				self.cells[i][move.source.y].traversal_count = self.cells[i][move.source.y].traversal_count - 1		
			#place a blocker in the next cell
			if move.target.x == 0:
				if self.horizontal_wrapping == True:
					next_cell = self.cells[move.target.x - 1 + self.width][move.target.y]
				else:
					# if we're not horizontal wrapping, edges count as blockers, so nothing to do here
					return
			else:
				next_cell = self.cells[move.target.x - 1][move.target.y]
		elif move.direction == 'R':
			steps = move.target.x - move.source.x
			if self.horizontal_wrapping == True and steps < 0:
				steps = steps + self.width
			if steps < 1:
				# something went wrong
				print("unexpected number of steps: " + str(steps))	
			#validate no blockers between source and target
			for x in range(steps + 1):
				i = move.source.x + x
				if self.horizontal_wrapping == True and i >= self.width:
					i = i - self.width
				self.cells[i][move.source.y].traversal_count = self.cells[i][move.source.y].traversal_count - 1		
			#place a blocker in the next cell
			if move.target.x +1 == self.width:
				if self.horizontal_wrapping == True:
					next_cell = self.cells[move.target.x + 1 - self.width][move.target.y]
				else:
					# if we're not horizontal wrapping, edges count as blockers, so nothing to do here
					return
			else:
				next_cell = self.cells[move.target.x + 1][move.target.y]
		elif move.direction == 'U':
			steps = move.source.y - move.target.y
			if self.vertical_wrapping == True and steps < 0:
				steps = steps + self.height
			if steps < 1:
				# something went wrong
				print("unexpected number of steps: " + str(steps))	
			#validate no blockers between source and target
			for y in range(steps + 1):
				j = move.source.y - y
				if self.vertical_wrapping == True and j < 0:
					j = j + self.height
				self.cells[move.source.x][j].traversal_count = self.cells[move.source.x][j].traversal_count - 1		
			#place a blocker in the next cell
			if move.target.y == 0:
				if self.vertical_wrapping == True:
					next_cell = self.cells[move.target.x][move.target.y - 1 + self.height]
				else:
					# if we're not vertical wrapping, edges count as blockers, so nothing to do here
					return
			else:
				next_cell = self.cells[move.target.x][move.target.y - 1]
		elif move.direction == 'D':
			steps = move.target.y - move.source.y
			if self.vertical_wrapping == True and steps < 0:
				steps = steps + self.height
			if steps < 1:
				# something went wrong
				print("unexpected number of steps: " + str(steps))	
			#validate no blockers between source and target
			for y in range(steps + 1):
				j = move.source.y + y
				if self.vertical_wrapping == True and j >= self.height:
					j = j - self.height
				self.cells[move.source.x][j].traversal_count = self.cells[move.source.x][j].traversal_count - 1		
			#place a blocker in the next cell
			if move.target.y + 1 == self.height:
				if self.vertical_wrapping == True:
					next_cell = self.cells[move.target.x][move.target.y  + 1 - self.height]
				else:
					# if we're not vertical wrapping, edges count as blockers, so nothing to do here
					return
			else:
				next_cell = self.cells[move.target.x][move.target.y + 1]

		next_cell.times_used_as_blocker = next_cell.times_used_as_blocker - 1

		#rollback any blockers placed for uncovered landing cells
		if move.blocker_placed:
			move.blocker_placed.times_used_as_blocker = move.blocker_placed.times_used_as_blocker - 1		

		return

	def validate_solution_uniqueness(self):
		print("TODO: implement validate_solution_uniqueness()")
		#just because a solution exists, doesn't mean it is unique; we check to avoid loops in the original solution, but we still need to check the full 
		# set of permutation branches if we're looking for a unique solution
		return True

	def recursive_solve(self, remaining_steps, current_cell):
		print("recursive solve current board state:")
		self.print()
		if remaining_steps < 0:
			return false
		if remaining_steps == 0:
			if current_cell == self.target:
				# found a viable solution, but need to ensure it's a minimal solution as well
				print("found valid solution; checking for minimality...")
				#	For any move that has at least one element in its blocker list, at least one of them must be blocked
				for move in current_cell.path_to_cell:
					#   For any list that has none currently blocked, we check if they all have at least one that is still open for filling
					move.print()
					print(move.spanning_blocker_required)
					print(len(move.spanning_blocker_list))
					if move.spanning_blocker_required:
						num_viable_cells = 0
						already_satisfied = False
						for cell in move.spanning_blocker_list:
							cell.print()
							if cell.times_used_as_blocker > 0: 
								already_satisfied = True
							if cell.traversal_count == 0:
								num_viable_cells = num_viable_cells + 1
						if not already_satisfied and num_viable_cells < 1:
							#not a valid solution because some landing cells are uncoverable
							return False
				# If we got here, all lists have at least one available slot, we place a blocker in a random valid place for each list
				for move in current_cell.path_to_cell:
					if move.spanning_blocker_required:
						viable_cells = []
						for cell in move.spanning_blocker_list:
							if cell.times_used_as_blocker > 0: 
								continue
							if cell.traversal_count == 0:
								viable_cells.append(cell)
						i = random.randint(0, len(viable_cells))
						viable_cells[i].times_used_as_blocker = viable_cells[i].times_used_as_blocker + 1	
				return True
			else:
				return False

		'''can't ever go back the same direction we just came from, or the same direction we just went '''
		if not current_cell.path_to_cell:
			print("all directions available")
			available_directions = ['U', 'D', 'L', 'R']
		else:
			last_direction = current_cell.path_to_cell[-1].direction
			if last_direction == 'L' or last_direction == 'R':
				available_directions = ['U', 'D']
			if last_direction == 'U' or last_direction == 'D':
				available_directions = ['L', 'R']

		random.shuffle(available_directions)

		for direction in available_directions:
			valid_moves = self.valid_moves(current_cell, direction)
			for move in valid_moves:
				move.print()
			#randomize order to try valid moves in depth-first search
			random.shuffle(valid_moves)
			for move in valid_moves:
				self.update_with_move(move)
				if self.recursive_solve(remaining_steps - 1, self.cells[move.target.x][move.target.y]) == True:
					# valid solution found; we're done.  Return true and don't change the board state
					return True
				else:
					# unwind the last move and continue the loop to try again with the next valid move
					self.rescind_move(move)
					self.print()
		return False
		

	def find_solution(self, steps):
		''' Recursive algorithm: 

			1. for each available direction,
			2. for each valid unvisited cell in that direction,
			3. add a blocker (if required and a valid blocker)
			4. update the board, cells, current location
			5. back to 1

		'''

		solution_found = self.recursive_solve(steps, self.origin)
		if solution_found == True:
			# a valid solution is not guaranteed to be unique
			print("solution found!")
			return self.validate_solution_uniqueness()
		return False
				

	def print(self):
		print("times_used_as_blocker:\n[")
		for j in range(self.height):
			for i in range(self.width):
				print(str(self.cells[i][j].times_used_as_blocker) + ",", end='')
			print("")
		print("]")

		print("traversal_count:\n[")
		for j in range(self.height):
			for i in range(self.width):
				print(str(self.cells[i][j].traversal_count) + ",", end='')
			print("")
		print("]")
		
		if self.target.path_to_cell:
			print("solution found!")
			print("source: ", end="")
			self.origin.print()
			print("target: ", end="")
			self.target.print()
			for move in self.target.path_to_cell:
				move.print()


	def print_formatted(self):
		print("")
		for move in self.target.path_to_cell:
			print(str(move.direction), end="")
		print("")
		for j in range(self.height):
			for i in range(self.width):
				if self.origin.x == i and self.origin.y == j: 
					print("S", end="")
				elif self.target.x == i and self.target.y == j: 
					print("E", end="")
				elif self.cells[i][j].times_used_as_blocker > 0:
					print("x", end='')
				elif self.cells[i][j].traversal_count > 0:
					print("*", end="")
				else:
					print(" ", end="")
			print("")
		print("]")

