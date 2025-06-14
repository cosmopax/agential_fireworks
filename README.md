# Agential Firework

## Overview

Agential Firework is a project aimed at creating a powerful, private, and extensible AI development environment. It facilitates the setup and use of local Large Language Models (LLMs) and Retrieval Augmented Generation (RAG) agents. This project provides scripts to set up the environment on both macOS (CPU-only) and Ubuntu (with NVIDIA GPU support).

## Directory Structure

A brief overview of the important directories:

-   `agential_framework_env_alt/`: This directory is central to the Python-based agent framework. It contains:
    -   Agent scripts like `rag_agent.py` (for document retrieval) and `tool_agent.py` (for using tools).
    -   Configuration files (e.g., `rag_config.ini` for the RAG agent, `tool_agent_config.ini` for the Tool-agent).
    -   The `core_logic/` subdirectory for shared agent functionalities (e.g., `rag_core.py`).
    -   The `tools/` subdirectory for pluggable tools.
    -   The Python virtual environment (`venv/`) created by the setup scripts.
-   `agential_framework_env_alt/tools/`: Contains individual tool modules (e.g., `calculator_tool.py`, `get_date_tool.py`, `list_directory_tool.py`, `read_file_tool.py`, `write_file_tool.py`, `make_directory_tool.py`, `save_content_tool.py`, `web_search_tool.py`, `query_local_docs_tool.py`, `help_tool.py`, `python_interpreter_tool.py`, `get_process_list_tool.py`) that can be used by `tool_agent.py`. Each tool should inherit from `BaseTool`.
-   `llama_cpp_bin/`: Stores compiled binaries for `llama.cpp` (`llama_main`, `llama_server`). Created by setup scripts.
-   `llama.cpp/`: Contains the source code for `llama.cpp` (cloned by setup scripts).
-   `models/`: This is where you should place your GGUF model files. This directory needs to be created manually or by the setup scripts if adapted.
-   `text_generation_webui_install/`: (On Ubuntu) Contains the installation for `text-generation-webui` if installed using the provided script.

## Setup Instructions

Choose the setup script appropriate for your operating system. The setup scripts have been updated to include all necessary base dependencies for the core agents and tools, including libraries like `duckduckgo-search` (for `WebSearchTool`) and `psutil` (for `GetProcessListTool`). For specific API-dependent tools (e.g., Tavily-based web search), you'll need to configure API keys separately in `tool_agent_config.ini`.

### macOS (CPU-Only Setup)
(Content remains the same - refers to running the script)

### Ubuntu (NVIDIA GPU Setup)
(Content remains the same - refers to running the script)

## Configuration (`rag_config.ini`)

The `rag_agent.py` script uses its dedicated configuration file named `rag_config.ini`, located in the `agential_framework_env_alt/` directory. If this file is not found when the `rag_agent.py` script is run, a default one will be created. You should review and edit this file to suit your RAG agent setup.

The settings are:

-   `[Paths]`
    -   `DOCUMENTS_PATH`: Absolute path to the folder containing your local documents (supports `.txt`, `.md`, and `.pdf` files) for the RAG agent.
    -   `CHROMA_DB_PATH`: Path to the Chroma vector database, relative to `rag_agent.py` if not absolute.
-   `[Models]`
    -   `EMBEDDING_MODEL`: HuggingFace model for embeddings (e.g., `all-MiniLM-L6-v2`).
    -   `LLAMA_SERVER_API_BASE`: URL for the `llama.cpp` server.
    -   `EMBEDDINGS_DEVICE`: Device for embeddings (`auto`, `cuda`, `cpu`).
    -   `RAG_RETRIEVER_K`: (Optional) The number of relevant document chunks the RAG system (used by `QueryLocalDocsTool` and now also by `rag_agent.py` for its core retrieval) should retrieve. Defaults to `3`.
-   `[Conversation]`
    -   `HISTORY_K`: Number of past interactions for RAG agent's conversation memory.

**Important**:
(Content remains the same)

## Using the RAG Agent (`rag_agent.py`)

The RAG agent allows you to chat with your local documents, with answers derived from your content and including source document citations.

### Internal Refactoring
Note: `rag_agent.py` has been refactored to utilize core components (like the document retriever and LLM for RAG) from the centralized `RAGSystem` located in `agential_framework_env_alt/core_logic/`. This ensures consistency in RAG operations across the project (e.g., with `QueryLocalDocsTool`) and makes the system more modular. The agent's interactive features and conversation history management remain within `rag_agent.py`. Its underlying RAG queries will now also respect settings like `RAG_RETRIEVER_K` from `rag_config.ini`.

