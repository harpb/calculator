import operator

class CalculatorException(Exception):
    pass

class Calculator(object):

    operations = {
        '+': operator.add,
        '-': operator.sub,
        'x': operator.mul,
        '/': operator.div,
        '(': None,
        ')': None,
        '%': None,
    }

    lower_orders = ['+', '-']
    higher_orders = ['x', '/']

    @classmethod
    def append_number(cls, tokens, number):
        '''
        Append number to tokens list.
        '''
        if not number:
            return

        tokens.append(float(number))

        if len(tokens) >= 2 \
                and tokens[-2] in cls.lower_orders\
                and not cls.has_left_number(tokens):
            # Apply the sign to the number
            # ['-', 2], 2 => [-2]
            # ['(', '+', 2] => ['(', 2]
            # ['(', '-', 2] => ['(', -2]
            # [5, '+', '-', 2]=> [5, '+', -2]
            # [5, '-', 5] does not changes
            if tokens[-2] == '-':
                tokens[-1] *= -1
            tokens.pop(-2)


    @classmethod
    def reduce(cls, tokens):
        '''
        Minimum of 2 items in tokens.
        Given a list with tokens, performs the operation at the 2nd to last
        position between the numbers at 1st and 3rd to last position.
        Reduces open paratheses down to a multiply operation.
        '''
        if not isinstance(tokens[-1], float):
            raise CalculatorException('Missing number at this position')

        if tokens[-2] == '(':
            if len(tokens) > 2:
                if isinstance(tokens[-3], float):
                    # Replace open parathese with a multiply operation
                    tokens[-2] = 'x'
                else:
                    # Otherwise, remove the open paranthese
                    tokens.pop(-2)
            else:
                # Remove the open paranthese
                # ['('] => []
                # ['(', '('] => ['(']
                # ['-', '('] => ['-']
                tokens.pop(0)
        else:
            if len(tokens) == 2:
                # If there are only 2 tokens, then operation is performed with 0
                # ['*', 1] => [0, '*', 1]
                tokens.insert(0, 0)

            b, func, a = tokens.pop(), cls.operations[tokens.pop()], tokens.pop()
            try:
                tokens.append(func(a, b))
            except ZeroDivisionError, e:
                raise CalculatorException(e.message)

    @classmethod
    def has_left_number(cls, tokens):
        '''
        Minimum of 3 items in tokens and the 3rd from the end item is a number.
        Valid:
            [1, '+', 1]
            [2, '+', 1, 'x', 1]
        '''
        return len(tokens) >= 3 and isinstance(tokens[-3], float)

    @classmethod
    def evaluate(cls, expression):
        if not expression:
            return 0

        tokens = []
        number = ''
        open_paren = 0  # Number of open paratheses

        for char in expression:
            if char == ' ':
                # Skip spaces
                continue

            if char in cls.operations.keys():
                cls.append_number(tokens, number)
                number = ''

                if char == '%':
                    # Evaluate percentage of the number
                    if not tokens or not isinstance(tokens[-1], float):
                        raise CalculatorException('Expected a number prior to percentage sign')

                    if cls.has_left_number(tokens) and tokens[-2] in cls.lower_orders:
                        # Evaluate percentage of the left number
                        tokens[-1] *= tokens[-3] * .01
                    else:
                        tokens[-1] *= .01

                    continue

                if cls.has_left_number(tokens) and tokens[-2] in cls.higher_orders:
                    cls.reduce(tokens)

                if char == ')':
                    if not open_paren:
                        raise CalculatorException('Unequal parantheses')
                    open_paren -= 1
#                     print 'right parenthese reduce'
                    cls.reduce(tokens)
                else:
                    if char == '(':
                        open_paren += 1
                    tokens.append(char)
            elif char.isdigit() or char == '.':
                if tokens and isinstance(tokens[-1], float):
                    # Assume multiplication, if the last token is a number
                    # (5)9 => 5 * 9, 5(9) => 5 * 9
                    # [5] => [5, 'x']
                    tokens.append('x')
                number += char
            else:
                raise CalculatorException('Invalid character: {}'.format(char))

        if open_paren:
            raise CalculatorException('Unequal parantheses')

        # Append the remaining number
        cls.append_number(tokens, number)

        # Apply operations
        while len(tokens) > 1:
            cls.reduce(tokens)

        if not isinstance(tokens[0], float):
            raise CalculatorException('{} does not evaluates to a number'.format(expression))

        # Result is placed in the tokens list
        return tokens.pop()
