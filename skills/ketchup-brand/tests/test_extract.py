import sys
import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Mock dependencies
sys.modules["playwright"] = MagicMock()
sys.modules["playwright.async_api"] = MagicMock()
sys.modules["colorthief"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["requests"] = MagicMock()

from scripts.extract import BrandExtractor, BrandAssets

class TestBrandExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = BrandExtractor()
        
    @patch("scripts.extract.async_playwright")
    def test_extract_brand(self, mock_playwright):
        # Setup complex async mock structure for Playwright
        mock_page = AsyncMock()
        mock_page.title.return_value = "Test Brand - Home"
        
        # Mock evaluate calls
        mock_page.evaluate.side_effect = [
            {"primary": "#000000", "background": "#ffffff"}, # _extract_colors
            {"src": "https://example.com/logo.png", "alt": "Logo"}, # _find_logo
            {"heading": "Arial", "body": "Helvetica"} # _extract_fonts
        ]
        
        mock_browser = AsyncMock()
        mock_browser.new_page.return_value = mock_page
        
        mock_p = AsyncMock()
        mock_p.chromium.launch.return_value = mock_browser
        
        # Configure context manager
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_p
        mock_playwright.return_value = mock_context
        
        # Run async test
        assets = asyncio.run(self.extractor.extract("https://example.com"))
        
        self.assertIsInstance(assets, BrandAssets)
        self.assertEqual(assets.name, "Test Brand")
        self.assertEqual(assets.colors["primary"], "#000000")
        self.assertEqual(assets.logo["url"], "https://example.com/logo.png")

if __name__ == "__main__":
    unittest.main()
