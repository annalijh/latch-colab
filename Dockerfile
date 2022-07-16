FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main

# basics
RUN apt-get update && apt-get install -y apt-transport-https \
    && apt-get install -y wget cmake git github-backup pandoc

# generic bioinfo
RUN apt-get install -y bedtools samtools picard-tools

# Motif discovery
# MEME
RUN apt-get install libhtml-template-perl libxml-simple-perl libsoap-lite-perl imagemagick \
    && wget 'ftp://ftp.ebi.edu.au/pub/software/MEME/4.8.1/meme_4.8.1.tar.gz' \
    && tar xf meme_4.8.1.tar.gz \
    && rm meme_4.8.1.tar.gz \
    && cd meme_4.8.1 \
    && ./configure --enable-build-libxml2 --with-url=http://meme.nbcr.net/meme \
    && make -j 4 \
    && make test \
    && make install

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
RUN python3 -m pip install --upgrade latch
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
