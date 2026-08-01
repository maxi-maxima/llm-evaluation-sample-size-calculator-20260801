import unittest

from llm_evaluation_sample_size_calculator_20260801.cli import cost, estimate


class EstimateTests(unittest.TestCase):
    def test_estimate_and_cost_are_positive(self):
        n = estimate(0.7, 0.8)
        self.assertGreater(n, 100)
        self.assertGreater(cost(n, 1000, 500, 1, 5), 0)


if __name__ == '__main__':
    unittest.main()
