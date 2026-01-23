import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock dependencies before import
sys.modules["PIL"] = MagicMock()
sys.modules["PIL.Image"] = MagicMock()
sys.modules["PIL.ImageDraw"] = MagicMock()
sys.modules["PIL.ImageFont"] = MagicMock()
sys.modules["pygments"] = MagicMock()
sys.modules["pygments.lexers"] = MagicMock()
sys.modules["pygments.formatters"] = MagicMock()
sys.modules["pygments.styles"] = MagicMock()

from scripts.render import CodeRenderer, RenderConfig

class TestCodeViz(unittest.TestCase):
    def setUp(self):
        self.config = RenderConfig(
            theme="monokai",
            font_size=12,
            padding=20,
            max_lines=10
        )
        self.renderer = CodeRenderer(self.config)

    @patch("scripts.render.highlight")
    def test_render_code(self, mock_highlight):
        # Mock highlight to return bytes
        mock_highlight.return_value = b"fake_image_data"
        
        # Mock open to avoid writing to disk
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            output = self.renderer.render_code(
                code="print('hello')",
                language="python",
                output_path="test_output.png"
            )
            
            # Verify highlight called
            mock_highlight.assert_called_once()
            
            # Verify file written
            mock_file.assert_called_with("test_output.png", "wb")
            mock_file().write.assert_called_with(b"fake_image_data")
            
            self.assertEqual(output, "test_output.png")

    @patch("scripts.render.highlight")
    def test_render_diff(self, mock_highlight):
        mock_highlight.return_value = b"fake_diff_image"
        
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            output = self.renderer.render_diff(
                diff_text="+ new line\n- old line",
                output_path="test_diff.png"
            )
            
            mock_highlight.assert_called_once()
            mock_file.assert_called_with("test_diff.png", "wb")
            
            self.assertEqual(output, "test_diff.png")

if __name__ == "__main__":
    unittest.main()
