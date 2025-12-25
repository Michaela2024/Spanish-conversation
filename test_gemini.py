import sys
import os

# Add the current folder to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversation.gemini_client import call_gemini_api


# test_gemini.py
import unittest
from conversation.gemini_client import call_gemini_api

class TestGeminiClient(unittest.TestCase):

    def test_greeting(self):
        """Test that the AI responds with a greeting."""
        response = call_gemini_api("greet the user", use_api=False)
        self.assertIn("Hello", response, "Greeting test failed")

    def test_grammar_correction(self):
        """Test grammar correction scenario."""
        response = call_gemini_api("grammar: i am lernig Python", use_api=False)
        self.assertIn("Corrected sentence", response, "Grammar test failed")

    def test_vocabulary(self):
        """Test vocabulary explanation scenario."""
        response = call_gemini_api("define ubiquitous", use_api=False)
        self.assertIn("means", response, "Vocabulary test failed")

    def test_generic_response(self):
        """Test fallback for unknown prompts."""
        response = call_gemini_api("random prompt", use_api=False)
        self.assertEqual(response, "This is a generic mock AI response.", "Generic response test failed")

if __name__ == "__main__":
    unittest.main()
