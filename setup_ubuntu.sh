#!/bin/bash
# ==============================================================================
# Setup Script for Agential AI Development Environment on Ubuntu (GPU support)
# ==============================================================================

set -euo pipefail

# --- Configuration ---
# IMPORTANT: Adjust PROJECT_DIR if you prefer a different location.
readonly PROJECT_USER="${USER:-cosmopax}" # Use current user or default to cosmopax
readonly PROJECT_DIR="/home/$PROJECT_USER/agential_firework"
readonly AGENT_PY_ENV_DIR="$PROJECT_DIR/agential_framework_env_alt"
readonly LLAMA_CPP_DIR="$PROJECT_DIR/llama.cpp"
readonly LLAMA_CPP_BIN_DIR="$PROJECT_DIR/llama_cpp_bin"
# IMPORTANT: Replace with your actual GitHub repository URL if different.
readonly GITHUB_REPO_URL="https://github.com/cosmopax/agential_firework.git"
# CUDA Version - This should be chosen based on compatibility with drivers and PyTorch
# For RTX 3090 Ti, CUDA 11.8 or 12.x are common. Let's target 11.8 for broader compatibility.
readonly CUDA_VERSION_MAJOR_MINOR="11.8"
readonly CUDA_VERSION_FULL="11.8.0"
readonly CUDA_INSTALLER_URL="https://developer.download.nvidia.com/compute/cuda/${CUDA_VERSION_FULL}/local_installers/cuda_${CUDA_VERSION_FULL}_520.61.05_linux.run"
readonly CUDA_INSTALLER_FILENAME="cuda_installer.run"


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
print_error() {
  echo -e "\033[1;31m[ERROR]\033[0m $1" >&2
}

# --- Script Execution ---
print_info "Starting Ubuntu AI Development Environment Setup (with GPU support)..."
sudo apt-get update

# Step 1: Install basic dependencies
print_info "Installing basic dependencies (git, python3, python3-venv, cmake, build-essential)..."
sudo apt-get install -y git python3 python3-venv python3-pip cmake build-essential
print_success "Basic dependencies installed."

# Step 2: Install NVIDIA CUDA Toolkit
# This is a simplified CUDA install. Production systems might need more specific driver management.
if ! command -v nvcc &> /dev/null || ! nvcc --version | grep -q "Cuda compilation tools, release ${CUDA_VERSION_MAJOR_MINOR}"; then
    print_info "NVIDIA CUDA Toolkit ${CUDA_VERSION_MAJOR_MINOR} not found or version mismatch. Attempting to install..."
    if ! lsmod | grep -q nvidia; then
        print_warning "NVIDIA kernel modules do not seem to be loaded. Ensure you have NVIDIA drivers installed compatible with CUDA ${CUDA_VERSION_MAJOR_MINOR}."
        print_warning "This script will attempt to install the CUDA toolkit, which includes a driver, but pre-installing a driver via 'Additional Drivers' or nvidia.com is often more robust."
        read -p "Do you want to proceed with CUDA Toolkit installation? (y/N): " confirm_cuda
        if [[ "$confirm_cuda" != "y" && "$confirm_cuda" != "Y" ]]; then
            print_error "CUDA installation aborted by user. llama.cpp GPU compilation will likely fail."
        else
            print_info "Downloading CUDA ${CUDA_VERSION_FULL} installer..."
            wget -P /tmp "$CUDA_INSTALLER_URL" -O "/tmp/$CUDA_INSTALLER_FILENAME"
            print_info "Running CUDA installer. This may take a while. Please follow on-screen instructions."
            print_warning "It is recommended to DESELECT the driver installation if you already have a compatible NVIDIA driver installed."
            sudo sh "/tmp/$CUDA_INSTALLER_FILENAME" --silent --driver --toolkit --samples
            rm "/tmp/$CUDA_INSTALLER_FILENAME"

            print_info "Adding CUDA to PATH. You might need to source ~/.bashrc or relogin."
            echo 'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}' | sudo tee /etc/profile.d/cuda.sh > /dev/null
            echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' | sudo tee -a /etc/profile.d/cuda.sh > /dev/null
            source /etc/profile.d/cuda.sh
        fi
    else
        print_info "NVIDIA drivers detected. Assuming they are compatible. Skipping separate CUDA driver install if toolkit is already present."
        # If nvcc is present but wrong version, or not present but drivers are, try installing only toolkit
        if ! command -v nvcc &> /dev/null || ! nvcc --version | grep -q "Cuda compilation tools, release ${CUDA_VERSION_MAJOR_MINOR}"; then
             print_info "Downloading CUDA ${CUDA_VERSION_FULL} installer (toolkit only)..."
            wget -P /tmp "$CUDA_INSTALLER_URL" -O "/tmp/$CUDA_INSTALLER_FILENAME"
            print_info "Running CUDA installer (toolkit only). This may take a while."
            sudo sh "/tmp/$CUDA_INSTALLER_FILENAME" --silent --toolkit --samples
            rm "/tmp/$CUDA_INSTALLER_FILENAME"

            print_info "Adding CUDA to PATH. You might need to source ~/.bashrc or relogin."
            echo 'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}' | sudo tee /etc/profile.d/cuda.sh > /dev/null
            echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' | sudo tee -a /etc/profile.d/cuda.sh > /dev/null
            source /etc/profile.d/cuda.sh
        fi
    fi
    if command -v nvcc &> /dev/null && nvcc --version | grep -q "Cuda compilation tools, release ${CUDA_VERSION_MAJOR_MINOR}"; then
        print_success "NVIDIA CUDA Toolkit ${CUDA_VERSION_MAJOR_MINOR} is ready."
    else
        print_warning "CUDA Toolkit installation might have had issues or requires a logout/reboot. Please verify 'nvcc --version'."
    fi
