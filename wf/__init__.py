"""
Find Motifs using Meme Suite
"""

import subprocess
from pathlib import Path

from latch import medium_task, workflow
from latch.types import LatchFile, LatchDir


# MEME find motifs
@medium_task
def run_motif_task(bed_file: LatchFile, genome_fasta: LatchFile, motif_lib: LatchFile) -> LatchDir:

    """
    Step 1: Extract DNA sequences from a fasta file based on feature coordinates.
    """
    output_fasta = Path("output_fasta.fa").resolve()

    _bedtools_make_fasta_cmd = [
        "bedtools",
        "getfasta",
        "-fi",
        genome_fasta.local_path,
        "-bed",
        bed_file.local_path,
        "-fo",
        str(output_fasta)
    ]

    subprocess.run(_bedtools_make_fasta_cmd)

    """
    Step 2: RUN meme-suite AME
        AME identifies known or user-provided motifs that are either relatively enriched in your sequences 
        compared with control sequences, that are enriched in the first sequences in your input file, 
        or that are enriched in sequences with small values of scores that you can specify with your input sequences
    """

    output_directory = Path("meme_analysis_output").resolve()

    _MEME_motif_cmd = [
        "ame",
        "--o",
        str(output_directory),
        genome_fasta.local_path,
        motif_lib.local_path,
    ]

    subprocess.run(_MEME_motif_cmd)

    return LatchDir(str(output_directory), "latch:///meme_analysis_output")


@workflow
def call_motifs(bed: LatchFile, genome: LatchFile, motif_lib: LatchFile) -> LatchDir:
    """MEME-Motif analyzes genomic positions for enriched motifs. 

    MEME-Motif
    ----

    Identifies known or user-provided motifs that are either relatively enriched in your sequences compared with control sequences, that are enriched in the first sequences in your input file, or that are enriched in sequences with small values of scores that you can specify with your input sequences

    __metadata__:
        display_name: MEME Suite: AME motif caller
        author:
            name: Stephen Lu
            email: stephen.lu@mail.mcgill.ca
            github: https://github.com/TheMatrixMaster
        repository: https://github.com/annalijh/latch-colab
        license:
            id: MIT

    Args:

        bed:
          input bed file to find enriched motifs

          __metadata__:
            display_name: bed

        genome:
          input genome file

          __metadata__:
            display_name: genome

        motif_lib:
          input motif library reference file

          __metadata__:
            display_name: library

        
    """

    return run_motif_task(
        bed=bed,
        genome_fasta=genome,
        motif_lib=motif_lib
    )


# Local Debugging
if __name__ == "__main__":
    bedFile = LatchFile("../data/")
    genomeFastaFile = LatchFile("../data/")
    motifLibFile = LatchFile("../data/")

    call_motifs(bed=bedFile, genome=genomeFastaFile, motif_lib=motifLibFile)
