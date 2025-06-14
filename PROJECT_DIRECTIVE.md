# PROJECT_DIRECTIVE.md: Agential Firework

### A. Mission & Core Objective
- **Mission:** To establish a robust, private, and extensible development environment for Artificial Intelligence, simplifying the setup and utilization of local Large Language Models (LLMs) and advanced Retrieval Augmented Generation (RAG) agents.
- **Current Success Criteria:** A functional local AI development environment with setup scripts for both macOS and Ubuntu. Core capabilities include a RAG agent for querying local documents and a Tool Agent with a suite of foundational tools, both interacting with a locally hosted LLM via `llama.server`.
- **Future Success Criteria:** An enhanced, more robust framework with improved tool integration, simplified configuration management, comprehensive user documentation, and a full suite of automated tests.

### B. Project Layout & Current State
- **`agential_framework_env_alt/`**: Core Python agent framework.
    - Agents: `rag_agent.py`, `tool_agent.py`
    - Configs: `rag_config.ini`, `tool_agent_config.ini`
    - Shared Logic: `core_logic/`
    - Tools: `tools/`
    - Environment: `venv/`
- **`llama.cpp/`**: Source code for the `llama.cpp` library.
- **`llama_cpp_bin/`**: Compiled `llama.cpp` binaries (`llama_main`, `llama_server`).
- **`models/`**: Directory for GGUF model files.
- **`text_generation_webui_install/`**: (Ubuntu) Optional installation of `text-generation-webui`.

### C. Technical & Resource Stack
- **Languages & Core Technologies:** Python 3, Shell Scripting (Bash/Zsh).
- **Core Libraries & Frameworks:** `llama.cpp` for LLM inference.
- **Python Dependencies:** `psutil`, `duckduckgo-search`, `tavily-python`, and others as specified in setup scripts.
- **Key Components:**
    - `llama_server` as the LLM backend API.
    - `RAGSystem` in `core_logic` for document retrieval.
    - Modular `BaseTool` structure for `tool_agent.py`.
- **Target Platforms:** macOS (CPU-only, Zsh/Homebrew), Ubuntu (NVIDIA GPU recommended, APT).

### D. Task Decomposition
#### Completed Milestones
- [x] **Setup Automation:** Develop setup scripts (`setup_macos.sh`, `setup_ubuntu.sh`) for dependencies and compilation.
- [x] **LLM Integration:** Integrate `llama.cpp` and establish the `llama_server` workflow.
- [x] **RAG Agent Development:** Create the initial `rag_agent.py` with `rag_config.ini` and core logic.
- [x] **Tool Agent Framework:** Develop the initial `tool_agent.py` capable of loading and using tools.
- [x] **Initial Tool Suite:** Implement a foundational set of tools (Filesystem, Web Search, System, etc.).

#### Next Steps & Future Roadmap
- [ ] **Phase 1: Refinement & Hardening**
    - [ ] **Tool Enhancement:** Harden the experimental `PythonInterpreterTool` with more robust sandboxing and clear limitations.
    - [ ] **Error Handling:** Improve global error handling within both the RAG and Tool agents to be more descriptive and resilient.
    - [ ] **Configuration Management:** Develop a script or a TUI (Text-based User Interface) tool to guide users through editing the `.ini` configuration files, reducing manual errors.
- [ ] **Phase 2: Testing & Validation**
    - [ ] **Unit Tests:** Develop a suite of `pytest` unit tests for each tool in the `tools/` directory.
    - [ ] **Integration Tests:** Create integration tests that verify the full loop of agent-to-tool and agent-to-LLM communication.
    - [ ] **CI/CD Pipeline:** Set up a basic GitHub Actions workflow to automatically run tests on push/pull request.
- [ ] **Phase 3: Documentation**
    - [ ] **User Guide:** Create a comprehensive `USER_GUIDE.md` in a new `docs/` directory, explaining setup, configuration, and agent execution for non-developers.
    - [ ] **Developer Guide:** Create a `DEVELOPER_GUIDE.md` explaining how to create and integrate new tools into the framework.
    - [ ] **API Documentation:** Add detailed docstrings to all Python functions and classes.
- [ ] **Phase 4: Feature Expansion**
    - [ ] **Conversational Tool Use:** Enhance the Tool Agent to allow for more natural, conversational interaction instead of single-shot commands.
    - [ ] **New High-Value Tools:** Design and implement more complex tools (e.g., a tool for Git operations, a database interaction tool).
    - [ ] **Alternative LLM Backends:** Refactor the LLM communication logic to allow for easy integration of other backends besides `llama_server` (e.g., Ollama, OpenAI API).

### E. Constraints & Preferences
- **Privacy First & Local Execution:** The primary mode of operation must always be with locally hosted models. Any tool requiring internet access (e.g., WebSearch) must be explicitly enabled by the user.
- **Extensible by Design:** The architecture must remain modular to facilitate easy addition of new tools and capabilities.
- **Sandboxed File Operations:** All tools that interact with the filesystem (`ReadFileTool`, `WriteFileTool`, etc.) MUST be strictly limited to the `PROJECT_SANDBOX_DIR` defined in the configuration.
- **Cautious Tool Use:** Tools marked as "Experimental" or with a high potential for system impact (`PythonInterpreterTool`, `WriteFileTool`) must log prominent warnings upon use.

### F. Autonomy Protocol
- **Role:** You are to act as a senior-level Python developer and AI systems architect.
- **Proactivity:** Proceed through the "Next Steps" tasks autonomously. When a task like "Develop a suite of `pytest` unit tests" is given, execute all logical sub-steps (creating test files, writing tests for each tool, providing run commands) without further prompting.
- **Library/Tool Selection:** When a new library is needed (e.g., for the configuration TUI), research open-source options (like `rich` or `questionary`), select the best fit based on documentation and ease of use, state your choice, and proceed.
- **Error Handling:** If code you generate fails, autonomously attempt to debug it up to two times. If still unresolved, present the original code, the error, all attempted fixes, and your analysis of the root cause, along with at least two paths forward.
- **Ambiguity Resolution:** If a requirement is ambiguous (e.g., the exact format for the User Guide), create a logical and professional-looking structure, state your choice, and proceed. Flag the choice for my later review.
- **End-of-Response Summary:** Conclude every major response with a status update: `[Task XYZ Complete]`, `[Blocked, Awaiting Input]`, or `[Ready for Next Phase]`.
