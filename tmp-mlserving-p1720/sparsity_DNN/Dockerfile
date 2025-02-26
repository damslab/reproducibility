FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Avoid interactive prompts during package installation
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    lsb-release \
    wget \
    git \
    m4 \
    patch \
    gcc \
    g++ \
    cmake \
    python3.9 \
    python3-pip \
    python-is-python3 \
    tzdata \
    sudo \
    libpq-dev \
    libclang-dev \
    nano \
    unzip \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY src/. /app
COPY requirements.txt /app
COPY Dockerfile /app

WORKDIR /app

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

RUN pip3 install flatbuffers packaging protobuf sympy 
RUN pip3 install onnxruntime-gpu --index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-11/pypi/simple/
RUN pip3 install onnxruntime-tools 
RUN pip3 install onnxoptimizer

WORKDIR /app