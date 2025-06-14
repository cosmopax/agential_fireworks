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
-   `agential_framework_env_alt/tools/`: Contains individual tool modules (e.g., `calculator_tool.py`, `get_date_tool.py`, `list_directory_tool.py`, `read_file_tool.py`, `write_file_tool.py`, `make_directory_tool.py`, `save_content_tool.py`, `web_search_tool.py`, `query_local_docs_tool.py`, `help_tool.py`, `python_interpreter_tool.py`) that can be used by `tool_agent.py`. Each tool should inherit from `BaseTool`.
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

This agent works by:
1.  Receiving a query from the user.
2.  Consulting an LLM, providing it with the user's query, conversation history, and a list of available tools.
3.  The LLM then decides if a tool is appropriate.
    - If so, it specifies which tool to use and the input (parameters) for that tool. It can also plan a sequence of up to two tools.
    - If not, the LLM provides a direct answer.
4.  If a tool (or a sequence of tools) is chosen, the agent executes it/them.
5.  For single tool usage, or after the final tool in a sequence, the output from the last tool is passed back to the LLM (along with the original query and history).
6.  The LLM synthesizes this information into a final, natural language response for the user.
If no tool was chosen initially, the LLM's direct answer from step 3 is provided to the user.

#### Tool Error Handling
If a tool encounters an error during its execution (e.g., invalid parameters, file not found, calculation error), it will return an error message. The Tool-Using Agent is designed to recognize these errors. Instead of trying to use the error message as a successful result, the agent will inform the LLM that the tool operation failed (by passing a "Tool Status: error" and the error message). The LLM will then attempt to explain this error to you in a user-friendly way and may suggest alternative actions. This makes the agent more robust and transparent when tools don't perform as expected.

#### Sequential Tool Execution (Chaining)
The agent can execute a sequence of up to two tools to fulfill more complex requests. The LLM can plan this sequence. For instance, it might decide to first use one tool (e.g., `WebSearchTool`) and then use its output as input for a second tool (e.g., `SaveContentTool`). When planning a two-step sequence, the LLM can use the placeholder `{{PREVIOUS_TOOL_OUTPUT}}` in the parameters for the second tool, which the agent will replace with the actual output from the first tool. The `{{PREVIOUS_TOOL_OUTPUT}}` placeholder is replaced with the literal string output of the first tool. If this output is multi-line or contains special characters, the LLM should be mindful of this when constructing the parameters for the second tool to ensure correct parsing by that tool.

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
-   **`PythonInterpreterTool`**: (Experimental & Restricted) Executes a provided snippet of Python code in a highly restricted environment.
    -   **Input**: A short string of Python code.
    -   **Purpose**: Intended for simple calculations, list/dictionary manipulations, or basic logic that is too complex for other tools.
    -   **Restrictions**: CANNOT perform file system operations, network requests, or import most libraries (only `math` and `random` are available alongside very limited built-ins). Execution is time-limited (e.g., a few seconds).
    -   **Output**: The captured standard output (stdout) of the code or an error message.
    -   **WARNING**: This tool is powerful and, despite restrictions, should be used with caution. It's designed for LLM-generated code snippets for benign tasks. Avoid enabling or using this tool if you have concerns about code execution risks.

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
