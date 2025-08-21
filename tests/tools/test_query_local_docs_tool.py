# tests/tools/test_query_local_docs_tool.py
import pytest
from unittest.mock import patch, MagicMock

# Import QueryLocalDocsTool.
from agential_framework_env_alt.tools.query_local_docs_tool import QueryLocalDocsTool

class TestQueryLocalDocsTool:

    @patch('agential_framework_env_alt.tools.query_local_docs_tool.RAGSystem')
    def test_successful_query(self, MockRAGSystem):
        """Test a successful query delegation to RAGSystem."""
        mock_rag_instance = MagicMock()
        mock_rag_instance.is_initialized = True
        mock_rag_instance.error_message = None
        mock_rag_instance.query.return_value = "This is the RAG answer."
        MockRAGSystem.return_value = mock_rag_instance

        QueryLocalDocsTool._rag_system_instance = None
        tool = QueryLocalDocsTool()

        query = "What is the project about?"
        result = tool.execute(query)

        assert result == "This is the RAG answer."
        mock_rag_instance.query.assert_called_once_with(query)
        assert tool.error_message is None

    @patch('agential_framework_env_alt.tools.query_local_docs_tool.RAGSystem')
    def test_ragsystem_initialization_fails(self, MockRAGSystem):
        """Test behavior when the internal RAGSystem fails to initialize."""
        mock_rag_instance = MagicMock()
        mock_rag_instance.is_initialized = False
        mock_rag_instance.error_message = "RAGSystem DB not found."
        MockRAGSystem.return_value = mock_rag_instance

        QueryLocalDocsTool._rag_system_instance = None
        tool = QueryLocalDocsTool()

        # Tool's __init__ should capture the error message
        # The exact message might be composed, so check for key part.
        assert "RAGSystem DB not found." in str(tool.error_message)

        result = tool.execute("any query")
        # The execute method should return the error captured during __init__ or from RAGSystem instance
        assert "RAGSystem DB not found." in result or \
               "RAGSystem not available to QueryLocalDocsTool" in result


    @patch('agential_framework_env_alt.tools.query_local_docs_tool.RAGSystem')
    def test_ragsystem_query_raises_exception(self, MockRAGSystem):
        """Test behavior when RAGSystem.query() raises an exception."""
        mock_rag_instance = MagicMock()
        mock_rag_instance.is_initialized = True
        mock_rag_instance.error_message = None
        mock_rag_instance.query.side_effect = RuntimeError("Simulated RAG query failure")
        MockRAGSystem.return_value = mock_rag_instance

        QueryLocalDocsTool._rag_system_instance = None
        tool = QueryLocalDocsTool()

        result = tool.execute("a query that will cause RAG error")

        # Check for the core part of the error message
        assert "Error querying local documents via QueryLocalDocsTool" in result
        assert "Simulated RAG query failure" in result

    def test_empty_query_string(self):
        """Test providing an empty or whitespace query string."""
        with patch('agential_framework_env_alt.tools.query_local_docs_tool.RAGSystem') as MockRAGSystemMinimal:
            mock_rag_instance_minimal = MagicMock()
            mock_rag_instance_minimal.is_initialized = True
            MockRAGSystemMinimal.return_value = mock_rag_instance_minimal

            QueryLocalDocsTool._rag_system_instance = None
            tool = QueryLocalDocsTool()

            result_empty = tool.execute("")
            assert "Error: Query for local documents cannot be empty." in result_empty

            result_whitespace = tool.execute("   ")
            assert "Error: Query for local documents cannot be empty." in result_whitespace

            mock_rag_instance_minimal.query.assert_not_called()

    def test_tool_properties(self):
        """Test basic properties of the tool."""
        with patch('agential_framework_env_alt.tools.query_local_docs_tool.RAGSystem') as MockRAGSystemForProps:
            mock_rag_instance_props = MagicMock()
            mock_rag_instance_props.is_initialized = True
            MockRAGSystemForProps.return_value = mock_rag_instance_props

            QueryLocalDocsTool._rag_system_instance = None
            tool = QueryLocalDocsTool()

            assert tool.name == "QueryLocalDocsTool"
            assert "Queries the pre-existing local knowledge base" in tool.description

    @patch('agential_framework_env_alt.tools.query_local_docs_tool.RAGSystem')
    def test_ragsystem_singleton_behavior(self, MockRAGSystem):
        """Test that RAGSystem is instantiated only once by QueryLocalDocsTool."""
        mock_rag_instance1 = MagicMock()
        mock_rag_instance1.is_initialized = True
        MockRAGSystem.return_value = mock_rag_instance1

        QueryLocalDocsTool._rag_system_instance = None

        tool1 = QueryLocalDocsTool()
        assert MockRAGSystem.call_count == 1
        assert tool1._rag_system_instance is mock_rag_instance1

        tool2 = QueryLocalDocsTool()
        assert MockRAGSystem.call_count == 1
        assert tool2._rag_system_instance is mock_rag_instance1
        assert tool1._rag_system_instance is tool2._rag_system_instance

```
