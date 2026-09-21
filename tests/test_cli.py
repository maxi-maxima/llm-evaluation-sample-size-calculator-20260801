import unittest

from llm_evaluation_sample_size_calculator_20260801.cli import cost, estimate, plan


class EstimateTests(unittest.TestCase):
    def test_estimate_and_cost_are_positive(self):
        n = estimate(0.7, 0.8)
        self.assertGreater(n, 100)
        self.assertGreater(cost(n, 1000, 500, 1, 5), 0)

    def test_plan_accepts_csv_style_row(self):
        result = plan({'name': 'routing', 'baseline': '0.72', 'target': '0.80', 'input_tokens': '1500', 'output_tokens': '600', 'input_price': '1', 'output_price': '5', 'candidates': '3'})
        self.assertEqual(result['name'], 'routing')
        self.assertEqual(result['candidates'], 3)
        self.assertGreater(result['estimated_cost_usd'], 0)


if __name__ == '__main__':
    unittest.main()
