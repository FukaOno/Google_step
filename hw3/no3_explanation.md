## Modify the program and support ()

## STEP 1 Add parenthesis reader
    def read_parenthesis(line, index):
        token = {'type':'PARENTHESIS'}
        return token, index+1

## STEP 2 Add caller in tokenize()
    elif line[index]=='(':
            (token, index) = read_open_parenthesis(line, index)
    elif line[index]==')':
            (token, index) = read_closed_parenthesis(line, index)

   
## STEP 3 Add symbol evaluator in evaluate()
    if has_parenthesis(tokens):
        tokens = evaluate_p_first(tokens)

## STEP 4 Identify if () in the tokens

    def has_parenthesis(tokens):
        for token in tokens:

            # if parenthesis in tokens
            if token['type'] in ('PARENTHESIS'):
                return True
        return False

## STEP 5 Compute the equation first-> put into tokens again

    # go through and if open parenthesis-> go through until we find close
    # push the equation into the stack
    # once we found the closed parenthesis -> pop from stack
    # then compute the in-between of parenthesis with 'evaluate()'

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