else
    print_info "NVIDIA CUDA Toolkit ${CUDA_VERSION_MAJOR_MINOR} already installed."
    # Ensure PATH is set for the current session if already installed
    if [[ -z "${CUDA_PATH}" ]] && [[ -d "/usr/local/cuda-${CUDA_VERSION_MAJOR_MINOR}" ]]; then
        export PATH="/usr/local/cuda-${CUDA_VERSION_MAJOR_MINOR}/bin${PATH:+:${PATH}}"
        export LD_LIBRARY_PATH="/usr/local/cuda-${CUDA_VERSION_MAJOR_MINOR}/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
    elif [[ -z "${CUDA_PATH}" ]] && [[ -d "/usr/local/cuda" ]]; then
        export PATH="/usr/local/cuda/bin${PATH:+:${PATH}}"
        export LD_LIBRARY_PATH="/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
    fi
fi


# Step 3: Create project directory and clone repository
print_info "Setting up project directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
if [ -d "$PROJECT_DIR/.git" ]; then
    print_info "Project directory already exists and is a git repo. Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull
else
    print_info "Cloning project repository from GitHub into $PROJECT_DIR..."
    git clone "$GITHUB_REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi
print_success "Project repository is up to date in $PROJECT_DIR."

# Step 4: Compile llama.cpp with CUDA support
print_info "Compiling llama.cpp (with CUDA support)..."
mkdir -p "$LLAMA_CPP_BIN_DIR"
if [ ! -d "$LLAMA_CPP_DIR" ]; then
    git clone https://github.com/ggerganov/llama.cpp.git "$LLAMA_CPP_DIR"
fi
cd "$LLAMA_CPP_DIR"
git pull # Ensure it's the latest version
make clean
# Attempt to build with CUDA. Ensure CUDA_PATH is set if nvcc is not in default PATH.
# Common flags for NVIDIA Ampere (RTX 30xx)
# Adjust CMAKE_CUDA_ARCHITECTURES based on specific GPU. For 3090 Ti (GA102), 86 is correct.
print_info "Compiling llama.cpp with LLAMA_CUDA=1. This may take a while..."
make LLAMA_CUDA=1 -j$(nproc) CMAKE_CUDA_ARCHITECTURES=86
cp ./main "$LLAMA_CPP_BIN_DIR/llama_main_cuda"
cp ./server "$LLAMA_CPP_BIN_DIR/llama_server_cuda"
print_success "llama.cpp compiled with CUDA and binaries copied."
cd "$PROJECT_DIR"

# Step 5: Set up Python Virtual Environment
print_info "Setting up Python virtual environment for Agential Framework..."
mkdir -p "$AGENT_PY_ENV_DIR" # Ensure parent directory for venv exists
if [ ! -d "$AGENT_PY_ENV_DIR/venv" ]; then
  print_info "Creating Python virtual environment..."
  python3 -m venv "$AGENT_PY_ENV_DIR/venv"
fi
print_info "Activating and installing/updating Agential Framework dependencies..."
source "$AGENT_PY_ENV_DIR/venv/bin/activate"
pip install --upgrade pip
# Consider if torch should be installed with CUDA support specific version here
# e.g. pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
print_info "Installing PyTorch with CUDA ${CUDA_VERSION_MAJOR_MINOR} support..."
pip install torch torchvision torchaudio --index-url "https://download.pytorch.org/whl/cu$(echo $CUDA_VERSION_MAJOR_MINOR | tr -d '.')"
print_info "Installing other Python dependencies..."
pip install requests langchain langchain-community langchain-experimental chromadb sentence-transformers pypdf tavily-python
deactivate
print_success "Python virtual environment for Agential Framework is ready."

# Step 6: Create other necessary directories
print_info "Creating additional directories (e.g., models)..."
mkdir -p "$PROJECT_DIR/models"
print_success "Directory structure prepared."

echo -e "\n\033[1;32m*** Ubuntu setup complete! ***\033[0m"
echo "Please ensure CUDA is correctly in your PATH and LD_LIBRARY_PATH."
echo "You may need to 'source ~/.bashrc' or log out and log back in."
echo "To activate the Python environment, run: source $AGENT_PY_ENV_DIR/venv/bin/activate"
echo "Llama.cpp CUDA binaries are in: $LLAMA_CPP_BIN_DIR"
