#!/bin/bash

# usage 
if [ "$#" -ne 2 ]; then
	echo "usage: $0 <bed-like file> <input.fasta file>"
	echo "the output will be the CpG regions in chr22"
	exit 1
fi 

INPUT_BED=$1
INPUT_FA=$2

awk '$1 == "chr22"' "$INPUT_BED" | awk '{print $1"\t"$2"\t"$3}' > chr22_CpG.bed

seqkit subseq --bed chr22_CpG.bed "$INPUT_FA" > chr22_CpG.fa


# === produce a file with outside genomic regions === 

CHR_LEN=$(samtools faidx "$INPUT_FA" && awk '{print $2}' "${INPUT_FA}.fai")

awk -v len="$CHR_LEN" 'BEGIN{srand()} {
    island_len = $3 - $2
    start = int(rand() * (len - island_len))
    print "chr22\t" start "\t" start + island_len "\toutside_" NR
}' chr22_CpG.bed > outside_regions.bed

seqkit subseq --bed outside_regions.bed "$INPUT_FA" > outside_sequences.fa
