# tests/tools/test_make_directory_tool.py
import pytest
import os
import pathlib # For tmp_path
from agential_framework_env_alt.tools.make_directory_tool import MakeDirectoryTool

class TestMakeDirectoryTool:

    @pytest.fixture
    def tool(self, tmp_path: pathlib.Path):
        """Instantiates MakeDirectoryTool with a temporary sandbox directory."""
        return MakeDirectoryTool(project_sandbox_dir=str(tmp_path))

    def test_create_new_single_directory(self, tool: MakeDirectoryTool, tmp_path: pathlib.Path):
        """Test creating a new single directory."""
        dir_name = "new_folder_alpha"
        result = tool.execute(dir_name)

        expected_dir_abs = tmp_path / dir_name
        assert "Successfully created directory" in result
        # The tool's display path logic might vary slightly for simple names vs. paths with separators
        # For 'new_folder_alpha', relpath(tmp_path / 'new_folder_alpha', tmp_path) is 'new_folder_alpha'
        assert f"'./{dir_name}'" in result or f"'{dir_name}'" in result
        assert expected_dir_abs.exists()
        assert expected_dir_abs.is_dir()

    def test_create_nested_directories(self, tool: MakeDirectoryTool, tmp_path: pathlib.Path):
        """Test creating nested directories (os.makedirs behavior)."""
        nested_path_str = os.path.join("level1", "level2", "final_dir") # Use os.path.join for platform independence
        result = tool.execute(nested_path_str)

        expected_dir_abs = tmp_path / nested_path_str
        assert "Successfully created directory" in result
        assert f"'./{nested_path_str}'" in result or f"'{nested_path_str}'" in result
        assert expected_dir_abs.exists()
        assert expected_dir_abs.is_dir()

    def test_directory_already_exists(self, tool: MakeDirectoryTool, tmp_path: pathlib.Path):
        """Test creating a directory that already exists (should succeed due to exist_ok=True)."""
        dir_name = "pre_existing_dir"
        existing_dir_abs = tmp_path / dir_name
        existing_dir_abs.mkdir() # Create it first

        result = tool.execute(dir_name)
        assert "Successfully created directory (or it already existed)" in result
        assert f"'./{dir_name}'" in result or f"'{dir_name}'" in result
        assert existing_dir_abs.is_dir() # Still a directory

    def test_path_validation_sandbox_escape(self, tool: MakeDirectoryTool, tmp_path: pathlib.Path):
        """Test path validation for sandbox escapes when creating directories."""
        outside_relative_path = os.path.join("..", "attempt_outside_dir")
        result_dotdot = tool.execute(outside_relative_path)
        assert "Error: Path" in result_dotdot
        # Check for either of the specific error messages from _is_safe_path
        assert ("resolves to" in result_dotdot and "which is outside the allowed project sandbox" in result_dotdot) or \
               ("attempts to navigate outside or is absolute after normalization" in result_dotdot)

        assert not (tmp_path.parent / "attempt_outside_dir").exists()

        # Construct an absolute path that is outside the sandbox
        abs_path_attempt = str(tmp_path.parent / "another_attempt_outside")
        result_abs = tool.execute(abs_path_attempt)
        assert "Error: Absolute paths are not allowed" in result_abs
        assert not (tmp_path.parent / "another_attempt_outside").exists()


    def test_path_is_an_existing_file(self, tool: MakeDirectoryTool, tmp_path: pathlib.Path):
        """Test attempting to create a directory where a file already exists."""
        file_name = "existing_file.txt"
        existing_file_abs = tmp_path / file_name
        existing_file_abs.write_text("This is a file.")

        result = tool.execute(file_name)
        assert "Error: Cannot create directory. A file already exists at" in result
        assert f"'./{file_name}'" in result or f"'{file_name}'" in result

    @pytest.mark.parametrize("invalid_path, expected_error_part", [
        ("", "Directory path parameter cannot be empty or just '.'"),
        ("   ", "Directory path parameter cannot be empty or just '.'"),
        (".", "Directory path parameter cannot be empty or just '.'"),
        ("./", "Directory path parameter cannot be empty or just '.'"),
    ])
    def test_invalid_path_parameters(self, tool: MakeDirectoryTool, invalid_path, expected_error_part):
        """Test invalid path parameters like empty string or '.'."""
        result = tool.execute(invalid_path)
        assert "Error:" in result
        assert expected_error_part in result

    def test_tool_properties(self, tool: MakeDirectoryTool):
        """Test basic properties of the tool."""
        assert tool.name == "MakeDirectoryTool"
        assert "Creates a new directory" in tool.description
        assert "relative to the project's configured sandbox directory" in tool.description
        assert os.path.isabs(tool.project_sandbox_dir)

```
