'''
functions for computing 
the BWT(T) from a string T;
the string T from BWT(T);
...
'''


def structure(T:str):
    
    #dictionary containing charcter:count pairs
    char_counts = {}
    #list of tuples, which are character in T coupled with its occurrence in T
    pairs = []

    for character in T:
        occurrence = char_counts.get(character,0) # get 0 if the character is not present in the dict
        pairs.append((character,occurrence))
        char_counts[character] = occurrence + 1 #increment by 1 the count

    return pairs

#test
#print(structure('abaaba$'))
#out: [('a', 0), ('b', 0), ('a', 1), ('a', 2), ('b', 1), ('a', 3), ('$', 0)]

def rotate(T:str):

    rotations = []

    for i in range(len(T)):
        #creating rotated string
        S = T[i:] + T[:i]
        #adding the rotated string to the list
        rotations.append(S)

    return rotations

#test
#print(rotate('abaaba$'))
#out: ['abaaba$', 'baaba$a', 'aaba$ab', 'aba$aba', 'ba$abaa', 'a$abaab', '$abaaba']

def BWT(T:str, show=False):
    
    #computig all the rotations and sorting them
    sorted_rotations = sorted(rotate(T))
    
    bwt = []

    for rotation in sorted_rotations:
        last_char = structure(rotation)[-1]
        bwt.append(last_char)
    
    #optional display
    if show==True:
        str_bwt = ''
        for pair in bwt:
            str_bwt += pair[0]
        print(str_bwt)

    return bwt

#test
#BWT('abaaba$',show=True)
#printed: abba$aa

