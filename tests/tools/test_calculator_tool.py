# tests/tools/test_calculator_tool.py
import pytest
# Assuming 'agential_framework_env_alt' is in PYTHONPATH or pytest is run from project root
from agential_framework_env_alt.tools.calculator_tool import CalculatorTool

class TestCalculatorTool:

    @pytest.fixture
    def calculator(self):
        """Returns an instance of CalculatorTool."""
        return CalculatorTool()

    @pytest.mark.parametrize("expression, expected_start", [
        ("2 + 2", "The result of '2 + 2' is 4"),
        ("5 - 3", "The result of '5 - 3' is 2"),
        ("4 * 6", "The result of '4 * 6' is 24"),
        ("10 / 2", "The result of '10 / 2' is 5.0"), # Floats for division
        ("2 + 3 * 4", "The result of '2 + 3 * 4' is 14"), # Order of operations
        ("(2 + 3) * 4", "The result of '(2 + 3) * 4' is 20"), # Parentheses
        ("2 ** 3", "The result of '2 ** 3' is 8"), # Exponentiation
        ("2 ^ 3", "The result of '2 ^ 3' is 8"),   # Alternative exponentiation
        ("10 / 4", "The result of '10 / 4' is 2.5"),
        ("-5 + 2", "The result of '-5 + 2' is -3"), # Negative numbers
        ("3 * -2", "The result of '3 * -2' is -6"),
        ("2.5 * 2", "The result of '2.5 * 2' is 5.0"), # Floating point numbers
        ("1 + 2 - 3 * 4 / 5 + 6 ^ 2", "The result of '1 + 2 - 3 * 4 / 5 + 6 ^ 2' is 36.6") # Complex
    ])
    def test_valid_expressions(self, calculator, expression, expected_start):
        """Test valid arithmetic expressions."""
        result = calculator.execute(expression)
        assert result.startswith(expected_start) # Check start as result might have float precision variations

    @pytest.mark.parametrize("expression, expected_error_message_part", [
        ("10 / 0", "Error: Division by zero"),
        ("5 / (2 - 2)", "Error: Division by zero"),
        ("abc + 2", "Error evaluating expression 'abc + 2': Unsupported node type in expression: <class '_ast.Name'>"),
        ("2 +", "Error evaluating expression '2 +': unexpected EOF while parsing"), # SyntaxError
        ("1 ~ 2", "Error: Expression '1 ~ 2' contains invalid characters."), # Custom invalid char check
        ("os.system('echo hello')", "Error: Expression 'os.system('echo hello')' contains invalid characters."), # Invalid characters
        ("", "Error evaluating expression '': unexpected EOF while parsing"),
        ("++2", "Error evaluating expression '++2': invalid syntax"),
        ("2+3)", "Error evaluating expression '2+3)': unmatched ')'"),
        ("print('hello')", "Error evaluating expression 'print('hello')': Unsupported node type in expression: <class '_ast.Name'>")
    ])
    def test_error_conditions(self, calculator, expression, expected_error_message_part):
        """Test error conditions like division by zero and invalid syntax."""
        result = calculator.execute(expression)
        assert expected_error_message_part in result

    def test_empty_string_input_refined(self, calculator):
        """Test specific handling for empty or whitespace string if different from general syntax errors."""
        result = calculator.execute("")
        assert "Error evaluating expression '': unexpected EOF while parsing" in result

        result_space = calculator.execute("   ")
        # The tool's `params.replace('^', '**')` on "   " results in "   "
        # The allowed_chars check is `if not all(char in allowed_chars for char in safe_params):`
        # " " is in allowed_chars. So it passes this.
        # Then eval_expr("   ") is called. ast.parse("   ", mode='eval') raises "SyntaxError: unexpected EOF while parsing"
        assert "Error evaluating expression '   ': unexpected EOF while parsing" in result

    def test_tool_properties(self, calculator):
        """Test basic properties of the tool."""
        assert calculator.name == "CalculatorTool"
        assert "Evaluates basic arithmetic expressions" in calculator.description
        assert "2+3*4" in calculator.description # Example from description
