import itertools

def overlap_and_merge(s1,s2):

    overlap = 0
    for i in range(1, min(len(s1), len(s2))+1):
        #checking suffix of s1 and prefix of s2
        if s1[-i:]==s2[:i]:
            overlap = i

    if overlap==0:
        #if there is no overlap concatenate s1 and s2
        s3 = s1 + s2 
    else:
        #else concatenate s1 + the unique portion of s2, from the end of the overlap to the end of the string
        s3 = s1 + s2[overlap:]

    return s3 

#print(over_and_merge('abrac','acadabra'))


def superstring(l:list):
    
    permutations = list(itertools.permutations(l))  #list of tuples containing all the possible combinations

    current_superstring = None
    min_length = float('inf')

    for set in permutations:
        superstring = set[0]
        #each time the superstring is the result of the merge of two strigs, for every element in the set
        for i in range(1, len(set)):
            superstring = overlap_and_merge(superstring,set[i])

        #storing the superstring 
        if len(superstring) < min_length:
            min_length = len(superstring)
            current_superstring = superstring

    return current_superstring


strings = ['abr','raca','racadabra','abracada']

print(superstring(strings))
