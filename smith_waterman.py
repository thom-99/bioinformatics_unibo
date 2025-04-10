import pandas as pd 

def initialize_matrix(seqA,seqB,penalty=-2):
    seqA = ['-'] + list(seqA)
    seqB = ['-'] + list(seqB)

    matrix = pd.DataFrame(columns=seqA, index=seqB)

    # Set first row and first column to zero
    matrix.iloc[0, :] = 0  # First row
    matrix.iloc[:, 0] = 0  # First column
    
    return matrix


#takes as arguments the two sequences, the gap penalty, the match and mismatch points
#by setting show=True you can visualize each step

def smith_waterman(sequence1, sequence2, gap_penalty=-2, match=1, mismatch=-1, show=False):

    matrix = initialize_matrix(sequence1,sequence2, penalty=gap_penalty)

    max_value = 0
    max_coord = (0,0)

    for i in range(1,len(matrix.index)):
        for j in range(1,len(matrix.columns)):

            if matrix.columns[j]==matrix.index[i]:
                value = match
            else:
                value = mismatch

            down = matrix.iloc[i-1,j] + gap_penalty
            right = matrix.iloc[i,j-1] + gap_penalty
            diagonal = matrix.iloc[i-1, j-1] + value 

            matrix.iloc[i,j] = max(down, right, diagonal, 0)   

            #check if the values is a maximum in the matrix 
            if matrix.iloc[i,j] > max_value:
                max_value = matrix.iloc[i,j]
                max_coord = (i,j)
            
            if show==True:
                print(matrix)

    return matrix, max_coord


#smith_waterman('ATTC','GTTA',show=True)

def sw_align(sequenceA, sequenceB, Gap=-2, Match=1, Mismatch=-1):

    matrix, start_coord = smith_waterman(sequenceA, sequenceB, gap_penalty=Gap, match=Match, mismatch=Mismatch)
    
    #unpacking - the matrix[i,j] is the starting position
    i, j = start_coord

    seqA = matrix.columns[j]
    seqB = matrix.index[i]

    while i>=0 and j>=0 and matrix.iloc[i,j] > 0:

        diag = matrix.iloc[i-1,j-1]
        up = matrix.iloc[i-1, j]
        left = matrix.iloc[i,j-1]

        max_val = max(diag, up, left)

        if max_val<=0:
            break

        if diag==max_val:
            i -= 1
            j -= 1
            seqA = matrix.columns[j] + seqA
            seqB = matrix.index[i] + seqB

        elif up==max_val:
            i -= 1
            seqA = '-' + seqA
            seqB = matrix.index[i] + seqB 

        else:
            j -= 1
            seqA = matrix.columns[j] + seqA
            seqB = '-' + seqB

    print(seqA)
    print()
    print(seqB)

    return seqA, seqB
            
    

sw_align('ATTC','ATTGCG')
    

