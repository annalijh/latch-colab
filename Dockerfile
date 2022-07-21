FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main
MAINTAINER "Stephen Lu"

# Update env
RUN apt-get update -y

# Add UNIX tools
RUN apt-get install -y gcc g++ make perl zip unzip gzip wget curl

# Get miniconda and set path
RUN curl -O \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/root/miniconda3/bin:$PATH"
ARG PATH="/root/miniconda3/bin:$PATH"

# testing conda installation
RUN conda update conda
RUN conda install python=3.7.6
RUN conda --version && conda clean --all --yes

# memesuite
RUN conda install -c bioconda meme

# bedtools
RUN conda install -c bioconda bedtools

# handle local files
COPY data/hg38.fa /root/reference/hg38.fa
COPY data/motif.meme /root/reference/motif.meme

COPY wf /root/wf

# Download hg38.fa file from source
# RUN wget -P /root/reference http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
# RUN gzip -d /root/reference/hg38.fa.gz

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
