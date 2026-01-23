import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Mock dependencies
sys.modules["elevenlabs"] = MagicMock()

from scripts.generate import VoiceGenerator, VoiceConfig

class TestVoiceGenerator(unittest.TestCase):
    def setUp(self):
        # Mock API environment variable
        self.env_patcher = patch.dict("os.environ", {"ELEVENLABS_API_KEY": "fake_key"})
        self.env_patcher.start()
        
        self.config = VoiceConfig(preset="storyteller")

    def tearDown(self):
        self.env_patcher.stop()

    @patch("scripts.generate.ElevenLabs")
    def test_generate_voice(self, mock_elevenlabs):
        # Setup mock client
        mock_client = MagicMock()
        mock_elevenlabs.return_value = mock_client
        
        # Mock audio stream response
        mock_client.text_to_speech.convert.return_value = [b"chunk1", b"chunk2"]
        
        generator = VoiceGenerator(self.config)
        
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            output = generator.generate(
                text="Hello world",
                output_path="test_voice.mp3"
            )
            
            # Verify convert called
            mock_client.text_to_speech.convert.assert_called_once()
            
            # Verify file write
            mock_file.assert_called_with("test_voice.mp3", "wb")
            handle = mock_file()
            handle.write.assert_any_call(b"chunk1")
            handle.write.assert_any_call(b"chunk2")
            
            self.assertEqual(output, "test_voice.mp3")

    def test_missing_api_key(self):
        # Remove API key
        with patch.dict("os.environ", clear=True):
             # Ensure ELEVENLABS_API_KEY is not present
             if "ELEVENLABS_API_KEY" in os.environ:
                 del os.environ["ELEVENLABS_API_KEY"]
                 
             with self.assertRaises(ValueError):
                 VoiceGenerator(self.config)

if __name__ == "__main__":
    unittest.main()
