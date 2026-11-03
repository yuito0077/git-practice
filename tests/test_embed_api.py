import unittest
from fastapi.testclient import TestClient
from server import app
import os

class TestEmbedApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Ensure static folder and file exists for the test
        if not os.path.exists('static'):
            os.makedirs('static')
        if not os.path.exists('static/embed.html'):
            with open('static/embed.html', 'w') as f:
                f.write('<html></html>')

    def test_get_embed(self):
        response = self.client.get('/embed')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('text/html' in response.headers['content-type'])

    def test_post_api_ask_json(self):
        response = self.client.post('/api/ask', json={'prompt': 'test json'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['answer'], 'This is a response to: test json')
        self.assertEqual(data['model'], 'dummy-model-v1')
        self.assertEqual(data['cost'], 0.0)
        self.assertFalse(data['is_cache_hit'])
        self.assertEqual(data['record_id'], 'rec_12345')
        self.assertEqual(data['duration_sec'], 0.5)

    def test_post_api_ask_text(self):
        response = self.client.post('/api/ask', json={'prompt': 'test text', 'format': 'text'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('text/plain' in response.headers['content-type'])
        self.assertEqual(response.text, 'This is a response to: test text')

if __name__ == '__main__':
    unittest.main()