(Rest of RAG Agent section: Place Documents, Configure, Start llama_server, Run Agent, etc. remains the same)

## Using `text-generation-webui` (Ubuntu with GPU)
(Content remains the same)

## Using the Tool-Using Agent (`tool_agent.py`)

The Tool-Using Agent (`tool_agent.py`) is an experimental agent capable of utilizing a collection of "tools" to answer questions or perform tasks that go beyond the direct knowledge of the LLM.

### Overview
(Content remains the same)

#### Tool Error Handling
(Content remains the same)

#### Sequential Tool Execution (Chaining)
(Content remains the same)

### Configuration (`tool_agent_config.ini`)
(Content remains the same)

### Available Tools

*Note on Tool Dependencies*: Some tools have specific Python library dependencies (e.g., `WebSearchTool (DuckDuckGo)` uses `duckduckgo-search`, `GetProcessListTool` uses `psutil`). These are included in the main project setup scripts. Ensure the environment is set up correctly for all tools to be available. Some tools like `WebSearchTool` also require an active internet connection, and `QueryLocalDocsTool` requires the RAG database to be built by `rag_agent.py` first.

Currently implemented tools:
-   **`CalculatorTool`**: Evaluates basic arithmetic expressions.
-   **`GetCurrentDateTool`**: Returns the current date and time.
-   **`HelpTool`**: Provides information about available tools.
    -   Input: Can be a specific tool name (e.g., "CalculatorTool") to get detailed help for that tool.
    -   Input: If left empty or if "all" or "list" is provided, it lists all available tools and their brief descriptions.
-   **`ListDirectoryTool`**: Lists contents of a directory relative to `PROJECT_SANDBOX_DIR`.
-   **`MakeDirectoryTool`**: Creates a directory relative to `PROJECT_SANDBOX_DIR`.
-   **`PythonInterpreterTool`**: (Experimental & Restricted) Executes a provided snippet of Python code in a highly restricted environment.
    -   **Input**: A short string of Python code (e.g., `data = {{\"key\": \"value\"}}; import json; print(json.dumps(data))`).
    -   **Purpose**: Intended for simple calculations, data manipulations (lists, dicts), or basic logic.
    -   **Output**: The tool indicates if the output is a `(JSON String)` or `(Text)`. It returns the captured standard output (stdout) or an error message.
    -   **Restrictions**: CANNOT perform file system operations, network requests, or import most libraries (only `math` and `random` are available alongside very limited built-ins). Execution is time-limited.
    -   **WARNING**: This tool is powerful. Use with caution.
-   **`QueryLocalDocsTool`**: Queries local document database (uses `RAGSystem` from `core_logic`). Requires RAG DB to be built.
-   **`ReadFileTool`**: Reads content of a file relative to `PROJECT_SANDBOX_DIR`, up to `MAX_FILE_READ_CHARS`.
-   **`SaveContentTool`**: Saves text content to a file relative to `PROJECT_SANDBOX_DIR`. (Specialized `WriteFileTool`).
-   **`WriteFileTool`**: Writes/overwrites a file relative to `PROJECT_SANDBOX_DIR`. Cannot create directories. **Use with extreme caution.**
-   **`GetProcessListTool`**: Lists currently running processes on the system, showing details like PID, name, username, CPU%, and Memory%. It takes no input parameters. The output is a sample of processes (up to a default limit of 25) and may be truncated. Requires the `psutil` library (installed by setup scripts).
-   **`WebSearchTool (DuckDuckGo)`**: Performs a web search via DuckDuckGo. Requires internet.
-   **`WebSearchTool (Tavily)`**: Alternative web search via Tavily (needs API key). Requires internet.


The agent will list all successfully loaded tools upon startup.

### Running the Agent
(Content remains the same)

### Extending with New Tools
(Content remains the same)

## Other Scripts

-   **`download_deps_for_linux.sh`**:
    *   Run on macOS or another machine with internet to download Linux Python packages for offline transfer to your Ubuntu machine. The script has been updated to include new dependencies like `duckduckgo-search` and `psutil`.
    *   Creates an `offline_pip_cache_for_linux` directory.
    *   See script comments for usage on the Ubuntu side.

---
This README will be updated as new features are added to the Agential Firework project.
