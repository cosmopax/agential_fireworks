#!/bin/bash
# ==============================================================================
# Setup Script for text-generation-webui on Ubuntu (with Conda)
# ==============================================================================

set -euo pipefail

# --- Configuration ---
# IMPORTANT: Adjust if you prefer a different installation location.
readonly PROJECT_USER="${USER:-cosmopax}" # Use current user or default to cosmopax
readonly BASE_INSTALL_DIR="/home/$PROJECT_USER/text_generation_webui_install"
readonly WEBUI_DIR="$BASE_INSTALL_DIR/text-generation-webui"
readonly CONDA_ENV_NAME="textgen"
# It's assumed CUDA is already installed (e.g., by setup_ubuntu.sh)
# And that basic tools like git, wget are present.

# --- Helper Functions ---
print_info() {
  echo -e "\n\033[1;34m[INFO]\033[0m $1"
}
print_success() {
  echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}
print_warning() {
  echo -e "\033[1;33m[WARNING]\033[0m $1"
}

# --- Script Execution ---
print_info "Starting text-generation-webui setup..."

# Step 1: Install Miniconda (if not already installed)
if ! command -v conda &> /dev/null; then
    print_info "Miniconda not found. Installing Miniconda..."
    mkdir -p "$BASE_INSTALL_DIR/miniconda3"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O "$BASE_INSTALL_DIR/miniconda3/miniconda.sh"
    bash "$BASE_INSTALL_DIR/miniconda3/miniconda.sh" -b -u -p "$BASE_INSTALL_DIR/miniconda3"
    rm -rf "$BASE_INSTALL_DIR/miniconda3/miniconda.sh"
    # Initialize Conda for the current shell and add to PATH for future sessions
    print_info "Initializing Conda. You might need to start a new shell or source ~/.bashrc after this script."
    eval "$("$BASE_INSTALL_DIR/miniconda3/bin/conda" 'shell.bash' 'hook')"
    conda init bash
    # Add conda to PATH for this script's session
    export PATH="$BASE_INSTALL_DIR/miniconda3/bin:$PATH"
    print_success "Miniconda installed and initialized."
else
    print_info "Miniconda already installed."
    # Ensure conda is available in PATH for this script's session if already installed
    if ! command -v conda &> /dev/null; then
      # Try common installation paths if not in current PATH
      if [ -f "$HOME/miniconda3/bin/conda" ]; then
        export PATH="$HOME/miniconda3/bin:$PATH"
        eval "$("$HOME/miniconda3/bin/conda" 'shell.bash' 'hook')"
      elif [ -f "$HOME/opt/miniconda3/bin/conda" ]; then
        export PATH="$HOME/opt/miniconda3/bin:$PATH"
        eval "$("$HOME/opt/miniconda3/bin/conda" 'shell.bash' 'hook')"
      elif [ -f "$BASE_INSTALL_DIR/miniconda3/bin/conda" ]; then # If installed by this script previously
        export PATH="$BASE_INSTALL_DIR/miniconda3/bin:$PATH"
        eval "$("$BASE_INSTALL_DIR/miniconda3/bin/conda" 'shell.bash' 'hook')"
      else
        print_warning "Conda is installed but not found in PATH. Please add it to your PATH and re-run."
        exit 1
      fi
    fi
fi

# Step 2: Create Conda environment for text-generation-webui
if conda env list | grep -q "$CONDA_ENV_NAME"; then
    print_info "Conda environment '$CONDA_ENV_NAME' already exists."
else
    print_info "Creating Conda environment '$CONDA_ENV_NAME'..."
    # Specify Python version compatible with text-generation-webui, e.g., 3.10 or 3.11
    # Also install PyTorch with CUDA. Ensure your CUDA toolkit version matches.
    # Example: PyTorch for CUDA 11.8
    conda create -n "$CONDA_ENV_NAME" python=3.10 -y
    print_success "Conda environment '$CONDA_ENV_NAME' created."
fi

