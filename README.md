# Agential Firework

## Overview

Agential Firework is a project aimed at creating a powerful, private, and extensible AI development environment. It facilitates the setup and use of local Large Language Models (LLMs) and Retrieval Augmented Generation (RAG) agents. This project provides scripts to set up the environment on both macOS (CPU-only) and Ubuntu (with NVIDIA GPU support).

## Directory Structure

A brief overview of the important directories:

-   `agential_framework_env_alt/`: This directory is central to the Python-based agent framework. It contains:
    -   Agent scripts like `rag_agent.py` (for document retrieval) and `tool_agent.py` (for using tools).
    -   Configuration files (e.g., `rag_config.ini`).
    -   The `tools/` subdirectory for pluggable tools.
    -   The Python virtual environment (`venv/`) created by the setup scripts.
-   `agential_framework_env_alt/tools/`: Contains individual tool modules (e.g., `calculator_tool.py`, `get_date_tool.py`) that can be used by `tool_agent.py`. Each tool should inherit from `BaseTool`.
-   `llama_cpp_bin/`: Stores compiled binaries for `llama.cpp` (`llama_main`, `llama_server`). Created by setup scripts.
-   `llama.cpp/`: Contains the source code for `llama.cpp` (cloned by setup scripts).
-   `models/`: This is where you should place your GGUF model files. This directory needs to be created manually or by the setup scripts if adapted.
-   `text_generation_webui_install/`: (On Ubuntu) Contains the installation for `text-generation-webui` if installed using the provided script.

## Setup Instructions

Choose the setup script appropriate for your operating system.

### macOS (CPU-Only Setup)

The macOS setup provides a CPU-based environment. Model inference will be slower than on a GPU-accelerated machine.

1.  **Prerequisites**: Ensure you have an internet connection.
2.  **Run the script**:
    *   Open your terminal.
    *   Navigate to the root of this repository.
    *   Make the script executable: `chmod +x setup_macos.sh`
    *   Run the script: `./setup_macos.sh`
3.  **Script Actions**:
    *   Installs Homebrew (if not present) and necessary tools (`cmake`, `python`, `git`).
    *   Clones this project repository to `/Users/cosmopax/Desktop/agential_firework` (adjust `PROJECT_DIR` in the script if needed).
    *   Clones and compiles `llama.cpp` (CPU version). Binaries (`llama_main`, `llama_server`) are placed in `llama_cpp_bin/`.
    *   Creates a Python virtual environment in `agential_framework_env_alt/venv/` and installs required packages.

### Ubuntu (NVIDIA GPU Setup)

The Ubuntu setup enables GPU acceleration for significantly faster performance, assuming you have compatible NVIDIA hardware and drivers.

1.  **Prerequisites**:
    *   An NVIDIA GPU.
    *   An internet connection.
    *   It's recommended to have NVIDIA drivers already installed. The script can attempt to install them, but a manual setup via "Additional Drivers" or NVIDIA's website is often more robust.
2.  **Run the script**:
    *   Open your terminal.
    *   Navigate to the root of this repository.
    *   Make the script executable: `chmod +x setup_ubuntu.sh`
    *   Run the script with sudo: `sudo ./setup_ubuntu.sh` (sudo is needed for `apt-get` and CUDA installation).
3.  **Script Actions**:
    *   Installs essential packages (`git`, `python3`, `python3-venv`, `cmake`, `build-essential`).
    *   Attempts to install NVIDIA CUDA Toolkit (version 11.8 specified in script).
    *   Clones this project repository to `/home/<your_user>/agential_firework` (adjust `PROJECT_DIR` in script if needed).
    *   Clones and compiles `llama.cpp` with CUDA support (e.g., for RTX 3090 Ti). Binaries (`llama_main_cuda`, `llama_server_cuda`) are placed in `llama_cpp_bin/`.
    *   Creates a Python virtual environment in `agential_framework_env_alt/venv/` and installs packages, including PyTorch with CUDA support.
4.  **Post-Setup**: You might need to log out and log back in or `source ~/.bashrc` for CUDA path changes to take full effect.

## Configuration (`rag_config.ini`)

The `rag_agent.py` script uses a configuration file named `rag_config.ini` located in the same directory (`agential_framework_env_alt/`). If this file is not found when the script is run, a default one will be created. You should review and edit this file to suit your setup. This configuration file is also used by `tool_agent.py` for some settings (e.g., LLM server connection, history length).

The settings are:

