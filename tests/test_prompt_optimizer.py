import unittest
from mosaic.prompt_optimizer import PromptOptimizer
from mosaic.model_selector import ModelSelector

class TestPromptOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = PromptOptimizer()
        self.selector = ModelSelector()

    def test_short_prompt_enhancement(self):
        prompt = "おはよう"
        optimized = self.optimizer.optimize(prompt)
        self.assertIn("You are a highly intelligent and helpful AI assistant.", optimized)
        self.assertIn("Please respond in a clear, concise, and natural Japanese tone.", optimized)
        self.assertIn("おはよう", optimized)

    def test_mask_preservation(self):
        prompt = "こんにちは、<MASK_PERSON_1>さん"
        optimized = self.optimizer.optimize(prompt)
        self.assertIn("<MASK_PERSON_1>", optimized)

    def test_model_selection_general(self):
        model = self.selector.select_model(category='general')
        self.assertEqual(model, 'gemini-3.8-flash')

    def test_model_selection_complex(self):
        model = self.selector.select_model(category='complex_reasoning')
        self.assertEqual(model, 'claude-sonnet-5-5')

if __name__ == '__main__':
    unittest.main()
