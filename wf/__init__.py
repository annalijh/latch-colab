"""
Find Motifs ...
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile, LatchDir


#make the fasta file
@small_task
def fasta_convert_task(bed: LatchFile, genome: LatchFile) -> LatchFile:
    #reference to the output
    fasta_file = Path("output_fasta.fa").resolve()
    
    _bedtools_makefasta_cmd = [
    "bedtools",
    "getfasta",
    "-fi",
    genome.local_path,
    "-bed",
    bed.local_path,
    "-fo",
    str(fasta_file)
    ]

    subprocess.run(_bedtools_makefasta_cmd)

    return LatchFile(str(fasta_file), "latch:///output_fasta.fa")

#MEME find motifs
@small_task
def MEME_motif_task(fasta: LatchFile,motif_lib: LatchFile) -> LatchDir:
    #output
    motif_directory = Path("MEME_motif_output").resolve()

    _MEME_motif_cmd = [
    "ame",
    "--o",
    str(motif_directory),
    fasta.local_path,
    motif_lib.local_path,
    ]

    subprocess.run(_MEME_motif_cmd)

    return LatchDir(str(motif_directory), "latch:///MEME_motif_output")


@workflow
def call_motifs(bed: LatchFile,genome: Latchfile, motif_lib: Latchfile) -> LatchDir:
    """MEME-Motif analyzes genomic positions for enriched motifs. 

    MEME-Motif
    ----

    identifies known or user-provided motifs that are either relatively enriched in your sequences compared with control sequences, that are enriched in the first sequences in your input file, or that are enriched in sequences with small values of scores that you can specify with your input sequences

    __metadata__:
        display_name: MEME Suite: AME motif caller
        author: annalijh
            name:
            email:
            github:
        repository:
        license:
            id: 

    Args:

        bed:
          input bed file to find enriched motifs

          __metadata__:
            display_name: bed
	
	genome:
	  input genome file
          __metadata__:
            display_name: genome

        motif library:
          input motif library reference file:

          __metadata__:
            display_name: library

        
    """
    
    fasta = fasta_convert_task(bed=bed,genome=genome)
    return MEME_motif_task(fasta = fasta,motif_lib=motif_lib)



