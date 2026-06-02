## Modify the program and support ()

# STEP 1 Add parenthesis reader
    def read_parenthesis(line, index):
        token = {'type':'PARENTHESIS'}
        return token, index+1

## STEP 2 Add caller in tokenize()

## STEP 3 Add symbol evaluator in evaluate()

# STEP 4 Identify if () in the tokens
    # traverse the tokens

    def has_parenthesis(tokens):
    # if parenthesis in tokens
    for token in tokens:
        if token['type'] in ('PARENTHESIS'):
            return True
    return False

# Compute the equation first-> put into tokens again

    # go through and if open parenthesis-> until we find close, then compute the in-between

        
    def evaluate_p_first(tokens):
        index =1 # starts with 1 so that there is always prev to check 
        while index < len(tokens):
            if tokens[index]['type'] == 'OPEN_PARENTHESIS':
                start=index
                while tokens[index]['type']!='CLOSED_PARENTHESIS':
                    index+=1
                
                ans=evaluate(tokens[start+1:index])
                del tokens[start:index+1] # delete the original token from '(' to ')'
                tokens.insert(start, {'type': 'NUMBER', 'number': ans})
                index = start
            
            index += 1
        return tokens
                
# TODO: Raise error when no matching parenthesis
# Nested parenthesis

                    

