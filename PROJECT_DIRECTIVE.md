## Project Overview: Agential Firework

Agential Firework is a project dedicated to establishing a robust, private, and extensible development environment for Artificial Intelligence. The core aim is to simplify the setup and utilization of local Large Language Models (LLMs) and advanced Retrieval Augmented Generation (RAG) agents. This initiative provides comprehensive setup scripts tailored for both macOS (CPU-only) and Ubuntu (with NVIDIA GPU support) environments, facilitating a broad adoption for AI development and experimentation.

## Directory Structure

The project is organized into several key directories:

-   `agential_framework_env_alt/`: The core of the Python-based agent framework. It houses agent scripts (e.g., `rag_agent.py`, `tool_agent.py`), configuration files (e.g., `rag_config.ini`, `tool_agent_config.ini`), the `core_logic/` subdirectory for shared functionalities, the `tools/` subdirectory for pluggable tools, and the Python virtual environment (`venv/`).
-   `llama.cpp/`: Contains the source code for the `llama.cpp` library, used for running LLMs locally.
-   `llama_cpp_bin/`: Stores the compiled binaries for `llama.cpp` (e.g., `llama_main`, `llama_server`), created by the setup scripts.
-   `models/`: Designated directory for storing GGUF model files. This directory needs to be created manually or by adapted setup scripts.
-   `text_generation_webui_install/`: (Ubuntu specific) Contains the installation for the `text-generation-webui` if installed via the provided script.
-   `docs/`: (If it exists or is planned) Intended for user documentation, guides, and detailed explanations of components.
-   `scripts/` or `setup_scripts/`: (If setup scripts are consolidated) Would contain all setup-related shell scripts (`setup_macos.sh`, `setup_ubuntu.sh`, `download_deps_for_linux.sh`).

## Agential Framework

The heart of Agential Firework is its Python-based agential framework, located within the `agential_framework_env_alt/` directory. This framework is designed for modularity and extensibility, supporting sophisticated AI agent development.

Key components include:

-   **RAG Agent (`rag_agent.py`):** Enables conversational interaction with a local document corpus.
    -   Utilizes `rag_config.ini` for configuration (document paths, embedding models, etc.).
    -   Leverages the `RAGSystem` from `core_logic/` for core document retrieval and generation, ensuring consistency across the project.
    -   Manages conversation history and user interaction.

-   **Tool Agent (`tool_agent.py`):** An experimental agent capable of using a suite of tools to perform tasks and answer questions beyond the LLM's intrinsic knowledge.
    -   Configured via `tool_agent_config.ini` (LLM settings, tool enablement, API keys).
    -   Features include error handling for tools and sequential tool execution (chaining).

-   **Core Logic (`core_logic/`):** Contains shared Python modules and functionalities, such as `rag_core.py`, which centralizes the RAG operations for both the RAG agent and the `QueryLocalDocsTool`.

-   **Tools (`tools/`):** A collection of pluggable Python modules, each representing a distinct capability that the Tool Agent can leverage. Each tool typically inherits from a `BaseTool` class.

-   **Configuration Files:**
    -   `rag_config.ini`: Specific to the RAG Agent, defining paths for documents and the vector database, embedding model details, and conversation parameters.
    -   `tool_agent_config.ini`: For the Tool Agent, specifying LLM server details, API keys for certain tools (e.g., Tavily Web Search), and sandbox directory settings.

-   **Python Virtual Environment (`venv/`):** An isolated Python environment created by the setup scripts to manage project-specific dependencies.

## Available Tools for Tool Agent

The Tool Agent (`tool_agent.py`) can utilize a variety of tools to extend its capabilities. These tools are located in the `agential_framework_env_alt/tools/` directory. Some tools may require specific dependencies (installed by setup scripts) or network access.

-   **`CalculatorTool`**: Evaluates basic arithmetic expressions.
-   **`GetCurrentDateTool`**: Returns the current date and time.
-   **`HelpTool`**: Provides information about available tools. Can list all tools or give detailed help for a specific tool.
-   **`ListDirectoryTool`**: Lists contents of a specified directory relative to a defined project sandbox directory (`PROJECT_SANDBOX_DIR`).
-   **`MakeDirectoryTool`**: Creates a new directory relative to `PROJECT_SANDBOX_DIR`.
-   **`PythonInterpreterTool`**: (Experimental & Restricted) Executes simple Python code snippets in a highly restricted environment. Limited library access (e.g., `math`, `random`). **Use with caution.**
-   **`QueryLocalDocsTool`**: Queries the local document database built by the RAG Agent, utilizing the shared `RAGSystem` from `core_logic/`. Requires the RAG database to be populated first.
-   **`ReadFileTool`**: Reads the content of a specified file relative to `PROJECT_SANDBOX_DIR`, with a maximum character limit.
-   **`SaveContentTool`**: Saves provided text content to a specified file relative to `PROJECT_SANDBOX_DIR`. (A specialized version of `WriteFileTool`).
-   **`WriteFileTool`**: Writes or overwrites content to a specified file relative to `PROJECT_SANDBOX_DIR`. Does not create directories. **Use with extreme caution.**
-   **`GetProcessListTool`**: Lists currently running processes on the system, showing details like PID, name, CPU%, and Memory%. Requires the `psutil` library.
-   **`WebSearchTool (DuckDuckGo)`**: Performs web searches using DuckDuckGo. Requires an internet connection and the `duckduckgo-search` library.
-   **`WebSearchTool (Tavily)`**: An alternative web search tool using the Tavily API. Requires an internet connection and a Tavily API key configured in `tool_agent_config.ini`.

