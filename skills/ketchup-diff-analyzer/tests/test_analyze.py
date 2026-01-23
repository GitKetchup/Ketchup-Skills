import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock dependencies
sys.modules["git"] = MagicMock()
sys.modules["langchain_anthropic"] = MagicMock()
sys.modules["langchain_openai"] = MagicMock()
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.messages"] = MagicMock()

from scripts.analyze import DiffAnalyzer, AnalysisConfig

class TestDiffAnalyzer(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict("os.environ", {"ANTHROPIC_API_KEY": "fake_key"})
        self.env_patcher.start()
        
        self.config = AnalysisConfig(detail_level="normal")

    def tearDown(self):
        self.env_patcher.stop()

    @patch("scripts.analyze.ChatAnthropic")
    def test_analyze_diff(self, mock_llm_class):
        # Mock LLM instance
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = "## Summary\nThis is a mock summary."
        mock_llm_class.return_value = mock_llm
        
        analyzer = DiffAnalyzer(self.config)
        result = analyzer.analyze("diff content")
        
        # Verify LLM called
        mock_llm.invoke.assert_called_once()
        self.assertIn("mock summary", result)

    @patch("scripts.analyze.ChatOpenAI")
    def test_openrouter_init(self, mock_openai_class):
        # Test OpenRouter initialization logic
        with patch.dict("os.environ", {
            "OPENROUTER_API_KEY": "sk-or-...",
            "ANTHROPIC_API_KEY": "" # Ensure only OpenRouter is set
        }):
            analyzer = DiffAnalyzer(self.config)
            
            # Verify ChatOpenAI initialized with OpenRouter base_url
            mock_openai_class.assert_called_with(
                model="anthropic/claude-3.5-sonnet",
                base_url="https://openrouter.ai/api/v1",
                api_key="sk-or-...",
                default_headers={"HTTP-Referer": "https://github.com/GitKetchup/ketchup-skills"}
            )

if __name__ == "__main__":
    unittest.main()
