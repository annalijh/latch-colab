"""
Find Motifs using Meme Suite
"""

import subprocess
from pathlib import Path
from enum import Enum

from latch import large_task, workflow
from latch.types import LatchFile, LatchDir

class LibraryType(Enum):
    motif_lib_jaspar = "/root/reference/JASPAR_CORE_REDUNDANT_2016_vertebrates.meme"
    motif_lib_hocomoco = "/root/reference/HOCOMOCOv11_full_HUMAN_mono_meme_format.meme"

# MEME find motifs
@large_task
def run_ame_motif_task(
    bed_file: LatchFile,
    genome_fasta: str = "/root/reference/hg38.fa",
    library_type: LibraryType = LibraryType.motif_lib_jaspar,
) -> LatchDir:

    """
    Step 1: Extract DNA sequences from a fasta file based on feature coordinates.
    """
    output_fasta = Path("output_fasta.fa").resolve()

    _bedtools_make_fasta_cmd = [
        "bedtools",
        "getfasta",
        "-fi",
        genome_fasta,
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
        "--oc",
        str(output_directory),
        str(output_fasta),
        library_type.value,
    ]

    subprocess.run(_MEME_motif_cmd)

    return LatchDir(str(output_directory), "latch:///meme_analysis_output")


@workflow
def call_ame_workflow(bed: LatchFile, library_type: LibraryType = LibraryType.motif_lib_jaspar,) -> LatchDir:
    """MEME-Motif analyzes genomic positions for enriched motifs. 

    MEME-Motif
    ----

    Identifies known or user-provided motifs that are either relatively enriched in your sequences compared with control sequences, that are enriched in the first sequences in your input file, or that are enriched in sequences with small values of scores that you can specify with your input sequences

    ### Tools used
    - Robert McLeay and Timothy L. Bailey, "Motif Enrichment Analysis: A unified framework and method evaluation", BMC Bioinformatics, 11:165, 2010, doi:10.1186/1471-2105-11-165. [full text]
    - Aaron R. Quinlan, Ira M. Hall, BEDTools: a flexible suite of utilities for comparing genomic features, Bioinformatics, Volume 26, Issue 6, 15 March 2010, Pages 841–842, https://doi.org/10.1093/bioinformatics/btq033

    __metadata__:
        display_name: MEME Suite AME motif caller
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

        library_type:
          The known motif library to compare sequences against.

          __metadata__:
            display_name: Library Type

    """

    return run_ame_motif_task(
        bed_file=bed,
        genome_fasta="/root/reference/hg38.fa",
        motif_lib="/root/reference/motif.meme",
    )