The Tool Agent lists all successfully loaded tools upon startup.

## Local LLM Integration

A core feature of Agential Firework is its ability to run Large Language Models (LLMs) locally, ensuring privacy and control over AI capabilities.

-   **`llama.cpp`**: The project utilizes the `llama.cpp` library for efficient LLM inference.
    -   The source code for `llama.cpp` is included in the `llama.cpp/` directory and is typically cloned during the setup process.
    -   Compiled binaries (e.g., `llama_main` for direct interaction, `llama_server` for providing an API endpoint) are placed in the `llama_cpp_bin/` directory by the setup scripts.
    -   The `llama_server` is crucial for the RAG and Tool agents, which communicate with the LLM via its API (default: `http://127.0.0.1:8080/completion`).

-   **Models (`models/` directory):**
    -   This directory is the designated location for storing LLM model files, typically in the GGUF (GPT-Generated Unified Format).
    -   Users need to procure and place their desired GGUF-compatible models in this directory. The setup scripts may create this directory if it doesn't exist, but model acquisition is manual.

-   **`text-generation-webui` (Optional, Ubuntu with GPU):**
    -   For users on Ubuntu with NVIDIA GPUs, the project provides an option to install `text-generation-webui` (located in `text_generation_webui_install/`).
    -   This offers a comprehensive web interface for interacting with various LLMs, managing models, and experimenting with different generation parameters. It can serve as an alternative or complementary way to interact with local LLMs alongside the project's agents.

## Setup and Execution

The project provides scripts to streamline the setup process on supported operating systems.

-   **Setup:**
    -   **macOS (CPU-Only):** Run `setup_macos.sh` to install dependencies, clone `llama.cpp`, build it, and set up the Python virtual environment.
    -   **Ubuntu (NVIDIA GPU Recommended):** Run `setup_ubuntu.sh` for a similar setup, with added support for NVIDIA GPU acceleration for `llama.cpp` and an option to install `text-generation-webui`.
    -   **Offline Dependencies:** The `download_deps_for_linux.sh` script can be used to download Python packages on a machine with internet access for offline transfer to a Linux environment.
    -   All necessary base dependencies for core agents and tools (like `duckduckgo-search`, `psutil`) are included in these setup scripts.

-   **Execution:**
    1.  **Place LLM Models:** Ensure your GGUF model files are in the `models/` directory.
    2.  **Configure Agents:**
        -   Review and edit `agential_framework_env_alt/rag_config.ini` for the RAG Agent (document paths, embedding models, etc.). A default file is created if missing.
        -   Review and edit `agential_framework_env_alt/tool_agent_config.ini` for the Tool Agent (LLM server endpoint, API keys for tools like Tavily, sandbox directory). A default is also created if missing.
    3.  **Start `llama_server`:**
        -   Navigate to the `llama_cpp_bin/` directory (or where your `llama_server` binary is).
        -   Run the server, pointing it to your chosen model. Example: `./llama_server -m ../models/your_model.gguf -c 2048 --host 0.0.0.0 --port 8080`. Adjust parameters as needed.
    4.  **Run Agents:**
        -   Activate the Python virtual environment: `source agential_framework_env_alt/venv/bin/activate`.
        -   **RAG Agent:** Navigate to `agential_framework_env_alt/` and run `python rag_agent.py`. The first run might involve building the document database.
        -   **Tool Agent:** Navigate to `agential_framework_env_alt/` and run `python tool_agent.py`. It will list loaded tools on startup.
    5.  **(Optional) Use `text-generation-webui`:** If installed on Ubuntu, run its `start_linux.sh` script.

## Extensibility

Agential Firework is designed with extensibility in mind, particularly concerning the capabilities of the Tool Agent.

-   **Adding New Tools:** The primary way to extend the framework is by creating new tools for the `tool_agent.py`.
    -   New tool classes should be created within the `agential_framework_env_alt/tools/` directory.
    -   Each tool should ideally inherit from the `BaseTool` class (if one exists, or follow a similar structural pattern).
    -   The tool needs to implement specific methods for its operation (e.g., an `execute` method).
    -   The `tool_agent.py` is designed to automatically discover and load tools placed in the `tools/` directory, making integration straightforward.
    -   Ensure any new dependencies for tools are managed, potentially by updating setup scripts or requirements files.

-   **Modifying Agents:** The RAG and Tool agents themselves can be modified or extended. Their modular design, especially the separation of core logic (like `RAGSystem`), facilitates enhancements or alterations to their behavior.

-   **Integrating Different LLMs/Backends:** While currently focused on `llama.cpp`, the agent configurations could be adapted to point to different LLM serving backends or APIs with modifications to the communication logic within the agents.

## Conclusion

Agential Firework provides a comprehensive platform for developing and experimenting with local LLMs and AI agents. Its focus on privacy, local execution, and extensibility makes it a valuable asset for AI practitioners and researchers seeking to build custom AI-powered applications. This directive outlines its current state and capabilities, serving as a guide for users and developers.
