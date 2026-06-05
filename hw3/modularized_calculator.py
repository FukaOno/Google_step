#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index+1

def read_divide(line, index):
    token= {'type':'DIVIDE'}
    return token, index+1

def read_open_parenthesis(line, index):
    token = {'type':'OPEN_PARENTHESIS'}
    return token, index+1

def read_closed_parenthesis(line, index):
    token = {'type':'CLOSED_PARENTHESIS'}
    return token, index+1

def read_abs(line, index):
    token={'type':'ABS'}
    return token, index+1

def read_int(line, index):
    token={'type':'INT'}
    return token, index+1

def read_round(line, index):
    token={'type':'ROUND'}
    return token, index+1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index]=='*':
            (token, index) = read_multiply(line, index)
        elif line[index]=='/':
            (token, index) = read_divide(line, index)
        elif line[index]=='(':
            (token, index) = read_open_parenthesis(line, index)
        elif line[index]==')':
            (token, index) = read_closed_parenthesis(line, index)
        elif line[index:index+3]=='abs':
            (token, index) = read_abs(line, index+3)
        elif line[index:index+3]=='int':
            (token, index) = read_int(line, index+3)
        elif line[index:index+5]=='round':
            (token, index) = read_round(line, index+5)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_mult_n_divide_first(tokens):
    index =1 # starts with 1 so that there is always prev to check 
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS' or tokens[index - 1]['type'] == 'MINUS':
                index+=1
                continue
            elif tokens[index - 1]['type'] == 'MULTIPLY':
                
                # get two numbers
                num1=tokens[index-2]['number']
                num2=tokens[index]['number']

                # multiply
                ans = num1*num2

                # delete the numbers to multiply and symbol
                del tokens[index-2:index+1]

                # insert at the same position as the original mult symbol
                tokens.insert(index-2, {'type': 'NUMBER', 'number': ans})
                index-=1

            elif tokens[index - 1]['type'] == 'DIVIDE':

                num1=tokens[index-2]['number']
                num2=tokens[index]['number']

                ans = num1/num2

                # delete the numbers to divide and symbol
                del tokens[index-2:index+1]

                tokens.insert(index-2, {'type': 'NUMBER', 'number': ans})
                index-=1
               
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return tokens

def evaluate_p_first(tokens):
    index =0
    while index < len(tokens):

        # ERROR: no matching opne p found
        if tokens[index]['type'] == 'CLOSED_PARENTHESIS':
            print('Invalid syntax: no matching ( found')
            exit(1)

        # open parenthesis then init
        if tokens[index]['type'] == 'OPEN_PARENTHESIS':
            start=index
            stack=[]
            index+=1
                
            # if open again then we continue push
            # if closed 
            while True:
                if tokens[index]['type']=='OPEN_PARENTHESIS':
                    stack.append(tokens[index])
                elif tokens[index]['type']=='CLOSED_PARENTHESIS':

                    # if the stack is empty -> we pop every elements inside of stack
                    # we found the final closing p
                    if len(stack)==0:
                        break

                    # if we still have elements inside of stack-> its inner closed parenthesis
                    stack.pop()
                index+=1

                # ERROR : ran out of tokens without finding matching ')'
                if index >= len(tokens):
                    print('Invalid syntax: no matching ) found')
                    exit(1)
            
            # evaluate the equation in between of '(' and ')'
            ans=evaluate(tokens[start+1:index])

            # delete the original token from '(' to ')'
            del tokens[start:index+1]
                
            # insert to the original position 
            tokens.insert(start, {'type': 'NUMBER', 'number': ans})
            index = start

        index += 1
        
    return tokens

def evaluate_abs_int_round_first(tokens):
    index =0
    while index < len(tokens):
        if tokens[index]['type'] == 'ABS':
            # get the number
            num = tokens[index+1]['number']
            ans = abs(num)

            del tokens[index:index+2] # delete the original
            tokens.insert(index, {'type': 'NUMBER', 'number': ans})

        elif tokens[index]['type']=='INT':
            # get the number
            num = tokens[index+1]['number']
            ans = int(num)

            del tokens[index:index+2] # delete the original
            tokens.insert(index, {'type': 'NUMBER', 'number': ans})
        
        elif tokens[index]['type']=='ROUND':
            # get the number
            num = tokens[index+1]['number']
            ans = round(num)

            del tokens[index:index+2] # delete the original
            tokens.insert(index, {'type': 'NUMBER', 'number': ans})
        else:
            index+=1
    return tokens

         

# if mult and divide in this tokens-> call evaluate_mult_n_divide_first(tokens)
# looping -> costy
def has_mult_or_div(tokens):
    for token in tokens:
        if token['type'] in ('MULTIPLY', 'DIVIDE'):
            return True
    
    return False

def has_parenthesis(tokens):
    # if parenthesis in tokens
    for token in tokens:
        if token['type'] in ('OPEN_PARENTHESIS', 'CLOSED_PARENTHESIS'):
            return True
    return False

def has_abs_int_round(tokens):
    for token in tokens:
        if token['type'] in ('ABS', 'INT', 'ROUND'):
            return True
    return False


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1

    if has_parenthesis(tokens):
        tokens = evaluate_p_first(tokens)

    if has_abs_int_round(tokens):
        tokens=evaluate_abs_int_round_first(tokens)
    
    if has_mult_or_div(tokens):
        tokens=evaluate_mult_n_divide_first(tokens)

    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    print("==== Test multiply! ====")
    test("2*3")
    test("2.0*3+3")
    test("10.0*2")
    print("==== Test divide! ====")
    test("2/4")
    test("1.0/4")
    test("5.0/2.3")
    print("==== Test both multiply and divide! ====")
    test("2/4+2*3")
    test("1.0/4-0-2.0*3+3")
    test("5.0/2.3+2.5+10.0*2")
    print("==== Test parenthesis! ====")
    test("(5.0/2.3)")
    test("(3.0+1.0)*2")
    print("==== Test all! ====")
    test("2/(4+2)*3")
    test("1.0/4-0-(2.0*3+3)")
    test("5.0/(2.3+2.5)+10.0*2")
    test("(3.0+2") # Invalid: No closed
    test(")2.0+1") # Invalid: No Open
    test("((3.0+1.0)*2)") # Nested Parenthesis
    print("==== Test abs! ====")
    test("abs(1.0/4-0-(2.0*3+3))")
    print("==== Test int! ====")
    test("int(1.0/4-0-(2.0*3+3))")
    print("==== Test round! ====")
    test("round(1.0/4-0-(2.0*3+3))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)