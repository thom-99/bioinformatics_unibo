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

    pairs = structure(T)
    rotations = []

    for i in range(len(pairs)):
        
        rotated_pairs = pairs[i:] + pairs[:i]
        #adding the rotated pairs to the list
        rotations.append(rotated_pairs)

    return rotations

#test
#print(rotate('abaaba$'))
#out: ['abaaba$', 'baaba$a', 'aaba$ab', 'aba$aba', 'ba$abaa', 'a$abaab', '$abaaba']

def BWT(T:str, show=True):
    
    #computig all the rotations and sorting them
    sorted_rotations = sorted(rotate(T))
    
    F = []
    L = []

    for rotation in sorted_rotations:
        F.append(rotation[0]) #first char
        L.append(rotation[-1]) #last char
    
    #optional display
    if show==True:
        str_bwt = ''
        for pair in L:
            str_bwt += pair[0]
        print(str_bwt)

    return L, F 

#test
#BWT('abaaba$',show=True)
#printed: abba$aa


def rBWT(L:list, F:list):

    row = 0 #row starting with $
    rbwt = '$'

    for i in range(len(L)-1):
        
        last_char = L[row][0]
        rbwt = last_char + rbwt

        
        #finding the next row usint L and F
        target_pair = L[row]
        row = F.index(target_pair) #index of char in F 

    return rbwt

#test
#L, F = BWT('abaaba$',show=False)   
#print(L)
#print(F)     
#print(rBWT(L,F))

def match(P:str, L:list, F:list):
    '''
    matches the query string P to the original string T leveraging FM index properties
    returns the number of times P is found in T, if present at all. 
    '''

    #this goes from len(p)-1 to 0 (-1 excluded), last -1 means backwards
    for i in range(len(P)-1, -1, -1):
        

        
        for pair in F:
            if pair[0]==P[i]:


