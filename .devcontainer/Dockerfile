FROM ubuntu:22.04

# Install Conda
RUN apt-get update && apt-get install -y wget bzip2
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda3-installer.sh
RUN bash Miniconda3-installer.sh -b -p /opt/conda
ENV PATH="/opt/conda/bin:${PATH}"

# Install Python (if needed, but base image might already have it, Conda will manage Python versions)
# RUN conda install -y python=3.11.8 # Conda will handle Python version

# Copy environment.txt (make sure it's in the same .devcontainer folder)
COPY environment.txt /tmp/environment.txt

# Create and activate Conda environment (moved to postCreateCommand in devcontainer.json)
# RUN conda env create -f /tmp/environment.txt
# RUN conda activate base

# [Optional] You can add other system-level dependencies here using apt-get install if needed for your project
# Example: RUN apt-get install -y some-system-package