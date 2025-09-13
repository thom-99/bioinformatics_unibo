import pandas as pd
from collections import defaultdict
import math

def parsefasta(filename:str):
    sequences = []
    current_sequence = ''

    with open(filename, 'r') as fastafile:
        for line in fastafile:
            line = line.strip()
            if line.startswith('>'):
                if current_sequence != '':
                    sequences.append(current_sequence.upper())
                    current_sequence = ''
            else:
                current_sequence += line
        if current_sequence!='':
            sequences.append(current_sequence.upper())
    
    return sequences

def dinucleofrequencies(sequences):
    
    dinucleo_counts = defaultdict(int)
    first_nucleo_counts = defaultdict(int)
    nucletides = ['A', 'C', 'G', 'T']

    for seq in sequences:
        for i in range(len(seq)-1):
            first_nucleo = seq[i]
            second_nucleo = seq[i+1]

            #if they are valid nucleotides, add the counts to the dict
            if first_nucleo in nucletides and second_nucleo in nucletides:
                dinucleo = first_nucleo + second_nucleo
                dinucleo_counts[dinucleo] += 1
                first_nucleo_counts[first_nucleo] += 1

    #additional step : making it into a dataframe

    matrix = []

    for prev_nuc in nucletides:
        current_row = []
        total_prev = first_nucleo_counts[prev_nuc]

        for next_nuc in nucletides:
            dinucleotide = prev_nuc + next_nuc
            count = dinucleo_counts[dinucleotide]

            if total_prev > 0:
                P = count / total_prev
                current_row.append(round(P, 2))
            else:
                current_row.append(0.0)
    
        matrix.append(current_row)

    df = pd.DataFrame(matrix, index=nucletides, columns=nucletides)
    return df 


def computeProb(sequence:str, model:pd.DataFrame):
    sequence = sequence.upper()
    sequence = sequence.strip()
    P = 0.25 
    for i in range(1,len(sequence)):
        conditional_p = model.loc[sequence[i-1], sequence[i]]
        P = P*conditional_p
    
    return P 

def isCpG(P_inside:float, P_outside:float):
    log_ratio = math.log(P_inside/P_outside)
    if log_ratio>0:
        print(f'log ratio : {log_ratio}, likely part of a CpG island')
    else:
        print(f'log ratio : {log_ratio}, likely NOT part of a CpG island')

    return log_ratio


# EXECUTION

inside_data = parsefasta('chr22_CpG.fa')
inside_model = dinucleofrequencies(inside_data)

outside_data = parsefasta('outside_sequences.fa')
outside_model = dinucleofrequencies(outside_data)

#print(inside_model)
#print()
#print(outside_model)


CpGseq = "gccttgagatacccctagcggtccagaggcgcaccctggtttcgagccagggacgctagggtctctggggcccagtgtagggctgatgggtagggacgttggtccgtgggggacccaggcgccacttctgggcgccgcagttttttattttttttctctgccccaggtgtctcacctttc"

P_inside = computeProb(CpGseq, inside_model)
P_outside = computeProb(CpGseq, outside_model)
isCpG(P_inside, P_outside)

# output : log ratio : 5.277031975772654, likely part of a CpG island

outside_seq = "CATGTCTCTTTATGAATGCCTGCAGACCCAGACCTAGGTGATGATGCCCCCACTCACCTACCCCCAAAATTAATTTAAAGCAATAGCTTCTCATTGGATGGTTGTAATGACCAACATTTAGCTCTTGGGTCTTCTGTTGGCCAGTTAATTTGGTAGTCATTTGCTTCTCATGGTCAGGAA"

P_inside2 = computeProb(outside_seq, inside_model)
P_outside2 = computeProb(outside_seq, outside_model)
isCpG(P_inside2, P_outside2)

# output : log ratio : -26.39676965080549, likely NOT part of a CpG islan