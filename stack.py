class Stack:
	def __init__(self):
		# Initialise the stack's data attributes
		self.arr = []
	
	def push(self, item):
		# Push an item to the stack
		self.arr.insert(0, item)

	def peek(self):
		# Return the element at the top of the stack
		# Return a string "Error" if stack is empty
		return "Error" if self.is_empty() else self.arr[0]

	def pop(self):
		# Pop an item from the stack if non-empty
		if self.is_empty(): return "Error"
		if not self.is_empty(): f=self.arr.pop(0)
		return f

	def is_empty(self):
		# Return True if stack is empty, False otherwise
		return self.arr == []

	def __str__(self):
		# Return a string containing elements of current stack in top-to-bottom order, separated by spaces
		# Example, if we push "2" and then "3" to the stack (and don't pop any elements), 
		# then the string returned should be "3 2"
		return " ".join([str(i) for i in self.arr])

	def __len__(self):
		# Return current number of elements in the stack
		return len(self.arr)

if __name__ == "__main__":
	f = Stack()
	f.push(4)
	print(f.pop())
	print(f.is_empty())