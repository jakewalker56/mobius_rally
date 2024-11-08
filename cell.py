from move import Move

class Cell:

	def __init__(self, x, y):
	    ''' indicates how many moves have relied on this cell containing a blocker. Any number > 0 implies this cell is untraverseable'''
	    self.times_used_as_blocker = 0
	    ''' path_to_cell is the list of moves necessary to reach this cell from the origin point.'''
	    self.path_to_cell = []
   	    
		# traversal_count indicates how many times this cell has already been traversed by a previous move and therefore cannot be filled by a blocker'''
		# it is a counter rather than a binary so we can easily unwind moves in a recursive format'''
	    self.traversal_count = 0
	    self.x = x
	    self.y = y

	def print(self):
		print("(" + str(self.x) + ", " + str(self.y)  + ")")
	


	
