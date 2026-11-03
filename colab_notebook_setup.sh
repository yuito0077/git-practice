#!/bin/bash
set -e

echo "Setting up Evolutionary Model Merge Pipeline dependencies..."

# Update and install build tools
sudo apt-get update
sudo apt-get install -y build-essential cmake

# Install Python dependencies for merging and optimization
pip install -q -U "mergekit[vllm]" optuna cmaes transformers huggingface_hub torch accelerate
pip install -q -U datasets evaluate scikit-learn

# Setup llama.cpp for GGUF conversion
if [ ! -d "llama.cpp" ]; then
    echo "Cloning llama.cpp for GGUF export..."
    git clone https://github.com/ggerganov/llama.cpp.git
    cd llama.cpp
    pip install -r requirements.txt
    make -j
    cd ..
fi

echo "Setup complete!"
