# Add abs(), int(), round()

## STEP 1 Add readers
    def read_abs(line, index):
        token={'type':'ABS'}
        return token, index+1

    def read_int(line, index):
        token={'token':'INT'}
        return token, index+1

    def read_round(line, index):
        token={'token':'ROUND'}
        return token, index+1


## STEP 2 Add caller in tokenize()
    elif line[index:index+3]=='abs':
            (token, index) = read_abs(line, index+3)
    elif line[index:index+3]=='int':
            (token, index) = read_int(line, index+3)
    elif line[index:index+5]=='round':
            (token, index) = read_round(line, index+5)

## STEP 3 Identify if () in the tokens

    def has_abs_int_round(tokens):
        for token in tokens:
            if token['type'] in ('ABS', 'INT', 'ROUND'):
                return True
        return False

## STEP 4 Add symbol evaluator in evaluate()
    # call has_abs_int_round(tokens)

    if has_abs_int_round(tokens):
        tokens=evaluate_abs_int_round_first(tokens)

## STEP 5  Compute the equation first-> put into tokens again

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