# tests/tools/test_get_date_tool.py
import pytest
from datetime import datetime
# Assuming 'agential_framework_env_alt' is in PYTHONPATH or pytest is run from project root
from agential_framework_env_alt.tools.get_date_tool import GetCurrentDateTool

class TestGetCurrentDateTool:

    @pytest.fixture
    def date_tool(self):
        """Returns an instance of GetCurrentDateTool."""
        return GetCurrentDateTool()

    def test_returns_string(self, date_tool):
        """Test that the execute method returns a string."""
        result = date_tool.execute("") # Parameter should be ignored
        assert isinstance(result, str)

    def test_output_format_and_valid_date(self, date_tool):
        """Test that the output string is a valid date in the expected format."""
        # Expected prefix: "The current date and time is: "
        expected_prefix = "The current date and time is: "

        result_string = date_tool.execute("some ignored params")
        assert result_string.startswith(expected_prefix)

        datetime_part_str = result_string[len(expected_prefix):].strip('.') # Remove potential trailing period if any from message

        # Attempt to parse the datetime string
        try:
            dt_object = datetime.strptime(datetime_part_str, "%Y-%m-%d %H:%M:%S")
            assert dt_object is not None # Should not be None if parsing succeeded
            # Check if the date is very recent (e.g., within the last few seconds)
            # This makes the test robust to the exact second of execution.
            assert abs((datetime.now() - dt_object).total_seconds()) < 5 # Allow 5s delta
        except ValueError:
            pytest.fail(f"Output datetime string '{datetime_part_str}' could not be parsed with format '%Y-%m-%d %H:%M:%S'. Full output: '{result_string}'")

    def test_ignores_parameters(self, date_tool):
        """Test that the tool ignores any input parameters."""
        # Get current time just before calling, for comparison
        time_before = datetime.now()

        result_with_params = date_tool.execute("some_random_param=123 foo bar")
        result_without_params = date_tool.execute("")

        # Both should start with the same prefix
        expected_prefix = "The current date and time is: "
        assert result_with_params.startswith(expected_prefix)
        assert result_without_params.startswith(expected_prefix)

        # Extract and parse the datetime part for both
        datetime_str_with_params = result_with_params[len(expected_prefix):].strip('.')
        datetime_str_without_params = result_without_params[len(expected_prefix):].strip('.')

        try:
            dt_with_params = datetime.strptime(datetime_str_with_params, "%Y-%m-%d %H:%M:%S")
            dt_without_params = datetime.strptime(datetime_str_without_params, "%Y-%m-%d %H:%M:%S")

            # The datetimes should be very close, accounting for execution time
            assert abs((dt_with_params - dt_without_params).total_seconds()) < 2 # Small delta
            assert abs((dt_with_params - time_before).total_seconds()) < 5 # Compare with time_before
            assert abs((dt_without_params - time_before).total_seconds()) < 5

        except ValueError:
            pytest.fail("Failed to parse datetime string in parameter ignorance test.")

    def test_tool_properties(self, date_tool):
        """Test basic properties of the tool."""
        assert date_tool.name == "GetCurrentDateTool"
        assert "Returns the current date and time" in date_tool.description
        assert "any input parameters will be ignored" in date_tool.description
