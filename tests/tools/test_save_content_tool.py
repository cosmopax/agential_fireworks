# tests/tools/test_save_content_tool.py
import pytest
import os
import pathlib # For tmp_path
from agential_framework_env_alt.tools.save_content_tool import SaveContentTool
# We might not need to import WriteFileTool explicitly unless we are mocking its direct call,
# but SaveContentTool's __init__ does import it.

class TestSaveContentTool:

    @pytest.fixture
    def tool(self, tmp_path: pathlib.Path):
        """Instantiates SaveContentTool with a temporary sandbox directory."""
        return SaveContentTool(project_sandbox_dir=str(tmp_path))

    def test_save_new_file(self, tool: SaveContentTool, tmp_path: pathlib.Path):
        """Test saving content to a new file."""
        file_path_rel = "newly_saved_file.txt"
        content = "This content is being saved.\nAcross multiple lines."
        params = f"{file_path_rel}|{content}"

        result = tool.execute(params)
        expected_file_abs = tmp_path / file_path_rel

        assert "Successfully saved" in result # Key difference from WriteFileTool's message
        assert f"'./{file_path_rel}'" in result
        assert expected_file_abs.exists()
        assert expected_file_abs.is_file()
        assert expected_file_abs.read_text(encoding='utf-8') == content

    def test_overwrite_existing_file_with_save(self, tool: SaveContentTool, tmp_path: pathlib.Path):
        """Test overwriting an existing file using SaveContentTool."""
        file_path_rel = "to_be_overwritten.txt"
        initial_content = "Original saved data."
        new_content = "New saved data!"

        test_file_abs = tmp_path / file_path_rel
        test_file_abs.write_text(initial_content, encoding='utf-8')

        params = f"{file_path_rel}|{new_content}"
        result = tool.execute(params)

        assert "Successfully saved" in result
        assert f"'./{file_path_rel}'" in result
        assert test_file_abs.read_text(encoding='utf-8') == new_content

    def test_save_empty_content(self, tool: SaveContentTool, tmp_path: pathlib.Path):
        """Test saving empty content to a file."""
        file_path_rel = "empty_saved_file.txt"
        params = f"{file_path_rel}|" # Empty content part

        result = tool.execute(params)
        expected_file_abs = tmp_path / file_path_rel

        assert "Successfully saved 0 characters" in result # Tool reports num chars
        assert f"'./{file_path_rel}'" in result
        assert expected_file_abs.exists()
        assert expected_file_abs.is_file()
        assert expected_file_abs.read_text(encoding='utf-8') == ""

    @pytest.mark.parametrize("invalid_params, expected_error_part", [
        ("no_delimiter.txt_content_here", "Invalid parameters. Expected format: '[relative_file_path]|[content_to_save]'"),
        # SaveContentTool's own check for '|'
        # The following are errors from the internal WriteFileTool, propagated
        ("|content_only_no_path", "File path cannot be empty."),
        ("", "Invalid parameters. Expected format: '[relative_file_path]|[content_to_write]'"), # This error comes from WriteFileTool if '|' is not found by SaveContentTool first
        ("   |   some content", "File path cannot be empty."),
    ])
    def test_invalid_parameter_parsing_delegated(self, tool: SaveContentTool, invalid_params, expected_error_part):
        """Test that invalid parameter errors (some from SaveContentTool, some from internal WriteFileTool) are handled."""
        result = tool.execute(invalid_params)
        assert "Error:" in result
        assert expected_error_part in result


    def test_parent_directory_does_not_exist_delegated(self, tool: SaveContentTool, tmp_path: pathlib.Path):
        """Test saving to a file where the parent directory does not exist."""
        params = os.path.join("non_existent_subdir", "mysavedfile.txt") + "|Some data."
        result = tool.execute(params)

        assert "Error: Parent directory" in result
        assert "does not exist" in result
        assert f"'{os.path.join('.', 'non_existent_subdir')}'" in result or f"'non_existent_subdir'" in result


    def test_path_validation_sandbox_escape_delegated(self, tool: SaveContentTool, tmp_path: pathlib.Path):
        """Test path validation for sandbox escapes (delegated to WriteFileTool)."""
        content = "Attempting to save outside."

        outside_relative_path = os.path.join("..", "outside_save.txt")
        result_dotdot = tool.execute(f"{outside_relative_path}|{content}")
        assert "Error: Path" in result_dotdot
        assert "resolves outside the allowed project sandbox" in result_dotdot or "attempts to navigate outside the allowed project directory" in result_dotdot

        abs_path = str(tmp_path.parent / "another_outside_save.txt")
        result_abs = tool.execute(f"{abs_path}|{content}")
        assert "Error: Absolute paths are not allowed" in result_abs

        assert not (tmp_path.parent / "outside_save.txt").exists()
        assert not (tmp_path.parent / "another_outside_save.txt").exists()

    def test_cannot_save_to_a_directory_path_delegated(self, tool: SaveContentTool, tmp_path: pathlib.Path):
        """Test attempting to save to a path that is an existing directory."""
        dir_path_rel = "existing_save_folder"
        (tmp_path / dir_path_rel).mkdir()

        params = f"{dir_path_rel}|Trying to overwrite a dir with save."
        result = tool.execute(params)

        assert "Error: Path" in result
        assert "points to an existing directory. Cannot write file." in result
        assert f"'{dir_path_rel}'" in result


    def test_tool_properties(self, tool: SaveContentTool):
        """Test basic properties of the tool."""
        assert tool.name == "SaveContentTool"
        assert "Saves provided text content" in tool.description
        # Check if the description contains the specific caution from WriteFileTool's behavior (it should)
        assert "Use with caution as it can overwrite files." in tool.description
        assert os.path.isabs(tool.write_file_tool_instance.project_sandbox_dir)

    def test_save_content_tool_initialization_failure(self, tmp_path: pathlib.Path):
        """Test SaveContentTool's behavior if internal WriteFileTool fails to init (e.g., bad sandbox path)."""
        with pytest.raises(RuntimeError, match="SaveContentTool: Failed to initialize internal WriteFileTool instance"):
            # Create a path that is a file, not a directory, to make WriteFileTool's __init__ fail
            invalid_sandbox_path_file = tmp_path / "i_am_a_file_not_a_dir.txt"
            invalid_sandbox_path_file.write_text("content")
            SaveContentTool(project_sandbox_dir=str(invalid_sandbox_path_file))

        with pytest.raises(ValueError, match="SaveContentTool: project_sandbox_dir .* must be a valid, existing directory"):
            SaveContentTool(project_sandbox_dir=str(tmp_path / "non_existent_dir_for_save_tool"))

```
