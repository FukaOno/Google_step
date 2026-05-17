import os

def list_to_string(sorted_list):
    return "".join(sorted_list)

def binary_search(sorted_string, new_dict):
    l=0
    r=len(new_dict)-1

    while l<=r:
        mid = (l+r)//2
        mid_string = new_dict[mid][0]

        if sorted_string == mid_string:
            return new_dict[mid][1]
        elif sorted_string > mid_string:
            # too big-> move to left
            l=mid+1
        else:
            r=mid -1
    return None


def find_anagram(given_string, dict_file):
    sorted_word_list=sorted(given_string)
    sorted_string = list_to_string(sorted_word_list)

    with open(dict_file, 'r') as file:
        new_dict =[]
        for line in file:
            sorted_w_list = sorted(line.rstrip('\n'))
            sorted_s = list_to_string(sorted_w_list)
            new_dict.append((sorted_s, line.rstrip('\n'))) # anagram : word
        new_dict.sort()

        anagram = binary_search(sorted_string, new_dict)
        return anagram
    

            

dict_file = os.path.join(os.path.dirname(__file__), "words.txt")
given_string1="tpo" #opt
given_string2="a" #None
given_string3="" #None
given_string4= "gbetniasn" #absenting
print(find_anagram(given_string3, dict_file))



