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
-   `agential_framework_env_alt/tools/`: Contains individual tool modules (e.g., `calculator_tool.py`, `get_date_tool.py`, `list_directory_tool.py`, `read_file_tool.py`, `write_file_tool.py`, `make_directory_tool.py`, `save_content_tool.py`, `web_search_tool.py`, `query_local_docs_tool.py`, `help_tool.py`, `python_interpreter_tool.py`, `get_process_list_tool.py`, `file_search_tool.py`) that can be used by `tool_agent.py`. Each tool should inherit from `BaseTool`.
-   `llama_cpp_bin/`: Stores compiled binaries for `llama.cpp` (`llama_main`, `llama_server`). Created by setup scripts.
-   `llama.cpp/`: Contains the source code for `llama.cpp` (cloned by setup scripts).
-   `models/`: This is where you should place your GGUF model files. This directory needs to be created manually or by the setup scripts if adapted.
-   `text_generation_webui_install/`: (On Ubuntu) Contains the installation for `text-generation-webui` if installed using the provided script.
-   `tests/`: Contains unit tests for the framework, primarily for tools.
    -   `tests/tools/`: Contains specific test files for each tool.

## Setup Instructions

Choose the setup script appropriate for your operating system. The setup scripts have been updated to include all necessary base dependencies for the core agents and tools, including libraries like `duckduckgo-search` (for `WebSearchTool`) and `psutil` (for `GetProcessListTool`). For specific API-dependent tools (e.g., Tavily-based web search), you'll need to configure API keys separately in `tool_agent_config.ini`.

### macOS (CPU-Only Setup)
(Content remains the same - refers to running the script)

### Ubuntu (NVIDIA GPU Setup)
(Content remains the same - refers to running the script)

## Configuration (`rag_config.ini`)

The `rag_agent.py` script uses its dedicated configuration file named `rag_config.ini`, located in the `agential_framework_env_alt/` directory. If this file is not found when the `rag_agent.py` script is run, a default one will be created. You should review and edit this file to suit your RAG agent setup.

The settings are:
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
The agent can execute a sequence of up to two tools to fulfill more complex requests. The LLM can plan this sequence. For instance, it might decide to first use one tool (e.g., `WebSearchTool`) and then use its output as input for a second tool (e.g., `SaveContentTool`). When planning a two-step sequence, the LLM can use the placeholder `{{PREVIOUS_TOOL_OUTPUT}}` in the parameters for the second tool, which the agent will replace with the actual output from the first tool. The `{{PREVIOUS_TOOL_OUTPUT}}` placeholder is replaced with the literal string output of the first tool. If this output is multi-line or contains special characters, the LLM should be mindful of this when constructing the parameters for the second tool to ensure correct parsing by that tool.

#### Tool Output Handling (JSON Awareness)
The agent is designed to recognize when a tool's output is structured data. For instance, if `PythonInterpreterTool` executes code that prints a valid JSON string, the agent identifies this. This type information ("json" or "text") is then provided to the LLM during the final response synthesis step, allowing the LLM to make more informed use of the tool's output (e.g., by referring to specific keys in a JSON object). For sequential tool execution, the raw string output (which would be the JSON string itself if applicable) is passed via the `{{PREVIOUS_TOOL_OUTPUT}}` placeholder.

### Configuration (`tool_agent_config.ini`)
(Content remains the same)

### Available Tools

*Note on Tool Dependencies*: Some tools have specific Python library dependencies (e.g., `WebSearchTool (DuckDuckGo)` uses `duckduckgo-search`, `GetProcessListTool` uses `psutil`). These are included in the main project setup scripts. Ensure the environment is set up correctly for all tools to be available. Some tools like `WebSearchTool` also require an active internet connection, and `QueryLocalDocsTool` requires the RAG database to be built by `rag_agent.py` first.

Currently implemented tools:
(Content remains the same)

### Running the Agent
(Content remains the same)

### Extending with New Tools
(Content remains the same)

## Testing the Framework

### Unit Tests

The project uses `pytest` for its unit testing framework. `pytest` is included in the Python dependencies installed by the setup scripts (`setup_macos.sh` and `setup_ubuntu.sh`).

All unit tests are located in the `tests/` directory, with tool-specific tests primarily found under `tests/tools/`. These tests are designed to verify the individual functionality, error handling, and safety mechanisms (like sandboxing for OS tools) of each component.

**Running the Tests:**

1.  Ensure you have set up the development environment by running the appropriate setup script for your OS.
2.  Activate the Python virtual environment:
    ```bash
    source agential_framework_env_alt/venv/bin/activate
    ```
    (Note: On Windows, the activation command would be different, e.g., `agential_framework_env_alt\venv\Scripts\activate`. However, the primary target platforms are macOS and Ubuntu.)
3.  Navigate to the root directory of the `agential_firework` project.
4.  Run pytest:
    ```bash
    pytest
    ```
    Alternatively, you can run it as a module:
    ```bash
    python -m pytest
    ```
This will discover and run all tests in the `tests/` directory and its subdirectories. You should see output indicating the number of tests passed, failed, or skipped.

## Other Scripts
(Content remains the same)

---
This README will be updated as new features are added to the Agential Firework project.
