# tests/tools/test_help_tool.py
import pytest
# Assuming 'agential_framework_env_alt' is in PYTHONPATH or pytest is run from project root
from agential_framework_env_alt.tools.help_tool import HelpTool

class TestHelpTool:

    @pytest.fixture
    def mock_tools_info(self):
        """Provides a sample dictionary of available tools information."""
        return {
            "CalculatorTool": "Calculates arithmetic expressions. Example: 2+2. Supports +, -, *, /, **.",
            "WebSearchTool": "Searches the web using DuckDuckGo. Returns top results. Needs a query string.",
            "ListDirectoryTool": "Lists files and directories at a given path. Path is relative to sandbox. Example: './my_folder'."
        }

    @pytest.fixture
    def help_tool(self, mock_tools_info):
        """Returns an instance of HelpTool initialized with mock_tools_info."""
        return HelpTool(available_tools_info=mock_tools_info)

    @pytest.fixture
    def help_tool_empty(self):
        """Returns an instance of HelpTool initialized with no tools info."""
        return HelpTool(available_tools_info={})

    @pytest.mark.parametrize("param", ["", "all", "LIST", " list "])
    def test_list_all_tools(self, help_tool: HelpTool, mock_tools_info, param):
        """Test listing all available tools with brief descriptions."""
        result = help_tool.execute(param)

        assert "Available tools:" in result
        for tool_name, full_desc in mock_tools_info.items():
            # HelpTool's 'all' list shows only the first sentence of the description
            brief_desc = full_desc.split('.')[0] + '.' if '.' in full_desc else full_desc
            expected_line = f"- {tool_name}: {brief_desc}"
            assert expected_line in result

        # Check number of listed tools matches mock_tools_info
        # Output starts with "Available tools:", then one line per tool
        assert len(result.strip().split('\n')) == len(mock_tools_info) + 1


    @pytest.mark.parametrize("tool_name_query, expected_tool_key", [
        ("CalculatorTool", "CalculatorTool"),
        ("calculatortool", "CalculatorTool"), # Case-insensitive query
        ("WEBSEARCHTOOL", "WebSearchTool"),   # Case-insensitive query
        ("ListDirectoryTool", "ListDirectoryTool")
    ])
    def test_help_for_specific_existing_tool(self, help_tool: HelpTool, mock_tools_info, tool_name_query, expected_tool_key):
        """Test getting help for a specific, existing tool (case-insensitive query)."""
        result = help_tool.execute(tool_name_query)

        expected_header = f"Help for tool '{expected_tool_key}':"
        assert expected_header in result
        assert mock_tools_info[expected_tool_key] in result # Full description

    def test_help_for_non_existent_tool(self, help_tool: HelpTool):
        """Test getting help for a tool that does not exist."""
        tool_name_query = "ImaginaryTool"
        result = help_tool.execute(tool_name_query)

        assert f"Sorry, no help available for a tool named '{tool_name_query}'." in result
        assert "Use 'HelpTool' with no parameters or 'all' to list available tools." in result

    def test_list_all_tools_when_no_tools_available(self, help_tool_empty: HelpTool):
        """Test listing all tools when HelpTool was initialized with empty info."""
        result = help_tool_empty.execute("") # Or "all"
        assert "No tools are currently available or HelpTool was not initialized correctly." in result

    def test_help_for_specific_tool_when_no_tools_available(self, help_tool_empty: HelpTool):
        """Test specific help when HelpTool was initialized with empty info."""
        result = help_tool_empty.execute("AnyTool")
        # Should indicate no help available because the internal dict is empty
        assert "Sorry, no help available for a tool named 'AnyTool'." in result
        assert "Use 'HelpTool' with no parameters or 'all' to list available tools." in result


    def test_tool_properties(self, help_tool: HelpTool):
        """Test basic properties of the HelpTool."""
        assert help_tool.name == "HelpTool"
        assert "Provides information about available tools" in help_tool.description
        assert "Input can be a specific tool name" in help_tool.description

    def test_help_tool_init_with_bad_data(self):
        """Test HelpTool initialization with incorrect data type (should handle gracefully)."""
        # HelpTool __init__ has a print warning and sets self.available_tools_info = {}
        # It does not raise an error.
        tool = HelpTool(available_tools_info="not a dict") # Pass a string instead of dict
        assert isinstance(tool.available_tools_info, dict) # Should be a dict
        assert tool.available_tools_info == {} # Should default to empty dict
        result = tool.execute("") # Should behave like no tools available
        assert "No tools are currently available or HelpTool was not initialized correctly." in result

```
