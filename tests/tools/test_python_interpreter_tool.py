# tests/tools/test_python_interpreter_tool.py
import pytest
import os
import signal # For checking if signal is available for timeout test
from agential_framework_env_alt.tools.python_interpreter_tool import PythonInterpreterTool, EXECUTION_TIMEOUT_SECONDS, TimeoutException

class TestPythonInterpreterTool:

    @pytest.fixture
    def tool(self, tmp_path): # tmp_path not strictly needed but good for consistency if tool ever uses sandbox_dir
        """Instantiates PythonInterpreterTool."""
        return PythonInterpreterTool(project_sandbox_dir=str(tmp_path))

    def test_tool_properties(self, tool: PythonInterpreterTool):
        """Test basic tool properties."""
        assert tool.name == "PythonInterpreterTool"
        assert "Executes a provided snippet of Python code" in tool.description
        assert f"time-limited to {EXECUTION_TIMEOUT_SECONDS} seconds" in tool.description
        assert "Available `math` functions:" in tool.description
        assert "Available `random` functions:" in tool.description

    @pytest.mark.parametrize("code_snippet, expected_stdout", [
        ("print(2+2)", "4"),
        ("my_list = [1, 2, 3]; print(sum(my_list))", "6"),
        ("s = 'hello world'; print(s.title())", "Hello World"),
        ("print(math['sqrt'](16))", "4.0"), # Access math functions as dict items
        ("import math; print(math.pi * 2)", "6.283185307179586"), # This will fail due to import, test in errors
        ("print(random['randint'](1,1))", "1"), # Access random functions as dict items
        ("data = {'key': 'value', 'numbers': [10,20]}; print(data['numbers'][0])", "10"),
    ])
    def test_valid_code_execution_text_output(self, tool: PythonInterpreterTool, code_snippet, expected_stdout):
        """Test execution of simple valid code snippets producing text output."""
        result = tool.execute(code_snippet)
        if "Error:" in result:
            # Special case for the "import math" which will fail due to restricted __import__
            if code_snippet == "import math; print(math.pi * 2)":
                assert "Name Error" in result
                assert "name '__import__' is not defined" in result
                return # Test passes for this specific error
            pytest.fail(f"Execution of '{code_snippet}' failed: {result}")

        # Some numeric outputs might be valid JSON, tool's output format reflects this.
        # We check if the expected_stdout is part of the actual output after the prefix.
        assert result.startswith("Execution successful. Output (Text):\n") or \
               result.startswith("Execution successful. Output (JSON String):\n")

        actual_output = result.split("\n",1)[1] if "\n" in result else ""
        assert actual_output == expected_stdout


    def test_json_output_detection(self, tool: PythonInterpreterTool):
        """Test that valid JSON printed by the code is identified."""
        # Code must print a string that IS JSON, as 'import json' is not available.
        json_string_code = "print('{\"name\": \"Test\", \"version\": 1.0, \"items\": [1, \"a\"]}')"
        expected_json_str = '{"name": "Test", "version": 1.0, "items": [1, "a"]}'

        result = tool.execute(json_string_code)
        assert result == f"Execution successful. Output (JSON String):\n{expected_json_str}"

        list_json_code = "print('[1,2,3, \"hello\"]')"
        expected_list_json_str = '[1,2,3, "hello"]'
        result_list = tool.execute(list_json_code)
        assert result_list == f"Execution successful. Output (JSON String):\n{expected_list_json_str}"

        # Test non-JSON complex output
        non_json_code = "print({'a', 'b', 'c'})" # A set, repr is not JSON
        result_non_json = tool.execute(non_json_code)
        assert result_non_json.startswith("Execution successful. Output (Text):\n")
        # Order of elements in set representation can vary
        assert "'a'" in result_non_json and "'b'" in result_non_json and "'c'" in result_non_json


    def test_no_stdout_output(self, tool: PythonInterpreterTool):
        """Test code that executes successfully but produces no stdout."""
        code = "x = 1 + 1\ny = x * 2" # No print statement
        result = tool.execute(code)
        assert result == "Execution successful. No output produced to stdout."

    @pytest.mark.parametrize("code_snippet, expected_error_type, expected_message_part", [
        ("print(2+)", "Syntax Error", "unexpected EOF while parsing"),
        ("open('file.txt')", "Name Error", "name 'open' is not defined"),
        ("import os", "Name Error", "name '__import__' is not defined"),
        ("print(type(1))", "Name Error", "name 'type' is not defined"),
        ("print(math['non_existent_func']())", "Key Error", "'non_existent_func'"), # KeyError on the math dict
        ("print(undefined_variable)", "Name Error", "name 'undefined_variable' is not defined"),
        ("len(5)", "Type Error", "object of type 'int' has no len()"),
        ("print(1/0)", "Zero Division Error", "division by zero"),
    ])
    def test_error_handling(self, tool: PythonInterpreterTool, code_snippet, expected_error_type, expected_message_part):
        """Test various Python errors during execution."""
        result = tool.execute(code_snippet)
        assert expected_error_type in result
        assert expected_message_part in result

    @pytest.mark.skipif(not (hasattr(signal, 'SIGALRM') and hasattr(signal, 'alarm')), reason="signal.alarm is not available on this platform (likely Windows).")
    def test_code_execution_timeout(self, tool: PythonInterpreterTool):
        """Test that code execution times out if it runs too long."""
        infinite_loop_code = "x = 0\nwhile True:\n  x += 1"
        result = tool.execute(infinite_loop_code)
        assert "Error: Code execution timed out" in result
        assert f"after {EXECUTION_TIMEOUT_SECONDS} seconds" in result

    def test_empty_or_whitespace_code_snippet(self, tool: PythonInterpreterTool):
        """Test providing an empty or whitespace-only code snippet."""
        result_empty = tool.execute("")
        assert "Error: Python code snippet cannot be empty." in result_empty

        result_whitespace = tool.execute("   \n   ")
        assert "Error: Python code snippet cannot be empty." in result_whitespace

    def test_disallowed_builtin_access_attempts(self, tool: PythonInterpreterTool):
        """Test attempts to access disallowed builtins or modules through tricky means (should fail)."""
        code_trick = "print(().__class__.__base__.__subclasses__())"
        result = tool.execute(code_trick)
        # The result will be a long list of classes, but importantly, it shouldn't allow execution of dangerous methods.
        # The crucial check is that dangerous names are not made available.
        assert "open" not in result.lower() # Check if 'open' appears in the output list of classes/methods
        assert "__import__" not in result.lower()
        assert "os" not in result.lower()
        assert "sys" not in result.lower()
        assert "subprocess" not in result.lower()
```
