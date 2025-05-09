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

def needle_wu(sequence1, sequence2, gap_penalty=-2, match=1, mismatch=-1, show=False):

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

#needle_wu('ACGT','ACGGT',show=True)


def align(sequenceA, sequenceB, Gap=-2, Match=1, Mismatch=-1):

    matrix = needle_wu(sequenceA, sequenceB, gap_penalty=Gap, match=Match, mismatch=Mismatch)

    #looping for every character in the longer sequence

    COLUMN = len(sequenceA)
    ROW = len(sequenceB)

    #initializing alignment list of lists with the last pair
    seqA = matrix.columns[COLUMN]
    seqB = matrix.index[ROW]

    for i in range(max(len(sequenceA), len(sequenceB))-1):

        #diagonal for match
        if seqA[-1]==seqB[-1]:
            if matrix.iloc[ROW, COLUMN] == matrix.iloc[ROW-1, COLUMN-1] + Match:
                ROW -= 1
                COLUMN -= 1
                seqA = seqA + matrix.columns[COLUMN]
                seqB = seqB + matrix.index[ROW]


        else:
            if matrix.iloc[ROW, COLUMN] == matrix.iloc[ROW-1, COLUMN-1] + Mismatch:
                ROW -= 1
                COLUMN -= 1
                seqA = seqA + matrix.columns[COLUMN]
                seqB = seqB + matrix.index[ROW]

            #from above
            if matrix.iloc[ROW, COLUMN] == matrix.iloc[ROW-1, COLUMN] + Gap:
                ROW -= 1
                seqA = seqA[:-1] + '-' + matrix.columns[COLUMN]
                seqB = seqB + matrix.index[ROW]
                
            #from left
            else:
                COLUMN-=1
                seqB = seqB[:-1] + '-' + matrix.index[ROW]
                seA = seqA + matrix.columns[ROW]

    print(f'seq1 : {seqA}')
    print(f'seq2 : {seqB}')

    return seqA, seqB

print(align('ACGT','ACGGT'))