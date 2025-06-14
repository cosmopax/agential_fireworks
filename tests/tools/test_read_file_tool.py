# tests/tools/test_read_file_tool.py
import pytest
import os
import pathlib # For tmp_path
from agential_framework_env_alt.tools.read_file_tool import ReadFileTool, DEFAULT_MAX_READ_CHARS

class TestReadFileTool:

    @pytest.fixture
    def tool_default_read_limit(self, tmp_path: pathlib.Path):
        """Instantiates ReadFileTool with default read limit, using tmp_path as sandbox."""
        return ReadFileTool(project_sandbox_dir=str(tmp_path))

    @pytest.fixture
    def tool_custom_read_limit(self, tmp_path: pathlib.Path):
        """Instantiates ReadFileTool with a small custom read limit for truncation tests."""
        return ReadFileTool(project_sandbox_dir=str(tmp_path), max_read_chars=10)

    def test_read_full_file_within_limit(self, tool_default_read_limit: ReadFileTool, tmp_path: pathlib.Path):
        """Test reading a file whose content is shorter than the default max_read_chars."""
        file_content = "This is a test file with content."
        test_file = tmp_path / "testfile.txt"
        test_file.write_text(file_content, encoding='utf-8')

        result = tool_default_read_limit.execute("testfile.txt")

        expected_output_start = "Content of file './testfile.txt' (from user input 'testfile.txt'):\n---\n"
        # expected_output_end = f"\n---\n[Note: Content was truncated to the first {DEFAULT_MAX_READ_CHARS} characters.]"

        assert result.startswith(expected_output_start)
        assert file_content in result

        # The current truncation check in ReadFileTool is: if len(content) == self.max_read_chars, it tries to read one more byte.
        # If successful, was_truncated = True.
        if len(file_content) < DEFAULT_MAX_READ_CHARS:
            assert "[Note: Content was truncated" not in result
        # If len(file_content) == DEFAULT_MAX_READ_CHARS, the note might appear if the file size is exactly that
        # and the one-byte check reads nothing more. This part can be tricky to assert universally
        # without knowing if the file system adds an EOF marker that counts as a byte for size but not for read(1).
        # For simplicity, if it's exactly at the limit, we accept either outcome for the note.
        elif len(file_content) == DEFAULT_MAX_READ_CHARS:
            # This condition is hard to reliably test for the note's absence/presence without exact file size knowledge
            # vs. how read(1) behaves at EOF. The core is that content is read.
            pass


    def test_read_file_with_truncation(self, tool_custom_read_limit: ReadFileTool, tmp_path: pathlib.Path):
        """Test reading a file where content is longer than max_read_chars."""
        file_content = "This is a long line of text for testing truncation."
        custom_limit = tool_custom_read_limit.max_read_chars # Should be 10
        assert len(file_content) > custom_limit

        test_file = tmp_path / "longfile.txt"
        test_file.write_text(file_content, encoding='utf-8')

        result = tool_custom_read_limit.execute("longfile.txt")

        expected_content_part = file_content[:custom_limit]
        expected_output_start = "Content of file './longfile.txt' (from user input 'longfile.txt'):\n---\n"
        expected_truncation_note = f"[Note: Content was truncated to the first {custom_limit} characters.]"

        assert result.startswith(expected_output_start)
        assert result.strip().endswith(expected_truncation_note) # Check end after strip
        assert expected_content_part == result[len(expected_output_start):len(expected_output_start)+custom_limit] # Check the content part
        assert file_content not in result # Full content should not be there unless limit is larger than content

    def test_path_validation_sandbox_escape(self, tool_default_read_limit: ReadFileTool, tmp_path: pathlib.Path):
        """Test path validation for sandbox escapes."""
        result_dotdot = tool_default_read_limit.execute(os.path.join("..", "sensitive_file.txt"))
        assert "Error: Path" in result_dotdot
        assert "resolves outside the allowed project sandbox" in result_dotdot or "attempts to navigate outside the allowed project directory" in result_dotdot


        abs_path = os.path.abspath(os.path.join(str(tmp_path.parent), "some_other_file.txt"))
        result_abs = tool_default_read_limit.execute(abs_path)
        assert "Error: Absolute paths are not allowed" in result_abs

    def test_non_existent_file(self, tool_default_read_limit: ReadFileTool):
        """Test reading a non-existent file."""
        result = tool_default_read_limit.execute("ghost_file.txt")
        assert "does not exist" in result
        assert "'ghost_file.txt'" in result

    def test_path_is_a_directory(self, tool_default_read_limit: ReadFileTool, tmp_path: pathlib.Path):
        """Test attempting to read a directory as if it were a file."""
        folder_name = "a_folder"
        (tmp_path / folder_name).mkdir()
        result = tool_default_read_limit.execute(folder_name)
        assert "is not a file" in result
        assert f"'{folder_name}'" in result

    def test_empty_file_path_parameter(self, tool_default_read_limit: ReadFileTool):
        """Test execute with an empty file path parameter."""
        result = tool_default_read_limit.execute("")
        assert "Error: File path parameter cannot be empty." in result

        result_space = tool_default_read_limit.execute("   ")
        assert "Error: File path parameter cannot be empty." in result_space


    def test_unicode_decode_error(self, tool_default_read_limit: ReadFileTool, tmp_path: pathlib.Path):
        """Test reading a file with non-UTF-8 content."""
        non_utf8_file_name = "binary.dat"
        non_utf8_file = tmp_path / non_utf8_file_name
        non_utf8_file.write_bytes(b'\x80\xff') # Invalid UTF-8 sequence

        result = tool_default_read_limit.execute(non_utf8_file_name)
        assert "Error: Could not decode file" in result
        assert "as UTF-8 text" in result
        assert f"'./{non_utf8_file_name}'" in result

    def test_tool_properties_default_limit(self, tool_default_read_limit: ReadFileTool):
        """Test tool properties with default read limit."""
        assert tool_default_read_limit.name == "ReadFileTool"
        assert str(DEFAULT_MAX_READ_CHARS) in tool_default_read_limit.description
        assert "Reads the content of a specified text file" in tool_default_read_limit.description
        assert os.path.isabs(tool_default_read_limit.project_sandbox_dir)

    def test_tool_properties_custom_limit(self, tool_custom_read_limit: ReadFileTool):
        """Test tool properties with custom read limit."""
        custom_limit = 10 # Must match the fixture
        assert tool_custom_read_limit.name == "ReadFileTool"
        assert str(custom_limit) in tool_custom_read_limit.description
        assert tool_custom_read_limit.max_read_chars == custom_limit
```
