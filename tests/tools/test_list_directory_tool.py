# tests/tools/test_list_directory_tool.py
import pytest
import os
import pathlib # For tmp_path which is a pathlib.Path object
from agential_framework_env_alt.tools.list_directory_tool import ListDirectoryTool

class TestListDirectoryTool:

    @pytest.fixture
    def tool(self, tmp_path: pathlib.Path):
        """Instantiates ListDirectoryTool with a temporary sandbox directory."""
        # tmp_path is a pathlib.Path object, convert to string for the tool
        return ListDirectoryTool(project_sandbox_dir=str(tmp_path))

    def test_list_empty_directory(self, tool: ListDirectoryTool, tmp_path: pathlib.Path):
        """Test listing an empty directory."""
        # tmp_path is initially empty
        result = tool.execute(".") # Execute with "." for current (sandbox) directory
        # Expected message might vary slightly, e.g. "The directory '.' (resolved to './.') is empty."
        assert "is empty" in result
        assert f"Contents of directory '.' (resolved to './.')" not in result # Check it doesn't try to list if empty

        result_empty_param = tool.execute("") # Should be same as "."
        assert "is empty" in result_empty_param

    def test_list_directory_with_content(self, tool: ListDirectoryTool, tmp_path: pathlib.Path):
        """Test listing a directory with files and subdirectories."""
        # Create some content
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file_b.log").write_text("log_content")
        (tmp_path / "subdir1").mkdir()
        (tmp_path / "subdir_a").mkdir()
        (tmp_path / "subdir_a" / "nested_file.md").write_text("nested")

        result = tool.execute(".") # List the root of the sandbox

        # print(f"DEBUG: ListDirectoryTool output for populated dir:\n{result}")

        # Expected items (sorted alphabetically by ListDirectoryTool's current implementation)
        # The tool sorts items using sorted(os.listdir(full_path))
        expected_header_part = "Contents of directory '.' (resolved to './.')"
        expected_items_sorted = sorted([
            "- file1.txt (file)",
            "- file_b.log (file)",
            "- subdir1 (directory)",
            "- subdir_a (directory)"
        ])

        result_lines = result.strip().split('\n')

        assert expected_header_part in result_lines[0]

        actual_listed_items = sorted([line for line in result_lines if line.startswith("- ")])
        assert actual_listed_items == expected_items_sorted
        assert len(actual_listed_items) == len(expected_items_sorted)
        assert len(result_lines) == len(expected_items_sorted) + 1 # +1 for header

    def test_list_subdirectory(self, tool: ListDirectoryTool, tmp_path: pathlib.Path):
        """Test listing a specific subdirectory within the sandbox."""
        subdir_path_obj = tmp_path / "my_data" / "logs" # Use pathlib for path manipulation
        subdir_path_obj.mkdir(parents=True, exist_ok=True)
        (subdir_path_obj / "log1.txt").write_text("log1")
        (subdir_path_obj / "another_file.dat").write_text("data")

        # Path param for tool is relative to sandbox root (tmp_path)
        relative_path_to_list = os.path.join("my_data", "logs") # Use os.path.join for platform indep. string path
        result = tool.execute(relative_path_to_list)

        # print(f"DEBUG: ListDirectoryTool output for subdir:\n{result}")

        # Construct expected relative path for display based on OS
        expected_display_rel_path = os.path.join('.', 'my_data', 'logs')


        expected_header = f"Contents of directory './{expected_display_rel_path}' (from user input '{relative_path_to_list}')"
        expected_items = sorted([
            "- another_file.dat (file)",
            "- log1.txt (file)"
        ])

        result_lines = result.strip().split('\n')
        assert expected_header in result_lines[0]

        actual_listed_items = sorted([line for line in result_lines[1:] if line.startswith("- ")])
        assert actual_listed_items == expected_items
        assert len(actual_listed_items) == 2

    def test_path_validation_sandbox_escape_attempts(self, tool: ListDirectoryTool, tmp_path: pathlib.Path):
        """Test attempts to list directories outside the sandbox."""

        result_dotdot = tool.execute(os.path.join("..", "another_dir"))
        # The exact error message might vary slightly based on how realpath and startswith interact at the boundary.
        # The key is that it should be an error indicating an attempt to go outside.
        assert "Error: Path" in result_dotdot
        assert "resolves outside the allowed project sandbox" in result_dotdot or "attempts to navigate outside the allowed sandbox directory" in result_dotdot

        abs_path_to_try = os.path.abspath(os.sep)
        result_abs = tool.execute(abs_path_to_try)
        assert "Error: Absolute paths are not allowed." in result_abs

    def test_non_existent_path(self, tool: ListDirectoryTool, tmp_path: pathlib.Path):
        """Test listing a non-existent directory."""
        non_existent_dir = "this_dir_does_not_exist"
        result = tool.execute(non_existent_dir)
        assert "does not exist" in result
        assert f"'{non_existent_dir}'" in result

    def test_path_is_a_file(self, tool: ListDirectoryTool, tmp_path: pathlib.Path):
        """Test attempting to list a path that is a file, not a directory."""
        file_in_sandbox_name = "iam_a_file.txt"
        file_in_sandbox = tmp_path / file_in_sandbox_name
        file_in_sandbox.write_text("I am a file.")

        result = tool.execute(file_in_sandbox_name)
        assert "is not a directory" in result
        assert f"'{file_in_sandbox_name}'" in result

    def test_tool_properties(self, tool: ListDirectoryTool):
        """Test basic properties of the tool."""
        assert tool.name == "ListDirectoryTool"
        assert "Lists the contents" in tool.description
        assert "relative to the project's configured sandbox directory" in tool.description
        assert os.path.isabs(tool.project_sandbox_dir)

```
