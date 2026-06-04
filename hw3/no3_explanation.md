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

## Compute the equation first-> put into tokens again

    # go through and if open parenthesis-> go through until we find close
    # then compute the in-between of parenthesis with 'evaluate()'

        
    def evaluate_p_first(tokens):
        index =1 # starts with 1 so that there is always prev to check 
        while index < len(tokens):

            # start of equation to do first
            if tokens[index]['type'] == 'OPEN_PARENTHESIS':
                start=index

                # until we find closed parenthesis-> move index
                while tokens[index]['type']!='CLOSED_PARENTHESIS':
                    index+=1
                
                # evaluate the equation in between of '(' and ')'
                ans=evaluate(tokens[start+1:index])

                # delete the original token from '(' to ')'
                del tokens[start:index+1]
                
                # insert to the original position 
                tokens.insert(start, {'type': 'NUMBER', 'number': ans})
                index = start
            
            index += 1
        return tokens
                
## TODO: Raise error when no matching parenthesis
## Nested parenthesis

                    

