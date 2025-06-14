# tests/tools/test_web_search_tool.py
import pytest
from unittest.mock import patch, MagicMock
# Assuming 'agential_framework_env_alt' is in PYTHONPATH or pytest is run from project root
from agential_framework_env_alt.tools.web_search_tool import WebSearchTool, DEFAULT_MAX_RESULTS

class TestWebSearchTool:

    @pytest.fixture
    def tool_default_max_results(self):
        """Returns an instance of WebSearchTool with default max_results."""
        # Note: WebSearchTool __init__ doesn't take project_sandbox_dir, so no need to pass it.
        # It also doesn't take Tavily API key here, as this is the DDGS version.
        return WebSearchTool()

    @pytest.fixture
    def tool_custom_max_results(self):
        """Returns an instance of WebSearchTool with custom max_results=1."""
        return WebSearchTool(max_results=1)

    @patch('agential_framework_env_alt.tools.web_search_tool.DDGS')
    def test_successful_search_single_result(self, mock_ddgs_class, tool_default_max_results: WebSearchTool):
        """Test a successful search returning a single result."""
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = [
            {'title': 'Test Title 1', 'body': 'Test snippet body 1.', 'href': 'http://example.com/1'}
        ]
        mock_ddgs_class.return_value.__enter__.return_value = mock_ddgs_instance

        query = "test query"
        result = tool_default_max_results.execute(query)

        mock_ddgs_instance.text.assert_called_once_with(keywords=query, max_results=tool_default_max_results.max_results)
        assert f"Search results for '{query}':" in result
        assert "1. Title: Test Title 1" in result
        assert "Snippet: Test snippet body 1." in result
        assert "Source: http://example.com/1" in result

    @patch('agential_framework_env_alt.tools.web_search_tool.DDGS')
    def test_successful_search_multiple_results_respecting_tool_max_limit(self, mock_ddgs_class, tool_custom_max_results: WebSearchTool):
        """Test search with multiple results, respecting max_results limit of the tool."""
        mock_ddgs_instance = MagicMock()
        # Simulate DDGS library returning more results than the tool's configured max_results
        mock_ddgs_instance.text.return_value = [
            {'title': 'Title A', 'body': 'Snippet A.', 'href': 'http://example.com/a'},
            {'title': 'Title B', 'body': 'Snippet B.', 'href': 'http://example.com/b'}
        ]
        mock_ddgs_class.return_value.__enter__.return_value = mock_ddgs_instance

        query = "another query"
        # tool_custom_max_results has max_results=1
        result = tool_custom_max_results.execute(query)

        # The tool should call DDGS().text with its own max_results limit
        mock_ddgs_instance.text.assert_called_once_with(keywords=query, max_results=1)

        # Even if DDGS().text hypothetically returned more (due to its own internal logic or if we didn't control its max_results),
        # our tool's loop `for i, res in enumerate(results): if i >= self.max_results: break` (if it existed)
        # or rather, the fact that `ddgs.text(max_results=self.max_results)` is called, should limit it.
        # The current tool code passes self.max_results to ddgs.text(), so the library handles the limit.
        # This test verifies that call and the output.
        assert f"Search results for '{query}':" in result
        assert "1. Title: Title A" in result
        assert "Snippet: Snippet A." in result
        assert "Source: http://example.com/a" in result
        assert "Title B" not in result # Should not include the second result

    @patch('agential_framework_env_alt.tools.web_search_tool.DDGS')
    def test_search_no_results(self, mock_ddgs_class, tool_default_max_results: WebSearchTool):
        """Test search that yields no results."""
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = []
        mock_ddgs_class.return_value.__enter__.return_value = mock_ddgs_instance

        query = "a very obscure query"
        result = tool_default_max_results.execute(query)

        mock_ddgs_instance.text.assert_called_once_with(keywords=query, max_results=tool_default_max_results.max_results)
        assert f"No search results found for '{query}'." in result

    def test_empty_query_string(self, tool_default_max_results: WebSearchTool):
        """Test providing an empty or whitespace query string."""
        result_empty = tool_default_max_results.execute("")
        assert "Error: Search query cannot be empty." in result_empty

        result_whitespace = tool_default_max_results.execute("   ")
        assert "Error: Search query cannot be empty." in result_whitespace

    @patch('agential_framework_env_alt.tools.web_search_tool.DDGS')
    def test_search_api_error(self, mock_ddgs_class, tool_default_max_results: WebSearchTool):
        """Test handling of an error during the search API call."""
        mock_ddgs_instance = MagicMock()
        simulated_error_message = "Simulated API Network Error"
        mock_ddgs_instance.text.side_effect = Exception(simulated_error_message)
        mock_ddgs_class.return_value.__enter__.return_value = mock_ddgs_instance

        query = "query causing error"
        result = tool_default_max_results.execute(query)

        mock_ddgs_instance.text.assert_called_once_with(keywords=query, max_results=tool_default_max_results.max_results)
        assert f"Error performing web search for '{query}': Exception: {simulated_error_message}" in result

    @patch('agential_framework_env_alt.tools.web_search_tool.DDGS')
    def test_long_snippet_truncation(self, mock_ddgs_class, tool_default_max_results: WebSearchTool):
        """Test that long snippets are truncated correctly."""
        mock_ddgs_instance = MagicMock()
        long_body = "This is a very long snippet that definitely exceeds the two hundred and fifty character limit which has been set for display purposes to ensure that the output provided to the language model is not overly verbose and remains manageable for context window limitations. This part should be cut off."
        shortened_body_expected_len = 250 # As defined in WebSearchTool
        expected_snippet = long_body[:shortened_body_expected_len] + "..."

        mock_ddgs_instance.text.return_value = [
            {'title': 'Long Snippet Test', 'body': long_body, 'href': 'http://example.com/long'}
        ]
        mock_ddgs_class.return_value.__enter__.return_value = mock_ddgs_instance

        result = tool_default_max_results.execute("long snippet query")
        assert f"Snippet: {expected_snippet}" in result

    def test_tool_properties_default(self, tool_default_max_results: WebSearchTool):
        """Test tool properties with default max_results."""
        assert tool_default_max_results.name == "WebSearchTool"
        assert "Performs a web search using DuckDuckGo" in tool_default_max_results.description
        assert f"top {DEFAULT_MAX_RESULTS} search results" in tool_default_max_results.description
        assert tool_default_max_results.max_results == DEFAULT_MAX_RESULTS

    def test_tool_properties_custom(self, tool_custom_max_results: WebSearchTool):
        """Test tool properties with custom max_results."""
        custom_max = 1 # Must match the fixture
        assert tool_custom_max_results.name == "WebSearchTool"
        assert f"top {custom_max} search results" in tool_custom_max_results.description
        assert tool_custom_max_results.max_results == custom_max

```
