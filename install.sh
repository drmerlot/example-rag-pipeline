#!/bin/bash

# Initialize Conda for bash
eval "$(conda shell.bash hook)"

# follow these steps one by one in a shell interpreter on an apple silicon system
conda create -n erp python==3.11

conda activate erp

# Insatll llama cpp python with mps support
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python==0.2.18 --no-cache-dir

# then install this example package
pip install '.[dev]'

# user has to activate conda in their shell at the end
echo "Installation successful! 🎉"
echo ""
echo " █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗"
echo "██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║"
echo "███████║██║        ██║   ██║██║   ██║██╔██╗ ██║"
echo "██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║"
echo "██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║"
echo "╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝"
echo ""
echo "Please copy and paste the following command before continuing:"
echo ""
echo "conda activate erp"
echo ""
echo "Thank you for installing! Hope it is helpful. 😊"

