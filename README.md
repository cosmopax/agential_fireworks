# Agential Firework

## Overview

Agential Firework is a project aimed at creating a powerful, private, and extensible AI development environment. It facilitates the setup and use of local Large Language Models (LLMs) and Retrieval Augmented Generation (RAG) agents. This project provides scripts to set up the environment on both macOS (CPU-only) and Ubuntu (with NVIDIA GPU support).

## Directory Structure

A brief overview of the important directories:

-   `agential_framework_env_alt/`: This directory is central to the Python-based agent framework. It contains:
    -   Agent scripts like `rag_agent.py` (for document retrieval) and `tool_agent.py` (for using tools).
    -   Configuration files (e.g., `rag_config.ini` for the RAG agent, `tool_agent_config.ini` for the Tool-agent).
    -   The `tools/` subdirectory for pluggable tools.
    -   The Python virtual environment (`venv/`) created by the setup scripts.
-   `agential_framework_env_alt/tools/`: Contains individual tool modules (e.g., `calculator_tool.py`, `get_date_tool.py`, `list_directory_tool.py`, `read_file_tool.py`) that can be used by `tool_agent.py`. Each tool should inherit from `BaseTool`.
-   `llama_cpp_bin/`: Stores compiled binaries for `llama.cpp` (`llama_main`, `llama_server`). Created by setup scripts.
-   `llama.cpp/`: Contains the source code for `llama.cpp` (cloned by setup scripts).
-   `models/`: This is where you should place your GGUF model files. This directory needs to be created manually or by the setup scripts if adapted.
-   `text_generation_webui_install/`: (On Ubuntu) Contains the installation for `text-generation-webui` if installed using the provided script.

## Setup Instructions

Choose the setup script appropriate for your operating system.

### macOS (CPU-Only Setup)
(Content remains the same)

### Ubuntu (NVIDIA GPU Setup)
(Content remains the same)

## Configuration (`rag_config.ini`)

The `rag_agent.py` script uses its dedicated configuration file named `rag_config.ini`, located in the `agential_framework_env_alt/` directory. If this file is not found when the `rag_agent.py` script is run, a default one will be created. You should review and edit this file to suit your RAG agent setup.

The settings are:

-   `[Paths]`
    -   `DOCUMENTS_PATH`: Absolute path to the folder containing your local documents (supports `.txt`, `.md`, and `.pdf` files) for the RAG agent. Example: `/path/to/your/documents` or `C:\Users\YourName\Documents\ResearchPapers`.
    -   `CHROMA_DB_PATH`: Path to the Chroma vector database. If relative (e.g., `./chroma_db_local_docs`), it's relative to the `rag_agent.py` script itself.
-   `[Models]`
    -   `EMBEDDING_MODEL`: The name of the HuggingFace sentence transformer model to use for embeddings (e.g., `all-MiniLM-L6-v2`).
    -   `LLAMA_SERVER_API_BASE`: The base URL for the `llama.cpp` server's OpenAI-compatible API (e.g., `http://127.0.0.1:8080/v1`). This is used by the RAG agent.
    -   `EMBEDDINGS_DEVICE`: Specifies the device for calculating embeddings (used by RAG agent). Options:
        -   `auto`: (Default) Attempts to use `cuda` if available (PyTorch detects a CUDA GPU), otherwise falls back to `cpu`.
        -   `cuda`: Forces the use of CUDA. If not available, it will fall back to `cpu` with a warning.
        -   `cpu`: Forces the use of CPU for embeddings.
-   `[Conversation]`
    -   `HISTORY_K`: The number of past user/AI interaction pairs to keep in conversation memory for the RAG agent (e.g., `3`).

**Important**:
- After the default `rag_config.ini` is created, you **must** update `DOCUMENTS_PATH` to point to the actual location of your documents for the RAG agent to work.
- For faster document processing and query embedding on Ubuntu systems with a compatible NVIDIA GPU, ensure PyTorch with CUDA is installed (handled by `setup_ubuntu.sh`) and set `EMBEDDINGS_DEVICE = auto` or `EMBEDDINGS_DEVICE = cuda` in `rag_config.ini`.

