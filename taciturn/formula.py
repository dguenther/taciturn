'''
Definition
----------
Supported formulas are:
<operand> <operator> <operand>
<operand>

* Operands can be either unit attributes or numbers.
* Unit attributes are defined in the Unit class's get_attributes method.
* Unit attributes are not case sensitive.

Here are a few examples:
50 / Speed
3
'''
import operator

class Formula:
    def __init__(self):
        self.formula = ''
        
    def __init__(self, formula):
        self.formula = formula
        
    def evaluate(self, unit):
        tokens = formula.split()
        token_count = len(tokens)
        if (token_count == 1):
            result = parse_operand(tokens[0], unit)
        elif (token_count == 3):
            value1 = parse_operand(tokens[0])
            value2 = parse_operand(tokens[2])
            operator = tokens[1]
            result = do_math(value1, operator, value2)
        else:
            raise Exception('Invalid formula: \'%s\'' % (self.formula))
        return result
        
        
    def parse_operand(self, operand, unit):
        try:
            # see if the operand is a number
            value = float(operand)
            return value
        except ValueError:
            # if it's not a number, see if it's a unit attribute
            normalized_operand = operand.lower()
            attributes = unit.get_attributes()
            if normalized_operand in attributes:
                return attributes[normalized_operand]
            else: 
                raise Exception('Operand \'%s\' isn\'t in Unit.' % (operand))
        return None
        
    def do_math(self, operand1, operator, operand2):
        operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.div
        }
        return operations[operator](operand1, operand2)
    