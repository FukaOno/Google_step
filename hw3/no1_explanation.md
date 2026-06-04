# Modify the program and support '*' and '/'.

## STEP 1 Add following two methods to identify the symbol

def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index+1

def read_divide(line, index):
    token= {'type':'DIVIDE'}
    return token, index+1

## STEP 2 Add caller in tokenize()
    elif line[index]=='*':
            (token, index) = read_multiply(line, index)
    elif line[index]=='/':
            (token, index) = read_divide(line, index)


## STEP 3 Add symbol evaluator in evaluate()
    if has_mult_or_div(tokens):
        tokens=evaluate_mult_n_divide_first(tokens)


## STEP 4 Structure to perform '*' and '/' first
    evaluate() is the method that traverse the dict of number and type and perform last computation.
    -> if we already know that there is mult and divide, we perform them first and put into dict
    -> go through the dict and find mult and divide-> return computed dict

    def evaluate_mult_n_divide_first(tokens):
        index =1 # starts with 1 so that there is always prev to check 
        while index < len(tokens):
            if tokens[index]['type'] == 'NUMBER':
                if tokens[index - 1]['type'] == 'PLUS' or tokens[index - 1]['type'] == 'MINUS':
                    # if the type is minus or plus -> skip
                    index+=1
                    continue
                elif tokens[index - 1]['type'] == 'MULTIPLY':

                    # get the numbers to multiply
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
                # same for divide
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


    -> call this method if we know that mult is used 

## STEP 5 Identify whether mult and divide in tokens
    # add has_mul_or_div(tokens)
    # call in evaluate()
    # if mult and divide in this tokens-> call evaluate_mult_n_divide_first(tokens)

       def has_mult_or_div(tokens):
        for token in tokens:

            # if token is multiply or divide -> we found
            if token['type'] in ('MULTIPLY', 'DIVIDE'):
                return True
        
        return False