## Using the RAG Agent (`rag_agent.py`)
(Content remains the same, but ensure references to LLAMA_SERVER_API_BASE and HISTORY_K are consistent with rag_config.ini if they were previously implies as shared)

## Using `text-generation-webui` (Ubuntu with GPU)
(Content remains the same)

## Using the Tool-Using Agent (`tool_agent.py`)

The Tool-Using Agent (`tool_agent.py`) is an experimental agent capable of utilizing a collection of "tools" to answer questions or perform tasks that go beyond the direct knowledge of the LLM.

### Overview

This agent works by:
1.  Receiving a query from the user.
2.  Consulting an LLM, providing it with the user's query, conversation history, and a list of available tools.
3.  The LLM then decides if a tool is appropriate.
    - If so, it specifies which tool to use and the input (parameters) for that tool.
    - If not, the LLM provides a direct answer.
4.  If a tool is chosen, the agent executes it.
5.  The output from the tool is then passed back to the LLM (along with the original query and history).
6.  The LLM synthesizes this information into a final, natural language response for the user.
If no tool was chosen initially, the LLM's direct answer from step 3 is provided to the user.

### Configuration (`tool_agent_config.ini`)

The `tool_agent.py` script uses its own dedicated configuration file: `agential_framework_env_alt/tool_agent_config.ini`. If this file is not found when the script is run, a default one will be created. You should review and edit this file.

Key settings include:

-   `[LLM]`
    -   `LLAMA_SERVER_API_BASE`: URL for the `llama.cpp` server's API.
    -   `TOOL_LLM_TEMPERATURE`: Temperature setting for the LLM when making tool-related decisions and generating responses (e.g., `0.1` for more deterministic output).
-   `[Conversation]`
    -   `TOOL_AGENT_HISTORY_K`: Number of past interaction pairs for conversation memory.
-   `[Tools]`
    -   `PROJECT_SANDBOX_DIR`: Defines the intended root directory for safe OS operations by tools. Path can be relative to `tool_agent.py` (e.g., `..` for the project root) or absolute. **Note**: Currently, `ListDirectoryTool` and `ReadFileTool` internally define their sandbox relative to their own file location (effectively the project root). Future updates will make them fully utilize this config setting.
    -   `MAX_FILE_READ_CHARS`: Maximum number of characters `ReadFileTool` will read from a file (e.g., `2000`).

### Available Tools

Tools are located as individual Python files in the `agential_framework_env_alt/tools/` directory. Each tool provides a name and a description of its capabilities and expected parameters. The agent dynamically loads these tools when it starts.

Currently implemented tools:
-   **`CalculatorTool`**: Evaluates basic arithmetic expressions (e.g., "2 + 3 * 4", "100 / 5").
-   **`GetCurrentDateTool`**: Returns the current date and time.
-   **`ListDirectoryTool`**: Lists contents (files and subdirectories) of a directory. Expects a path relative to the project root (e.g., '.', 'agential_framework_env_alt/tools'). It's sandboxed to prevent listing outside the project area based on its own file location.
-   **`ReadFileTool`**: Reads the initial content of a specified text file. Expects a path relative to the project root. Sandboxed to the project area (based on its own file location) and reads up to `MAX_FILE_READ_CHARS` (configurable in `tool_agent_config.ini`).

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

For tools performing file system operations, they currently define a sandbox root relative to their own location. Future enhancements aim to have them utilize the `PROJECT_SANDBOX_DIR` from `tool_agent_config.ini` for more centralized control. If your tool requires specific configuration values (like `ReadFileTool` using `MAX_FILE_READ_CHARS`), the `tool_agent.py`'s `load_tools()` function needs to be aware of your tool to pass these parameters during its instantiation.

## Other Scripts
(Content remains the same)

---
This README will be updated as new features are added to the Agential Firework project.
