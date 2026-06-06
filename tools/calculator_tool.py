import math
from langchain.tools import tool


@tool
def calculator_tool(expression: str) -> str:
    """
        Useful for performing mathematical calculations.
        Input should be a valid mathematical expression such as:
        '2+2', '25*48', 'sqrt(16)', 'sin(pi/2)'.
        """
    try:
        # Clean the input  remove surrounding quotes if any
        expression = expression.strip().strip("'\"")

        # Allow safe math functions via the math module
        # We restrict eval to only math functions for security
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("_")
        }
        allowed_names["abs"] = abs
        allowed_names["round"] = round

        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": {}}, allowed_names)

        return f"The result of '{expression}' is: {result}"

    except ZeroDivisionError:
        return "❌ Error: Cannot divide by zero."
    except SyntaxError:
        return f"❌ Error: '{expression}' is not a valid math expression."
    except Exception as e:
        return f"❌ Calculator error: {str(e)}"