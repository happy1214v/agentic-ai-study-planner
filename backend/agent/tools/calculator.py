import re


def calculator(expression):
    try:
        # Extract mathematical expression from the sentence
        match = re.search(r"[\d+\-*/().\s]+", expression)

        if not match:
            return "No mathematical expression found"

        math_expression = match.group().strip()

        result = eval(math_expression)

        return result

    except Exception as e:
        return f"Error: {e}"