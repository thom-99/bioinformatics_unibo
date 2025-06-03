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

                

def match(P: str, L: list, F: list):
    
    top_row = 0
    bottom_row = len(F)-1

    # process each character from last to first
    for i in range(len(P)-1, -1, -1):
        char = P[i]
        new_top = None
        new_bottom = None

        #search the current char in F
        for j in range(top_row, bottom_row+1):
            if F[j][0]==char:
                if new_top==None:
                    new_top=j
                new_bottom=j
        
        #if no character is found, that means 0 matches 
        if new_top==None:
            return 0

        #update top and bottom row for the current character
        top_row=new_top
        bottom_row=new_bottom

        #LF mappinig part
        if i > 0: #do not perform LF mapping on the last iteration
            next_char = P[i-1]
            lf_top = None
            lf_bottom = None

            for j in range(top_row, bottom_row+1):
                if L[j][0]==next_char:
                    l_pair = L[j]
                    f_pair_index = F.index(l_pair) #finds where the l_pair tuple appears on F column

                    if lf_top==None:  #this occurs only on the first iteration
                        lf_top = f_pair_index
                        lf_bottom = f_pair_index
                    else:
                        #this occurs on every other iteration : building a range
                        lf_top = min(lf_top, f_pair_index)
                        lf_bottom = max(lf_bottom, f_pair_index)
            
            if lf_top==None:
                return 0

            top_row = lf_top
            bottom_row = lf_bottom
    
    #adding a 1 because I am counting a count of elements, not a distance
    return bottom_row - top_row +1 


P = ('hope','string2','KKK')

L, F = BWT('ACTGTAstring2CTTGhopeGGACGTACTGATstring2GGTAC$',show=False)
print(L)
print(F)
for p in P:
    print(match(p,L,F))
