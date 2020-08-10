#!/bin/bash

# Activate desired Python environment to run Jupyter.
#####################################################
# For example:
# [A] with conda (environment activation is based on https://github.com/conda/conda/issues/7980)
eval "$(conda shell.bash hook)"
conda activate jupyter-env

# [B] with standard venv/virtualenv
# source path/to/venv/bin/activate

# Launch Jupyter.
#################
# Use predefined security token?
# export JUPYTER_TOKEN="t"
jupyter notebook

# Sleep a bit to allow capturing of error messages if launching Jupyter failed.
sleep 3