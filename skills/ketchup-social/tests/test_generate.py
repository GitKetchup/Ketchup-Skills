import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock dependencies
sys.modules["langchain_anthropic"] = MagicMock()
sys.modules["langchain_openai"] = MagicMock()
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.messages"] = MagicMock()

from scripts.generate import SocialGenerator, SocialConfig

class TestSocialGenerator(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict("os.environ", {"OPENAI_API_KEY": "fake_key"})
        self.env_patcher.start()
        
        self.config = SocialConfig(platform="twitter", thread_length=3)

    def tearDown(self):
        self.env_patcher.stop()

    @patch("scripts.generate.ChatOpenAI")
    def test_generate_thread(self, mock_llm_class):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = "Tweet 1\n---\nTweet 2\n---\nTweet 3"
        mock_llm_class.return_value = mock_llm
        
        generator = SocialGenerator(self.config)
        result = generator.generate("Release notes content")
        
        mock_llm.invoke.assert_called_once()
        self.assertIn("Tweet 1", result)
        self.assertIn("Tweet 3", result)

    @patch("scripts.generate.ChatOpenAI")
    def test_linkedin_platform(self, mock_llm_class):
        # Setup mock first
        mock_llm = MagicMock()
        mock_llm_class.return_value = mock_llm
        
        # Get reference to the mocked SystemMessage class
        MockSystemMessage = sys.modules["langchain_core.messages"].SystemMessage
        MockSystemMessage.reset_mock()
        
        config = SocialConfig(platform="linkedin")
        generator = SocialGenerator(config)
        
        generator.generate("content")
        
        # Verify SystemMessage was initialized with LinkedIn prompt
        # We check all calls to SystemMessage constructor
        found_linkedin = False
        for call in MockSystemMessage.call_args_list:
            # call.kwargs['content'] or call.args[0] if positional
            content = call.kwargs.get('content')
            if content and "LinkedIn" in content:
                found_linkedin = True
                break
        
        self.assertTrue(found_linkedin, "SystemMessage should be initialized with LinkedIn prompt")

if __name__ == "__main__":
    unittest.main()
