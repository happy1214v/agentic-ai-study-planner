import ast
import operator
import re


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def calculate_node(node):
    if isinstance(node, ast.Expression):
        return calculate_node(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        operator_function = OPERATORS.get(type(node.op))

        if not operator_function:
            raise ValueError("Unsupported operator")

        left = calculate_node(node.left)
        right = calculate_node(node.right)

        return operator_function(left, right)

    if isinstance(node, ast.UnaryOp):
        value = calculate_node(node.operand)

        if isinstance(node.op, ast.UAdd):
            return +value

        if isinstance(node.op, ast.USub):
            return -value

        raise ValueError("Unsupported unary operator")

    raise ValueError("Invalid mathematical expression")


def calculator(expression):
    try:
        expression = expression.lower()

        # Natural language operators → mathematical operators
        replacements = [
            (r"\bplus\b", "+"),
            (r"\badd\b", "+"),
            (r"\bminus\b", "-"),
            (r"\bsubtract\b", "-"),
            (r"\btimes\b", "*"),
            (r"\bmultiply\b", "*"),
            (r"\bdivided by\b", "/"),
            (r"\bdivide\b", "/"),
            (r"\bmodulo\b", "%"),
            (r"\bmod\b", "%"),
            (r"\bpower of\b", "**"),
        ]

        for pattern, replacement in replacements:
            expression = re.sub(pattern, replacement, expression)

        # Extract mathematical expression
        match = re.search(r"\d[\d+\-*/().%\s]*", expression)

        if not match:
            return "No mathematical expression found"

        math_expression = match.group().strip()

        tree = ast.parse(math_expression, mode="eval")

        return calculate_node(tree)

    except Exception as e:
        return f"Error: {e}"