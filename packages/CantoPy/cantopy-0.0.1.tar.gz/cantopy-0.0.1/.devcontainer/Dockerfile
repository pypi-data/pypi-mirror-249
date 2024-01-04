FROM python:3.12-slim

# Configure new user
ARG USERNAME=robbe
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt /tmp/pip-tmp/
RUN pip install --upgrade pip \
    && pip install --requirement /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Set bash as the shell env
ENV SHELL=/bin/bash

# Update the pythonpath to always point to the base cantopy package
ENV PYTHONPATH "${PYTHONPATH}:/workspaces/CantoPy/cantopy"

# Set the default user
USER $USERNAME



