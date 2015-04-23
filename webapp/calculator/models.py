class CalculatorException(Exception):
    pass

'''
Determine whether the number is on left or right side of the evaluation.
In the case of %, different calculation is done based on the location
of the operator. Create a binary tree?

Evaluate * and / as it hits.
Evaluate down when hit )
'''
import operator

class Calculator(object):

    operations = {
        '+': operator.add,
        '-': operator.sub,
        'x': operator.mul,
        '/': operator.div,
    }

    @classmethod
    def reduce(cls, tokens):
#         print 'tokens', tokens
        if tokens[-2] == '(':
            if len(tokens) > 2:
                if isinstance(tokens[-3], float):
                    tokens[-2] = 'x'
                else:
                    tokens.pop(-2)
            else:
                tokens.pop(0)
        else:
            b, func, a = tokens.pop(), cls.operations[tokens.pop()], tokens.pop()
            tokens.append(func(a, b))

    @classmethod
    def append_number(cls, tokens, number):
        if not number:
            return

        if len(tokens) > 2 and tokens[-1] == '-' and not isinstance(tokens[-2], float):
            tokens.pop()
            tokens.append(float(number) * -1)
        else:
            tokens.append(float(number))

    @classmethod
    def has_left(cls, tokens):
        return len(tokens) > 2 and isinstance(tokens[-2], float)

    @classmethod
    def evaluate(cls, expression):
        if not expression:
            return 0

        tokens = []
        operators = ['+', '-', 'x', '/', '(', ')', '%']
        number = ''
        open_paren = False
        for char in expression:
            if char == ' ':
                # Skip spaces
                continue

            if char in operators:
                cls.append_number(tokens, number)
                number = ''

                if char == '%':
                    if len(tokens) > 2 and tokens[-2] in ['+', '-']:
                        tokens[-1] *= tokens[-3] * .01
                    else:
                        tokens[-1] *= .01
#                     print 'apply percent', tokens
                    continue

                if len(tokens) > 2 and tokens[-2] in ['x', '/']:
                    cls.reduce(tokens)

                if char == ')':
                    open_paren = False
#                     print 'right parenthese reduce'
                    cls.reduce(tokens)
                else:
                    if char == '(':
                        open_paren = True
                    tokens.append(char)
            elif char.isdigit() or char == '.':
                if tokens and isinstance(tokens[-1], float):
                    tokens.append('x')
                number += char
            else:
                raise CalculatorException('Invalid character: {}'.format(char))

        if open_paren:
            raise CalculatorException('Unequal parantheses')

        cls.append_number(tokens, number)
        while len(tokens) > 1:
            cls.reduce(tokens)

        return tokens[0]
