import pandas as pd 

def initialize_matrix(seqA,seqB,penalty=-2):
    seqA = ['-'] + list(seqA)
    seqB = ['-'] + list(seqB)

    matrix = pd.DataFrame(columns=seqA, index=seqB)

    #adding the first 0 and the first row and columns 
    matrix.iloc[0,0] = 0
    for i in range(1, len(seqA)):
        matrix.iloc[0,i]=i*penalty
    for i in range (1, len(seqB)):
        matrix.iloc[i,0]=i*penalty
    
    return matrix

#takes as arguments the two sequences, the gap penalty, the match and mismatch points
#by setting show=True you can visualize each step

def needle_wu(sequence1, sequence2, gap_penalty=-2, match=1, mismatch=-1, show=True):

    matrix = initialize_matrix(sequence1,sequence2, penalty=gap_penalty)

    for i in range(1,len(matrix.index)):
        for j in range(1,len(matrix.columns)):

            if matrix.columns[j]==matrix.index[i]:
                value = match
            else:
                value = mismatch

            down = matrix.iloc[i-1,j] + gap_penalty
            right = matrix.iloc[i,j-1] + gap_penalty
            diagonal = matrix.iloc[i-1, j-1] + value 

            matrix.iloc[i,j] = max(down, right, diagonal)

            if show==True:
                print(matrix)

    return matrix

needle_wu('ACGT','ACGGT',show=True)