-   `[Paths]`
    -   `DOCUMENTS_PATH`: Absolute path to the folder containing your local documents (supports `.txt`, `.md`, and `.pdf` files) for the RAG agent. Example: `/path/to/your/documents` or `C:\Users\YourName\Documents\ResearchPapers`.
    -   `CHROMA_DB_PATH`: Path to the Chroma vector database. If relative (e.g., `./chroma_db_local_docs`), it's relative to the `rag_agent.py` script itself.
-   `[Models]`
    -   `EMBEDDING_MODEL`: The name of the HuggingFace sentence transformer model to use for embeddings (e.g., `all-MiniLM-L6-v2`).
    -   `LLAMA_SERVER_API_BASE`: The base URL for the `llama.cpp` server's OpenAI-compatible API (e.g., `http://127.0.0.1:8080/v1`). This is used by both RAG and Tool agents.
    -   `EMBEDDINGS_DEVICE`: Specifies the device for calculating embeddings (used by RAG agent). Options:
        -   `auto`: (Default) Attempts to use `cuda` if available (PyTorch detects a CUDA GPU), otherwise falls back to `cpu`.
        -   `cuda`: Forces the use of CUDA. If not available, it will fall back to `cpu` with a warning.
        -   `cpu`: Forces the use of CPU for embeddings.
-   `[Conversation]`
    -   `HISTORY_K`: The number of past user/AI interaction pairs to keep in conversation memory (e.g., `3` means the last 3 questions and their answers will be remembered). Used by both RAG and Tool agents.

**Important**:
- After the default `rag_config.ini` is created, you **must** update `DOCUMENTS_PATH` to point to the actual location of your documents for the RAG agent to work.
- For faster document processing and query embedding on Ubuntu systems with a compatible NVIDIA GPU, ensure PyTorch with CUDA is installed (handled by `setup_ubuntu.sh`) and set `EMBEDDINGS_DEVICE = auto` or `EMBEDDINGS_DEVICE = cuda` in `rag_config.ini`.

## Using the RAG Agent (`rag_agent.py`)

The RAG agent allows you to chat with your local documents, with answers derived from your content and including source document citations.

