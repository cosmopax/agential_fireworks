#!/bin/bash
# 1. Navigate to your Desktop
# This script is intended to be run from where it is,
# so we'll create the directories relative to the script's location or a defined base path.
# For simplicity, let's assume it's run from the project root or a specific directory.
# We will create a directory for its output within the project structure if possible,
# or use ~/Desktop as a fallback if the script is moved.

# Define a base directory for output, ideally within the project.
# If PROJECT_DIR is set (e.g. by a calling script), use it. Otherwise, default to Desktop.
BASE_OUTPUT_DIR="${PROJECT_DIR:-$HOME/Desktop}"
OUTPUT_DIR="$BASE_OUTPUT_DIR/offline_pip_cache_for_linux"
REQUIREMENTS_FILE="$BASE_OUTPUT_DIR/requirements_for_linux.txt"

echo "Preparing to download Linux Python dependencies."
echo "Output will be saved in: $OUTPUT_DIR"
echo "Requirements will be temporarily stored in: $REQUIREMENTS_FILE"

# 2. Define the packages needed.
cat > "$REQUIREMENTS_FILE" << REQ_EOF
requests
langchain
langchain-community
langchain-experimental
chromadb
sentence-transformers
pypdf
tavily-python
duckduckgo-search
REQ_EOF

echo "Created requirements file:"
cat "$REQUIREMENTS_FILE"

# 3. Create a directory to store the packages.
mkdir -p "$OUTPUT_DIR"

echo "Downloading packages for Linux (manylinux_2_17_x86_64) and Python 3.13..."
# 4. Download packages for Linux (manylinux) and Python 3.13.
python3 -m pip download \
    --platform manylinux_2_17_x86_64 \
    --python-version 3.13 \
    --only-binary=:all: \
    -r "$REQUIREMENTS_FILE" \
    -d "$OUTPUT_DIR"

# It's good practice to remove the temporary requirements file
rm "$REQUIREMENTS_FILE"

echo "Download complete. Copy the '$OUTPUT_DIR' directory to your Ubuntu PC."
echo "Inside that directory, you can use pip install --no-index --find-links=. -r requirements.txt (you'll need to recreate a small requirements.txt there or install packages individually)."
