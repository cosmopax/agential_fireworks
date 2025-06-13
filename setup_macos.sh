#!/bin/bash
# ==============================================================================
# Setup Script for Agential AI Development Environment on macOS (CPU-only)
# ==============================================================================

set -euo pipefail

# --- Configuration ---
readonly PROJECT_DIR="/Users/cosmopax/Desktop/agential_firework"
readonly AGENT_PY_ENV_DIR="$PROJECT_DIR/agential_framework_env_alt"
readonly LLAMA_CPP_DIR="$PROJECT_DIR/llama.cpp"
readonly LLAMA_CPP_BIN_DIR="$PROJECT_DIR/llama_cpp_bin"
# IMPORTANT: Replace with your actual GitHub repository URL
readonly GITHUB_REPO_URL="https://github.com/cosmopax/agential_firework.git"

# --- Helper Functions ---
print_info() {
  echo -e "\n\033[1;34m[INFO]\033[0m $1"
}
print_success() {
  echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}
# --- Script Execution ---
print_info "Starting macOS AI Development Environment Setup..."
# Step 1: Install Homebrew (macOS Package Manager) if not present
if ! command -v brew &> /dev/null; then
    print_info "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if [ -x "/opt/homebrew/bin/brew" ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    print_info "Homebrew already installed. Updating..."
    brew update
fi
print_success "Homebrew is ready."

# Step 2: Install necessary tools with Homebrew
print_info "Installing dependencies with Homebrew (cmake, python, git)..."
brew install cmake python git

# Step 3: Clone the project repository from GitHub
if [ -d "$PROJECT_DIR" ]; then
    print_info "Project directory already exists. Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull
else
    print_info "Cloning project repository from GitHub..."
    # Ensuring the parent directory exists before attempting to clone into it.
    mkdir -p "/Users/cosmopax/Desktop/"
    cd "/Users/cosmopax/Desktop/"
    git clone "$GITHUB_REPO_URL" "$PROJECT_DIR" # Clone into the specific project directory
    cd "$PROJECT_DIR"
fi
print_success "Project repository is up to date."

# Step 4: Compile llama.cpp for macOS CPU
print_info "Compiling llama.cpp (CPU-only)..."
mkdir -p "$LLAMA_CPP_BIN_DIR"
if [ ! -d "$LLAMA_CPP_DIR" ]; then
    # Clone llama.cpp into the designated LLAMA_CPP_DIR
    git clone https://github.com/ggerganov/llama.cpp.git "$LLAMA_CPP_DIR"
fi
cd "$LLAMA_CPP_DIR"
make clean
# Standard 'make' will compile with CPU optimizations like AVX2 on your Intel Mac
make -j$(sysctl -n hw.ncpu)
cp ./main "$LLAMA_CPP_BIN_DIR/llama_main"
cp ./server "$LLAMA_CPP_BIN_DIR/llama_server"
print_success "llama.cpp compiled and binaries copied."
cd "$PROJECT_DIR" # Return to project directory

# Step 5: Set up Python Virtual Environment
print_info "Setting up Python virtual environment for Agential Framework..."
if [ ! -d "$AGENT_PY_ENV_DIR/venv" ]; then
  print_info "Creating Python virtual environment..."
  python3 -m venv "$AGENT_PY_ENV_DIR/venv" # This should be AGENT_PY_ENV_DIR not $PROJECT_DIR
fi
print_info "Activating and ensuring Agential Framework dependencies are up-to-date..."
source "$AGENT_PY_ENV_DIR/venv/bin/activate"
pip install --upgrade pip
pip install requests langchain langchain-community langchain-experimental chromadb sentence-transformers torch pypdf
deactivate
print_success "Dependency check/install for Agential Framework is complete."

echo -e "\n\033[1;32m*** macOS setup complete! ***\033[0m"
