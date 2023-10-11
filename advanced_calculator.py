from simple_calculator import SimpleCalculator
from stack import Stack
from simple_calculator import SimpleCalculatorModified

class AdvancedCalculator(SimpleCalculator):
	def __init__(self):
		"""
		Call super().__init__()
		Instantiate any additional data attributes
		"""
		self.operators = ["+", "-", "*", "/"]
		self.history = []

	def evaluate_expression(self, input_expression):
		"""
		Evaluate the input expression and return the output as a float
		Return a string "Error" if the expression is invalid
		"""
		checker = self.operators + ["(", ")", "{", "}"]
		list_tokens = self.destring(self.tokenize(input_expression))
		for token in list_tokens:
			if token not in checker and not token.isnumeric():
				return "Error"
		value = self.evaluate_list_tokens(list_tokens)
		self.history.insert(0, (input_expression, value))
		return value

	def tokenize(self, input_expression): # Done
		"""
		convert the input string expression to tokens, and return this list
		Each token is either an integer operand or a character operator or bracket
		"""
		length = len(input_expression)
		splitters = self.operators + ["(", ")", "{", "}"]
		min_idx = length
		for symbol in splitters:
			index = input_expression.find(symbol)
			if index != -1 and min_idx > index:
				min_idx = index
		tokens = [input_expression[:min_idx].strip()]
		i = min_idx
		while i < length:
			if input_expression[i] in splitters:
				tokens.append(input_expression[i])
				j = i+1
				s = ""
				while j < length and input_expression[j] not in splitters:
					s += input_expression[j]
					j += 1
				tokens.append(s.strip())
			i = j-1
			i += 1

		f = [i for i in tokens if i != ""]
		modified_tokens = []
		for j in f:
			if j.isnumeric():
				modified_tokens.append(int(j))
			else:
				modified_tokens.append(j)
		return modified_tokens
	def destring(self, tokens):
		modified = []
		for token in tokens:
			if type(token) == int:
				modified.append(str(token))
			else:
				modified.append(token)
		return modified

	def check_brackets(self, list_tokens): # Done
		"""
		check if brackets are valid, that is, all open brackets are closed by the same type 
		of brackets. Also () contain only () brackets.
		Return True if brackets are valid, False otherwise
		"""
		# using stack
		b = Stack()
		brackets = [token for token in list_tokens if token in ("(", ")", "{", "}")]
		for brack in brackets:
			if brack == "{":
				if "(" in b.__str__():
					return False
				b.push(brack)
			elif brack == "}":
				if ")" in b.__str__():
					return False
				if "{" ==b.peek():
					b.pop()
				else:
					b.push("}")
			elif brack == "(":
				b.push(brack)
			else:
				if "(" == b.peek():
					b.pop()
				else:
					b.push(")")
		return b.is_empty()
	def calculate_advanced(self, tokens):
		calculator = SimpleCalculatorModified()
		value = 0
		try:
			while len(tokens) != 1:
				add = False
				pass1 = False
				if "/" in tokens:
					index = tokens.index("/")
				elif "*" in tokens:
					index = tokens.index("*")
				elif "+" in tokens:
					add = True
					index = tokens.index("+")
				else:
					index = tokens.index("-")
				exp = "".join(tokens[index-1:index+2])
				if add:
					try:
						if tokens[index-2]=="-":
							pass1 = True
							exp1 = f"{tokens[index + 1]}-{tokens[index - 1]}"
							value = calculator.evaluate_expression(exp1)
							if float(value) < 0 or float(value) != 0:
								tokens = tokens[:index-2]+["+"]+[str(value)]+tokens[index+2:]
							else:
								tokens = tokens[:index-2]+["+"]+tokens[index+2:]
							continue
					except Exception:
						pass
				value = calculator.evaluate_expression(exp)
				tokens = tokens[:index-1] + [str(float(value))] + tokens[index+2:]
		except Exception:
			return "Error"
		return tokens[0]
	def solving_parantheses_exp(self, tokens):
		while len(tokens) != 1:
			try:
				index2 = tokens.index(")")
				index1 = next((i for i in range(index2, -1, -1) if tokens[i] == "("), 0)
			except ValueError:
				value = self.calculate_advanced(tokens)
				break
			exp = tokens[index1+1: index2]
			value = self.calculate_advanced(exp)
			tokens = tokens[:index1] + [str(float(value))] + tokens[index2+1:]
		return str(float(value))
	def solving_curly(self, tokens):
		# for solving {{3+4}*5}
		while len(tokens) != 1:
			try:
				index2 = tokens.index("}")
				index1 = next((i for i in range(index2, -1, -1) if tokens[i] == "{"), 0)
			except ValueError:
				value = self.calculate_advanced(tokens)
				break
			exp = tokens[index1+1: index2]
			value = self.calculate_advanced(exp)
			tokens = tokens[:index1] + [str(float(value))] + tokens[index2+1:]
		return str(float(value))
	def evaluate_list_tokens(self, list_tokens):
		"""
		Evaluate the expression passed as a list of tokens
		Return the final answer as a float, and "Error" in case of division by zero and other errors
		"""
		list_tokens = self.destring(list_tokens)
		if not self.check_brackets(list_tokens):
			return "Error"
		try:
			while "(" in list_tokens:
				index2 = list_tokens.index(")")
				index1 = next((i for i in range(index2, -1, -1) if list_tokens[i] == "("), 0)
				if index2 - index1 == 2:
					list_tokens = list_tokens[:index1] + [list_tokens[index1+1]] + list_tokens[index2+1:]
					continue
				exp = list_tokens[index1+1:index2]
				list_tokens = list_tokens[:index1] + [self.solving_parantheses_exp(exp)] + list_tokens[index2+1:]
			while "{" in list_tokens:
				index2 = list_tokens.index("}")
				index1 = next((i for i in range(index2, -1, -1) if list_tokens[i] == "{"), 0)
				if index2-index1==2:
					list_tokens = list_tokens[:index1] + [list_tokens[index1+1]] + list_tokens[index2+1:]
					continue
				exp = list_tokens[index1+1:index2]
				list_tokens = list_tokens[:index1] + [self.solving_curly(exp)] + list_tokens[index2+1:]
			return float(self.calculate_advanced(list_tokens))
		except Exception:
			return "Error"


	def get_history(self): # Done
		"""
		Return history of expressions evaluated as a list of (expression, output) tuples
		The order is such that the most recently evaluated expression appears first 
		"""
		return self.history

if __name__ == "__main__":
    exp = "(2+3)/(2+(3-4+1))"
    calc = AdvancedCalculator()
    print(calc.evaluate_expression(exp))