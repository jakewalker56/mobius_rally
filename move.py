class Move:

	def __init__(self, source, target, direction):
		self.source = source
		self.target = target
		self.direction = direction
		self.spanning_blocker_required = False
		self.spanning_blocker_list = []
		self.blocker_placed = False

	def print(self):
		print("  source: (" + str(self.source.x) + ", " + str(self.source.y) + ")")
		print("  target: (" + str(self.target.x) + ", " + str(self.target.y) + ")")
		print("  direction: " + str(self.direction))