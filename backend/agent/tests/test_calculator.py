from django.test import SimpleTestCase

from agent.tools.calculator import calculator


class CalculatorTests(SimpleTestCase):

    def test_multiplication(self):
        self.assertEqual(
            calculator("25 * 4"),
            100,
        )

    def test_times_keyword(self):
        self.assertEqual(
            calculator("25 times 4"),
            100,
        )

    def test_multiplied_by_keyword(self):
        self.assertEqual(
            calculator("25 multiplied by 4"),
            100,
        )

    def test_addition(self):
        self.assertEqual(
            calculator("20 plus 30"),
            50,
        )

    def test_invalid_expression(self):
        result = calculator(
            "hello world"
        )

        self.assertIsInstance(
            result,
            str,
        )