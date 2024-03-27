# Example Rag Service
Example rag service for demo purposes

### Requires
conda, pip, macos m series machine (this is made to run locally for the demo)

### Get model file from
https://huggingface.co/TheBloke/Llama-2-13B-GGUF/blob/main/llama-2-13b.Q4_0.gguf

put the file in the home project dir under a new dir "assets"

### Install
conda create -n erp python==3.11

conda activate erp

Install llama cpp python with mps support
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python==0.2.18 --no-cache-dir

then install this example package
pip install .
