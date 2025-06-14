# agential_framework_env_alt/core_logic/__init__.py
# This file makes Python treat the directory as a package.

# Attempt to import RAGSystem, but don't fail if rag_core doesn't exist yet
# or if RAGSystem isn't defined during initial scaffolding.
try:
    from .rag_core import RAGSystem
    __all__ = ['RAGSystem']
except ImportError:
    print("Warning: core_logic.rag_core or RAGSystem not found during __init__.")
    __all__ = []


print("agential_framework_env_alt.core_logic package loaded.")
