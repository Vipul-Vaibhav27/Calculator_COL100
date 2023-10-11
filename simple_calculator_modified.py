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
if __name__ == "__main__":
    calculator = SimpleCalculatorModified()
    exp = "-2.4/-3.4"
    print(calculator.evaluate_expression(exp))