# Activate Conda environment
print_info "Activating Conda environment '$CONDA_ENV_NAME'..."
# Sourcing conda.sh to ensure 'conda activate' is available in script
if [ -f "$BASE_INSTALL_DIR/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$BASE_INSTALL_DIR/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/opt/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/opt/miniconda3/etc/profile.d/conda.sh"
fi
conda activate "$CONDA_ENV_NAME"

# Install PyTorch with CUDA (must match system CUDA toolkit version for llama-cpp-python etc.)
# Assuming CUDA 11.8 was installed by setup_ubuntu.sh.
# PyTorch command from: https://pytorch.org/get-started/locally/
print_info "Installing PyTorch with CUDA 11.8 support in '$CONDA_ENV_NAME' env..."
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y

# Step 3: Clone text-generation-webui repository
if [ -d "$WEBUI_DIR" ]; then
    print_info "text-generation-webui directory already exists. Pulling latest changes..."
    cd "$WEBUI_DIR"
    git pull
else
    print_info "Cloning text-generation-webui repository..."
    mkdir -p "$BASE_INSTALL_DIR"
    git clone https://github.com/oobabooga/text-generation-webui.git "$WEBUI_DIR"
    cd "$WEBUI_DIR"
fi

# Step 4: Install dependencies
print_info "Installing text-generation-webui dependencies..."
# Some dependencies might be better installed via conda, others pip.
# The webui's requirements.txt is usually the primary guide.
# Often it's good to install specific versions of transformers, etc.
# For a robust setup, sometimes specific commits or versions are needed.
# This uses the standard requirements.txt.
pip install -r requirements.txt
# If issues arise with bitsandbytes or other specific packages, they may need manual install steps.
# e.g. pip install bitsandbytes==0.39.0

# For llama-cpp-python with BLAS and CUDA support (matching the llama.cpp compilation if possible)
# CMAKE_ARGS are important here.
# Ensure your CUDA toolkit's nvcc is in PATH.
# The version of CUDA used for llama-cpp-python should ideally match system llama.cpp compile
export CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCMAKE_CUDA_ARCHITECTURES=86" # For RTX 3090 Ti
export FORCE_CMAKE=1
pip uninstall llama-cpp-python -y # Uninstall if it was installed as a generic dependency
pip install llama-cpp-python --no-cache-dir
print_success "text-generation-webui dependencies installed."

# Step 5: Download a default model (optional, example)
# print_info "Downloading a small example model (TheBloke/Mistral-7B-Instruct-v0.1-GGUF)..."
# python download-model.py TheBloke/Mistral-7B-Instruct-v0.1-GGUF --output "$WEBUI_DIR/models"
# print_success "Example model downloaded."

# Deactivate environment for now
conda deactivate

print_success "text-generation-webui setup is complete."
echo -e "\nTo run text-generation-webui:"
echo "1. Open a new terminal or source your ~/.bashrc (e.g., 'source ~/.bashrc')."
echo "2. Activate the Conda environment: 'conda activate $CONDA_ENV_NAME'"
echo "3. Navigate to the webui directory: 'cd $WEBUI_DIR'"
echo "4. Start the server: 'python server.py --listen --model-dir $WEBUI_DIR/models'"
echo "   (Or your preferred models directory. The loader selection in the UI will depend on the model type, e.g. GGUF for llama.cpp)"
echo "5. Open your browser to the displayed address (usually http://0.0.0.0:7860)."
echo -e "\nModel Selection in UI:"
echo "- Once the server is running and you open the web UI:"
echo "- Go to the 'Model' tab."
echo "- You should see a dropdown menu labeled 'Model'. Click it to see compatible models found in your model directory."
echo "- If you are using GGUF models (recommended for llama.cpp backend), ensure they are in the directory specified by '--model-dir'."
echo "- You might need to click a 'Load' or 'Refresh' button next to the model selection if it doesn't populate automatically."
echo "- The correct 'loader' (e.g., llama.cpp, Transformers) should also be selected or auto-detected based on the model type."
echo "- If the 'select model' option is missing or empty, common reasons are:"
echo "  - No models found in the specified model directory."
echo "  - Incorrect model format for the selected loader."
echo "  - Issues with the Python environment or dependencies (check terminal for errors)."
echo "  - The server needs to be restarted after placing new models in the directory."
