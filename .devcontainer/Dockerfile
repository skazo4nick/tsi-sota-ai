FROM ubuntu:22.04

# Install Conda for Linux ARM64 (for Apple Silicon Macs)
RUN apt-get update && apt-get install -y wget bzip2 git
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O Miniconda3-installer.sh
RUN bash Miniconda3-installer.sh -b -p /opt/conda
ENV PATH="/opt/conda/bin:${PATH}"

# Initialize conda (Crucial step in Dockerfile)
RUN conda init bash

# Copy environment.yaml
COPY environment.yaml /tmp/environment.yaml

# [Optional] You can add other system-level dependencies here using apt-get install if needed for your project
# Example: RUN apt-get install -y some-system-package