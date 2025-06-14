# tests/tools/test_write_file_tool.py
import pytest
import os
import pathlib # For tmp_path
from agential_framework_env_alt.tools.write_file_tool import WriteFileTool

class TestWriteFileTool:

    @pytest.fixture
    def tool(self, tmp_path: pathlib.Path):
        """Instantiates WriteFileTool with a temporary sandbox directory."""
        return WriteFileTool(project_sandbox_dir=str(tmp_path))

    def test_write_new_file(self, tool: WriteFileTool, tmp_path: pathlib.Path):
        """Test writing content to a new file."""
        file_path_rel = "new_notes.txt"
        content = "This is a test note.\nWith multiple lines."
        params = f"{file_path_rel}|{content}"

        result = tool.execute(params)
        expected_file_abs = tmp_path / file_path_rel

        assert "Successfully wrote" in result
        assert f"'./{file_path_rel}'" in result # Check display path
        assert expected_file_abs.exists()
        assert expected_file_abs.is_file()
        assert expected_file_abs.read_text(encoding='utf-8') == content

    def test_overwrite_existing_file(self, tool: WriteFileTool, tmp_path: pathlib.Path):
        """Test overwriting an existing file."""
        file_path_rel = "existing_doc.txt"
        initial_content = "Old information."
        new_content = "Updated information!"

        test_file_abs = tmp_path / file_path_rel
        test_file_abs.write_text(initial_content, encoding='utf-8')

        params = f"{file_path_rel}|{new_content}"
        result = tool.execute(params)

        assert "Successfully wrote" in result
        assert f"'./{file_path_rel}'" in result
        assert test_file_abs.read_text(encoding='utf-8') == new_content

    def test_write_empty_content(self, tool: WriteFileTool, tmp_path: pathlib.Path):
        """Test writing empty content to a file (should create an empty file)."""
        file_path_rel = "empty_file.txt"
        params = f"{file_path_rel}|" # Empty content part

        result = tool.execute(params)
        expected_file_abs = tmp_path / file_path_rel

        assert "Successfully wrote 0 characters" in result # Tool reports num chars
        assert f"'./{file_path_rel}'" in result
        assert expected_file_abs.exists()
        assert expected_file_abs.is_file()
        assert expected_file_abs.read_text(encoding='utf-8') == ""

    @pytest.mark.parametrize("invalid_params, expected_error_part", [
        ("no_delimiter.txt_content_here", "Invalid parameters. Expected format: '[relative_file_path]|[content_to_write]'"),
        ("|content_only_no_path", "File path cannot be empty."),
        ("", "Invalid parameters. Expected format: '[relative_file_path]|[content_to_write]'"), # Empty params string
        ("   |   some content", "File path cannot be empty."), # Path is whitespace
    ])
    def test_invalid_parameter_parsing(self, tool: WriteFileTool, invalid_params, expected_error_part):
        """Test various invalid parameter formats."""
        result = tool.execute(invalid_params)
        assert "Error:" in result
        assert expected_error_part in result

    def test_parent_directory_does_not_exist(self, tool: WriteFileTool, tmp_path: pathlib.Path):
        """Test writing to a file where the parent directory does not exist."""
        # tmp_path itself is the sandbox root, it exists.
        # Tool is designed not to create directories.
        params = os.path.join("non_existent_subdir", "myfile.txt") + "|Some data."
        result = tool.execute(params)

        assert "Error: Parent directory" in result
        assert "does not exist" in result
        # Use os.path.join for platform-independent path segment in assertion
        assert f"'{os.path.join('.', 'non_existent_subdir')}'" in result or f"'non_existent_subdir'" in result


    def test_path_validation_sandbox_escape(self, tool: WriteFileTool, tmp_path: pathlib.Path):
        """Test path validation for sandbox escapes when writing."""
        content = "Attempting to write outside."

        # Construct path that tries to go up one level from sandbox
        # and then into a hypothetical sibling directory "outside_project_root"
        # This test assumes the sandbox (tmp_path) has a parent.
        outside_path_rel = os.path.join("..", "outside_file.txt")
        result_dotdot = tool.execute(f"{outside_path_rel}|{content}")

        assert "Error: Path" in result_dotdot
        assert "resolves outside the allowed project sandbox" in result_dotdot or "attempts to navigate outside the allowed project directory" in result_dotdot


        abs_path = str(tmp_path.parent / "another_outside.txt") # Ensure string for tool
        result_abs = tool.execute(f"{abs_path}|{content}")
        assert "Error: Absolute paths are not allowed" in result_abs

        # Ensure no file was actually created outside
        assert not (tmp_path.parent / "outside_file.txt").exists()
        assert not (tmp_path.parent / "another_outside.txt").exists()


    def test_cannot_write_to_a_directory_path(self, tool: WriteFileTool, tmp_path: pathlib.Path):
        """Test attempting to write to a path that is an existing directory."""
        dir_path_rel = "existing_folder"
        (tmp_path / dir_path_rel).mkdir()

        params = f"{dir_path_rel}|Trying to overwrite a dir."
        result = tool.execute(params)

        assert "Error: Path" in result
        assert "points to an existing directory. Cannot write file." in result
        assert f"'{dir_path_rel}'" in result

    def test_tool_properties(self, tool: WriteFileTool):
        """Test basic properties of the tool."""
        assert tool.name == "WriteFileTool"
        assert "Writes or overwrites a text file" in tool.description
        assert "Use with caution as it can overwrite files." in tool.description # Important warning
        assert os.path.isabs(tool.project_sandbox_dir)

```
