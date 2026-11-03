import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mosaic.pipeline import SmartMosaicPipeline, CacheAdapter

class DummyCacheAdapter(CacheAdapter):
    def adapt(self, prompt):
        if "hit" in prompt:
            return {"response": "dummy-cached-response", "model": "cache-model", "cache_id": "123"}
        return None

class TestSmartMosaicPipeline(unittest.TestCase):
    def test_pipeline_no_cache_hit_uses_model_selector(self):
        pipeline = SmartMosaicPipeline()
        result = pipeline.run("dummy prompt no hit")

        self.assertEqual(result['source'], 'regeneration')
        self.assertEqual(result['selected_model'], 'selected-model-1')
        self.assertNotEqual(result['selected_model'], 'gpt-4')

    def test_pipeline_cache_hit_accepted(self):
        pipeline = SmartMosaicPipeline()
        pipeline.cache_adapter = DummyCacheAdapter()

        # Default behavior of CacheVerifierAgent.should_accept_cache is True
        result = pipeline.run("dummy prompt hit")

        self.assertEqual(result['source'], 'cache')
        self.assertEqual(result['selected_model'], 'cache-model')

    def test_pipeline_cache_hit_rejected(self):
        pipeline = SmartMosaicPipeline()
        pipeline.cache_adapter = DummyCacheAdapter()

        # Override cache verifier to reject cache
        pipeline.cache_verifier.should_accept_cache = lambda cached_response, prompt: False

        result = pipeline.run("dummy prompt hit rejected")

        self.assertEqual(result['source'], 'regeneration')
        self.assertEqual(result['selected_model'], 'selected-model-1')
        self.assertNotEqual(result['selected_model'], 'gpt-4')

if __name__ == '__main__':
    unittest.main()
