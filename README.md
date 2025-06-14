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
-   `agential_framework_env_alt/tools/`: Contains individual tool modules (e.g., `calculator_tool.py`, `get_date_tool.py`, `list_directory_tool.py`, `read_file_tool.py`, `write_file_tool.py`, `make_directory_tool.py`, `save_content_tool.py`, `web_search_tool.py`, `query_local_docs_tool.py`, `help_tool.py`) that can be used by `tool_agent.py`. Each tool should inherit from `BaseTool`.
-   `llama_cpp_bin/`: Stores compiled binaries for `llama.cpp` (`llama_main`, `llama_server`). Created by setup scripts.
-   `llama.cpp/`: Contains the source code for `llama.cpp` (cloned by setup scripts).
-   `models/`: This is where you should place your GGUF model files. This directory needs to be created manually or by the setup scripts if adapted.
-   `text_generation_webui_install/`: (On Ubuntu) Contains the installation for `text-generation-webui` if installed using the provided script.

## Setup Instructions

Choose the setup script appropriate for your operating system. The setup scripts have been updated to include all necessary base dependencies for the core agents and tools, including `duckduckgo-search` for the `WebSearchTool`. For specific API-dependent tools like `WebSearchTool` (using Tavily), you'll need to configure API keys separately.

### macOS (CPU-Only Setup)
(Content remains the same - refers to running the script)

### Ubuntu (NVIDIA GPU Setup)
(Content remains the same - refers to running the script)

## Configuration (`rag_config.ini`)

The `rag_agent.py` script uses its dedicated configuration file named `rag_config.ini`, located in the `agential_framework_env_alt/` directory. If this file is not found when the `rag_agent.py` script is run, a default one will be created. You should review and edit this file to suit your RAG agent setup.

The settings are:

-   `[Paths]`
    -   `DOCUMENTS_PATH`: Absolute path to the folder containing your local documents (supports `.txt`, `.md`, and `.pdf` files) for the RAG agent. Example: `/path/to/your/documents` or `C:\Users\YourName\Documents\ResearchPapers`.
    -   `CHROMA_DB_PATH`: Path to the Chroma vector database. If relative (e.g., `./chroma_db_local_docs`), it's relative to the `rag_agent.py` script itself.
-   `[Models]`
    -   `EMBEDDING_MODEL`: The name of the HuggingFace sentence transformer model to use for embeddings (e.g., `all-MiniLM-L6-v2`).
    -   `LLAMA_SERVER_API_BASE`: The base URL for the `llama.cpp` server's OpenAI-compatible API (e.g., `http://127.0.0.1:8080/v1`). This is used by the RAG agent.
    -   `EMBEDDINGS_DEVICE`: Specifies the device for calculating embeddings (used by RAG agent). Options: `auto`, `cuda`, `cpu`.
    -   `RAG_RETRIEVER_K`: (Optional) The number of relevant document chunks the RAG system should retrieve from the vector database for context. Defaults to `3` if not specified or invalid.
-   `[Conversation]`
    -   `HISTORY_K`: The number of past user/AI interaction pairs to keep in conversation memory for the RAG agent (e.g., `3`).

**Important**:
(Content remains the same)

## Using the RAG Agent (`rag_agent.py`)
(Content remains the same)

## Using `text-generation-webui` (Ubuntu with GPU)
(Content remains the same)

## Using the Tool-Using Agent (`tool_agent.py`)

The Tool-Using Agent (`tool_agent.py`) is an experimental agent capable of utilizing a collection of "tools" to answer questions or perform tasks that go beyond the direct knowledge of the LLM.

### Overview
(Content remains the same)

#### Sequential Tool Execution (Chaining)
(Content remains the same)

### Configuration (`tool_agent_config.ini`)
(Content remains the same)

### Available Tools

Tools are located as individual Python files in the `agential_framework_env_alt/tools/` directory. Each tool provides a name and a description of its capabilities and expected parameters. The agent dynamically loads these tools when it starts.

Currently implemented tools:
-   **`CalculatorTool`**: Evaluates basic arithmetic expressions.
-   **`GetCurrentDateTool`**: Returns the current date and time.
-   **`ListDirectoryTool`**: Lists contents of a directory relative to `PROJECT_SANDBOX_DIR`.
-   **`ReadFileTool`**: Reads content of a file relative to `PROJECT_SANDBOX_DIR`, up to `MAX_FILE_READ_CHARS`.
-   **`WriteFileTool`**: Writes/overwrites a file relative to `PROJECT_SANDBOX_DIR`. Cannot create directories.
-   **`MakeDirectoryTool`**: Creates a directory relative to `PROJECT_SANDBOX_DIR`.
-   **`SaveContentTool`**: Saves text content to a file relative to `PROJECT_SANDBOX_DIR`. (Specialized `WriteFileTool`).
-   **`WebSearchTool (DuckDuckGo)`**: Performs a web search via DuckDuckGo. Requires internet.
-   **`WebSearchTool (Tavily)`**: Alternative web search via Tavily (needs API key). Requires internet.
-   **`QueryLocalDocsTool`**: Queries local document database (uses `RAGSystem` from `core_logic`). Requires RAG DB to be built.
-   **`HelpTool`**: Provides information about available tools.
    -   Input: Can be a specific tool name (e.g., "CalculatorTool") to get detailed help for that tool.
    -   Input: If left empty or if "all" or "list" is provided, it lists all available tools and their brief descriptions.
    This tool helps in understanding what other tools can do.

The agent will list all successfully loaded tools upon startup.
*Note: Some tools like `WebSearchTool` require an active internet connection to function. The `QueryLocalDocsTool` requires the RAG database to be built by `rag_agent.py` first.*

### Running the Agent
(Content remains the same)

### Extending with New Tools
(Content remains the same)

## Other Scripts
(Content remains the same)

---
This README will be updated as new features are added to the Agential Firework project.