1.  **Place Documents**: Put your `.txt`, `.md`, or `.pdf` documents into a folder.
2.  **Configure `rag_config.ini`**:
    *   Locate the `rag_config.ini` file in the `agential_framework_env_alt/` directory. (If it wasn't there, running `rag_agent.py` once will create a default version).
    *   Open `rag_config.ini` and **crucially, update the `DOCUMENTS_PATH` setting** under the `[Paths]` section to the absolute path of your documents folder.
    *   Adjust other settings like `CHROMA_DB_PATH`, `EMBEDDING_MODEL`, `LLAMA_SERVER_API_BASE`, `EMBEDDINGS_DEVICE`, and `HISTORY_K` as needed. Refer to the "Configuration (`rag_config.ini`)" section above for details on each setting.
3.  **Start `llama_server`**:
    *   Navigate to `llama_cpp_bin/`.
    *   Run the server:
        *   macOS: `./llama_server -m <path_to_your_model.gguf> -c <context_size>`
        *   Ubuntu: `./llama_server_cuda -m <path_to_your_model.gguf> -c <context_size> -ngl <number_of_gpu_layers>` (e.g., `-ngl 35` for a 7B model)
    *   Replace `<path_to_your_model.gguf>` with the actual path to your GGUF model file (e.g., `../models/your_model.gguf`).
4.  **Run the RAG Agent**:
    *   Open a new terminal.
    *   Navigate to the project root.
    *   Activate the Python environment: `source agential_framework_env_alt/venv/bin/activate`
    *   Navigate to the agent's directory: `cd agential_framework_env_alt`
    *   Run the script: `python rag_agent.py`
    *   To force re-indexing of documents: `python rag_agent.py --reindex`
    *   Type your questions and press Enter. Type `exit` or `quit` to end.
    *   **Conversation History**: The agent now remembers the number of interactions defined by `HISTORY_K` in `rag_config.ini` (user queries and AI responses) to provide more contextually relevant answers.
    *   **Reset History**: To clear the conversation history and start a fresh topic, type `/reset` as your question.
    *   **Source Citations**: The agent will now attempt to cite the source document(s) from which it derives its answers. The context provided to the LLM includes filenames, and the LLM is prompted to use them.

## Using `text-generation-webui` (Ubuntu with GPU)

`text-generation-webui` provides a graphical interface for interacting with various LLMs.

1.  **Prerequisites**:
    *   `setup_ubuntu.sh` should have been run successfully, especially the CUDA setup.
2.  **Run the setup script**:
    *   Navigate to the root of this repository.
    *   Make the script executable: `chmod +x setup_text_generation_webui.sh`
    *   Run the script: `./setup_text_generation_webui.sh` (This script installs Miniconda and the web UI in user space, typically under `~/text_generation_webui_install`).
3.  **Start the Web UI**:
    *   Open a new terminal or `source ~/.bashrc` to ensure Conda is initialized.
    *   Activate the Conda environment: `conda activate textgen` (or the name you used if modified in the script).
    *   Navigate to the web UI directory (e.g., `cd ~/text_generation_webui_install/text-generation-webui`).
    *   Start the server: `python server.py --listen --model-dir <path_to_your_models_directory>`
        *   Replace `<path_to_your_models_directory>` with the path to your GGUF models (e.g., `../../models` if your project is `~/agential_firework` and models are in `~/agential_firework/models`).
4.  **Access**: Open your web browser to `http://0.0.0.0:7860` (or the address shown in the terminal).
5.  **Model Selection**:
    *   Go to the "Model" tab in the UI.
    *   Use the dropdown to select your model.
    *   Ensure the correct "loader" (e.g., `llama.cpp` for GGUF models) is chosen.
    *   Click "Load".

## Using the Tool-Using Agent (`tool_agent.py`)

The Tool-Using Agent (`tool_agent.py`) is an experimental agent capable of utilizing a collection of "tools" to answer questions or perform tasks that go beyond the direct knowledge of the LLM.

### Overview

This agent works by:
1.  Receiving a query from the user.
2.  Consulting an LLM, providing it with the user's query, conversation history, and a list of available tools (with their descriptions).
3.  The LLM then decides if a tool is appropriate. If so, it specifies which tool to use and what input (parameters) to give it. If not, the LLM provides a direct answer.
4.  If a tool is chosen, the agent executes it and returns the tool's output.

### Configuration

-   **LLM Server**: The agent uses the `LLAMA_SERVER_API_BASE` setting from the shared `agential_framework_env_alt/rag_config.ini` file to connect to your local `llama.cpp` server.
-   **Conversation History**: It also uses the `HISTORY_K` setting from `rag_config.ini` for its conversation memory size.

### Available Tools

Tools are located as individual Python files in the `agential_framework_env_alt/tools/` directory. Each tool provides a name and a description of its capabilities and expected parameters. The agent dynamically loads these tools when it starts.

Currently implemented tools:
-   **`CalculatorTool`**: Evaluates basic arithmetic expressions (e.g., "2 + 3 * 4", "100 / 5").
-   **`GetCurrentDateTool`**: Returns the current date and time.

The agent will list all successfully loaded tools upon startup.

### Running the Agent

1.  **Start `llama_server`**: Ensure your `llama.cpp` server is running (same as for the RAG agent). Provide a model that is good at following instructions and structured output.
    *   Example (Ubuntu with GPU, from project root): `cd llama_cpp_bin && ./llama_server_cuda -m ../models/your_model.gguf -c 2048 -ngl 35`
    *   (Adjust context size `-c` and GPU layers `-ngl` as needed).
2.  **Run `tool_agent.py`**:
    *   Open a new terminal.
    *   Navigate to the project root: `cd /path/to/your/agential_firework`
    *   Activate the Python environment: `source agential_framework_env_alt/venv/bin/activate`
    *   Navigate to the agent's directory: `cd agential_framework_env_alt`
    *   Run the script: `python tool_agent.py`
3.  **Interact**:
    *   The agent will initialize and list available tools.
    *   Type your query and press Enter.
    *   To clear conversation history, type `/reset`.
    *   To exit, type `exit` or `quit`.

### Extending with New Tools

You can add new tools by:
1.  Creating a new Python file in the `agential_framework_env_alt/tools/` directory (e.g., `my_new_tool.py`).
2.  Inside this file, define a class that inherits from `BaseTool` (from `tools.base_tool`).
3.  Your class must override the `name` (string) and `description` (string) attributes. The description should clearly explain what the tool does and what parameters it expects (if any).
4.  Implement the `execute(self, params: str) -> str` method. This method takes a single string `params` (which your tool will need to parse if necessary) and must return a string result.
The `tool_agent.py` will automatically discover and attempt to load any such tools when it starts.

## Other Scripts

-   **`download_deps_for_linux.sh`**:
    *   Run on macOS or another machine with internet to download Linux Python packages for offline transfer to your Ubuntu machine.
    *   Creates an `offline_pip_cache_for_linux` directory.
    *   See script comments for usage on the Ubuntu side.

---
This README will be updated as new features are added to the Agential Firework project.
