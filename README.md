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
-   `agential_framework_env_alt/tools/`: Contains individual tool modules (e.g., `calculator_tool.py`, `get_date_tool.py`, `list_directory_tool.py`, `read_file_tool.py`, `write_file_tool.py`, `make_directory_tool.py`, `web_search_tool.py`, `query_local_docs_tool.py`) that can be used by `tool_agent.py`. Each tool should inherit from `BaseTool`.
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
(Content remains the same)

## Using the RAG Agent (`rag_agent.py`)
(Content remains the same)

## Using `text-generation-webui` (Ubuntu with GPU)
(Content remains the same)

## Using the Tool-Using Agent (`tool_agent.py`)

The Tool-Using Agent (`tool_agent.py`) is an experimental agent capable of utilizing a collection of "tools" to answer questions or perform tasks that go beyond the direct knowledge of the LLM.

### Overview
(Content remains the same)

### Configuration (`tool_agent_config.ini`)
(Content remains the same, including Tavily API key note)

### Available Tools

Tools are located as individual Python files in the `agential_framework_env_alt/tools/` directory. Each tool provides a name and a description of its capabilities and expected parameters. The agent dynamically loads these tools when it starts.

Currently implemented tools:
-   **`CalculatorTool`**: Evaluates basic arithmetic expressions (e.g., "2 + 3 * 4", "100 / 5").
-   **`GetCurrentDateTool`**: Returns the current date and time.
-   **`ListDirectoryTool`**: Lists contents (files and subdirectories) of a specified directory. Path must be relative to the configured `PROJECT_SANDBOX_DIR`.
-   **`ReadFileTool`**: Reads the initial content of a specified text file. Path must be relative to the `PROJECT_SANDBOX_DIR`. Reads up to `MAX_FILE_READ_CHARS`.
-   **`WriteFileTool`**: Writes or overwrites a text file with specified content. Input format: `'[relative_file_path]|[content_to_write]'`. Path must be relative to `PROJECT_SANDBOX_DIR`. This tool cannot create new directories; the target directory must already exist. **Use with extreme caution as it can overwrite files.**
-   **`MakeDirectoryTool`**: Creates a new directory (including any necessary parent directories if they are within the sandbox). Path must be relative to `PROJECT_SANDBOX_DIR`. Succeeds without error if the directory already exists.
-   **`WebSearchTool (DuckDuckGo)`**: Performs a web search using DuckDuckGo and returns a summary of the top search results (typically 3). Input should be the search query string. Useful for finding current information or topics not covered by local knowledge. Requires an internet connection. (Note: This tool uses the `duckduckgo-search` library. For more extensive search needs, the Tavily-based search below might be preferred if an API key is available.)
-   **`WebSearchTool (Tavily)`**: (Alternative to DuckDuckGo search if `TAVILY_API_KEY` is set) Performs a web search using the Tavily AI service to find up-to-date information. Expects a search query string as input. Requires a Tavily API key to be configured in `tool_agent_config.ini`.
-   **`QueryLocalDocsTool`**: Queries the pre-existing local knowledge base of documents (created and managed by `rag_agent.py` and its `rag_config.ini`) for specific information. Input should be the question or topic to search for within the local documents. This tool is read-only and relies on an already indexed document database; it will report an error if the database is not found or not initialized correctly.

The agent will list all successfully loaded tools upon startup.
*Note: Some tools like `WebSearchTool` require an active internet connection to function. The `QueryLocalDocsTool` requires the RAG database to be built by `rag_agent.py` first.*

### Running the Agent
(Content remains the same)

### Extending with New Tools
(Content remains the same)

## Other Scripts

-   **`download_deps_for_linux.sh`**:
    *   Run on macOS or another machine with internet to download Linux Python packages for offline transfer to your Ubuntu machine. The script has been updated to include new dependencies like `duckduckgo-search`.
    *   Creates an `offline_pip_cache_for_linux` directory.
    *   See script comments for usage on the Ubuntu side.

---
This README will be updated as new features are added to the Agential Firework project.
