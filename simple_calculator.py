class SimpleCalculator:
    def __init__(self):
        self.operators = ["+", "-", "*", "/"]
        self.history = []
    def check_errors(self, input_expression):
        operate = None
        indexes = None
        count = 0
        for _ in input_expression:
            if _ in self.operators:
                count += 1
                operate = _
                indexes = input_expression.index(_)
            if _ not in self.operators and _ != " " and not _.isnumeric():
                return False

        if count > 1:
            return False
        if operate is None:
            return False
        # checking middle brackets
        point1 = []
        point2 = None
        point3 = []
        point4 = None
        for j in range(len(input_expression)):
            if input_expression[j] not in self.operators:
                if j < indexes:
                    if input_expression[j] != " ":
                        point1.append(j)
                    elif point2 is None:
                        point2 = j
                elif input_expression[j] == " ":
                    point4 = j
                else:
                    point3.append(j)
        if len(point1) > 1 and point2 != None and point1[0] < point2 < point1[-1]:
            return False
        return (
            len(point3) <= 1
            or point4 is None
            or not point3[0] < point4 < point3[-1]
        )

    def evaluate_expression(self, input_expression):
        """
		Evaluate the input expression and return the output as a float
		Return a string "Error" if the expression is invalid
		"""
        temp = input_expression
        input_expression = list(list(input_expression.strip()))
        if not self.check_errors(input_expression):
            self.history.insert(0, (temp, "Error"))
            return "Error"
        input_expression = [i for i in input_expression if i != " "]
        operate = None
        indexes = None
        if input_expression[0] in self.operators or input_expression[-1] in self.operators:
            self.history.insert(0, (temp, "Error"))
            return "Error"
        count = 0
        for _ in input_expression:
            if _ in self.operators:
                count += 1
                operate = _
                indexes = input_expression.index(_)
        try:
            nums = [float("".join(input_expression[:indexes])), float("".join(input_expression[indexes+1:]))]
        except ValueError:
            self.history.insert(0, (temp, "Error"))
            return "Error"
        if operate == "+":
            self.history.insert(0, (temp, nums[0]+nums[1]))
            return nums[0]+nums[1]
        elif operate == "-":
            self.history.insert(0, (temp, nums[0]-nums[1]))
            return nums[0]-nums[1]
        elif operate == "*":
            self.history.insert(0, (temp, nums[0]*nums[1]))
            return nums[0]*nums[1]
        else:
            if nums[1] == 0:
                self.history.insert(0, [temp, "Error"])
                return "Error"
            self.history.insert(0, (temp, nums[0]/nums[1]))
            return nums[0]/nums[1]
    
    def get_history(self):
        """
		Return history of expressions evaluated as a list of (expression, output) tuples
		The order is such that the most recently evaluated expression appears first 
        """
        return self.history
    

class SimpleCalculatorModified(object):
    def __init__(self):
        self.operators = ["+", "-", "*", "/"]
        self.history = []
    def get_history(self):
        return self.history[::-1]
    def tokenize(self, input_expression):
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
        return [i for i in tokens if i != ""]

    def evaluate_expression(self, input_expression):
        tokens = self.tokenize(input_expression)
        if tokens[0] in ["-", "+"]:
            tokens = [tokens[0]+tokens[1]] + tokens[2:]
        if tokens[2] in ["-", "+"]:
            tokens = tokens[:2] + [tokens[2]+tokens[-1]]
        if tokens[1] == "+":
            return str(float(tokens[0])+float(tokens[2]))
        elif tokens[1] == "-":
            return str(float(tokens[0])-float(tokens[2]))
        elif tokens[1] == "*":
            return str(float(tokens[0])*float(tokens[2]))
        else:
            return str(float(tokens[0])/float(tokens[2]))
        
        
if __name__=="__main__":
    calc = SimpleCalculator()
    print(calc.evaluate_expression("2+3"))