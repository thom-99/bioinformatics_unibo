import pandas as pd
from collections import defaultdict
import numpy

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






inside_data = parsefasta('chr22_CpG.fa')
inside_model = dinucleofrequencies(inside_data)

outside_data = parsefasta('outside_sequences.fa')
outside_model = dinucleofrequencies(outside_data)

print(inside_model)
print()
print(outside_model)