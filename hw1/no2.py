import os

def get_score(anagram):
    score =0

    one =['a', 'e', 'h', 'i', 'n', 'o', 'r', 's', 't']
    two =['c', 'd', 'l', 'm', 'u']
    three = ['b', 'f', 'g', 'p', 'v', 'w', 'y']
    four =['j', 'k', 'q', 'x', 'z']

    for l in anagram:
        if l in one:
            score+=1
        elif l in two:
            score+=2
        elif l in three:
            score+=3
        elif l in four:
            score+=4
        else:
            print("Invalid letter")
    return score

# FIX: 
    # pre process the dictionary once 
    # sort with score
    # order : biggest-> smallest -> biggest score as a match

def build_dictionary_data(dict_file):
    dict=[]

    with open(dict_file, 'r') as file:
        for line in file:
            frequency_line=[0]*26
            # if the frequency count is smaller than its count of given_string-> anagram
            line_stripped = line.rstrip('\n')
            for j in range(len(line_stripped)):
                frequency_line[ord(line_stripped[j])-ord('a')]+=1
            
            score = get_score(line_stripped)
            dict.append(score, line_stripped, frequency_line)
    dict.sort(reverse=True)
    return dict


# dictに対して入っているstring をcount
def find_anagram_with_dictionary_counter(input_file, dict_file):

    dict=build_dictionary_data(dict_file)

    with open(input_file, 'r') as input:
        for input_line in input:

            frequency=[0]*26 
            input_word=input_line.rstrip('\n')

            # get the frequency of the word
            for l in input_word: 
                frequency[ord(l)-ord('a')]+=1
            max_anagram=""
            
            # traverse th score
            for score, line, frequency_line in dict:
                    is_valid=True
                    for i in range(26):
                        if frequency[i]<frequency_line[i]:
                            # remove this line
                            is_valid = False
                            break

                    # if its same or not used in given_string then its okay
                    if is_valid:
                        max_anagram = line
                        break
            with open("large_answer.txt", 'a') as file:
                    file.write(max_anagram+'\n')
    
    

small = os.path.join(os.path.dirname(__file__), "small.txt")
large = os.path.join(os.path.dirname(__file__), "large.txt")
dict_file = os.path.join(os.path.dirname(__file__), "words.txt")
print(find_anagram_with_dictionary_counter(large, dict_file))



