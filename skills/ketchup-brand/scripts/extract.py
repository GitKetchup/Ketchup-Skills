"""
Ketchup Brand - Brand Asset Extractor
Extracts logos, colors, and fonts from websites.
"""

import os
import sys
import json
import argparse
import asyncio
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Missing dependency: playwright")
    print("Install with: pip install playwright && playwright install")
    sys.exit(1)

try:
    from colorthief import ColorThief
    from PIL import Image
    import requests
    from io import BytesIO
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install colorthief Pillow requests")
    sys.exit(1)


@dataclass
class BrandAssets:
    name: str
    url: str
    colors: Dict[str, str]
    logo: Optional[Dict[str, str]]
    fonts: Dict[str, str]
    palette: List[str]


class BrandExtractor:
    """Extracts brand assets from websites."""
    
    async def extract(self, url: str, download_assets: bool = False) -> BrandAssets:
        """Extract brand assets from a URL."""
        
        print(f"🎨 Extracting brand from: {url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Extract page title for brand name
            title = await page.title()
            brand_name = title.split(" - ")[0].split(" | ")[0].strip()
            
            # Extract colors from CSS
            colors = await self._extract_colors(page)
            
            # Find logo
            logo = await self._find_logo(page, url, download_assets)
            
            # Extract fonts
            fonts = await self._extract_fonts(page)
            
            await browser.close()
        
        # Generate palette
        palette = list(colors.values())[:5]
        
        return BrandAssets(
            name=brand_name,
            url=url,
            colors=colors,
            logo=logo,
            fonts=fonts,
            palette=palette
        )
    
    async def _extract_colors(self, page) -> Dict[str, str]:
        """Extract primary colors from the page."""
        
        colors = await page.evaluate("""() => {
            const styles = getComputedStyle(document.body);
            const colors = {};
            
            // Get background
            colors.background = styles.backgroundColor;
            colors.text = styles.color;
            
            // Look for common CSS variables
            const root = getComputedStyle(document.documentElement);
            const varNames = ['--primary', '--secondary', '--accent', '--brand'];
            varNames.forEach(name => {
                const val = root.getPropertyValue(name).trim();
                if (val) colors[name.replace('--', '')] = val;
            });
            
            // Sample prominent elements
            const header = document.querySelector('header, nav, .header, .navbar');
            if (header) {
                const headerStyles = getComputedStyle(header);
                if (headerStyles.backgroundColor !== 'rgba(0, 0, 0, 0)') {
                    colors.primary = headerStyles.backgroundColor;
                }
            }
            
            // Find buttons for accent
            const btn = document.querySelector('button, .btn, [class*="button"]');
            if (btn) {
                const btnStyles = getComputedStyle(btn);
                colors.accent = btnStyles.backgroundColor;
            }
            
            return colors;
        }""")
        
        # Clean up colors
        cleaned = {}
        for key, val in colors.items():
            if val and val != 'rgba(0, 0, 0, 0)':
                cleaned[key] = self._rgb_to_hex(val) if 'rgb' in val else val
        
        return cleaned
    
    async def _find_logo(self, page, base_url: str, download: bool) -> Optional[Dict]:
        """Find the logo on the page."""
        
        logo_info = await page.evaluate("""() => {
            // Common logo selectors
            const selectors = [
                'img[alt*="logo" i]',
                'img[src*="logo" i]',
                'img[class*="logo" i]',
                'a[class*="logo" i] img',
                'header img:first-of-type',
                '.logo img',
                '#logo img'
            ];
            
            for (const sel of selectors) {
                const img = document.querySelector(sel);
                if (img && img.src) {
                    return { src: img.src, alt: img.alt || '' };
                }
            }
            
            // Check for SVG logos
            const svgLogo = document.querySelector('svg[class*="logo" i], a[class*="logo" i] svg');
            if (svgLogo) {
                return { src: 'svg-inline', alt: 'logo' };
            }
            
            return null;
        }""")
        
        if not logo_info:
            return None
        
        logo_url = urljoin(base_url, logo_info.get('src', ''))
        
        result = {"url": logo_url}
        
        if download and logo_url != 'svg-inline':
            try:
                response = requests.get(logo_url, timeout=10)
                if response.ok:
                    ext = logo_url.split('.')[-1].split('?')[0] or 'png'
                    local_path = f"./assets/logo.{ext}"
                    os.makedirs("./assets", exist_ok=True)
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    result["local_path"] = local_path
            except:
                pass
        
        return result
    
    async def _extract_fonts(self, page) -> Dict[str, str]:
        """Extract font families from the page."""
        
        fonts = await page.evaluate("""() => {
            const body = getComputedStyle(document.body);
            const h1 = document.querySelector('h1');
            
            return {
                body: body.fontFamily,
                heading: h1 ? getComputedStyle(h1).fontFamily : body.fontFamily
            };
        }""")
        
        return fonts
    
    def _rgb_to_hex(self, rgb: str) -> str:
        """Convert rgb(r, g, b) to #RRGGBB."""
        try:
            if rgb.startswith('#'):
                return rgb
            nums = [int(x) for x in rgb.replace('rgb(', '').replace('rgba(', '').replace(')', '').split(',')[:3]]
            return '#{:02x}{:02x}{:02x}'.format(*nums).upper()
        except:
            return rgb


async def main_async(args):
    extractor = BrandExtractor()
    assets = await extractor.extract(args.url, args.download_assets)
    
    output = asdict(assets)
    
    if args.format == "json":
        result = json.dumps(output, indent=2)
    elif args.format == "css":
        result = f""":root {{
  --brand-primary: {assets.colors.get('primary', '#000')};
  --brand-secondary: {assets.colors.get('secondary', '#666')};
  --brand-accent: {assets.colors.get('accent', '#0066cc')};
  --brand-background: {assets.colors.get('background', '#fff')};
  --brand-text: {assets.colors.get('text', '#333')};
  --font-heading: {assets.fonts.get('heading', 'system-ui')};
  --font-body: {assets.fonts.get('body', 'system-ui')};
}}"""
    else:
        result = json.dumps(output, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"✅ Saved to: {args.output}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="🎨 Ketchup Brand - Extract brand assets")
    parser.add_argument("--url", required=True, help="Website URL to extract from")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["json", "css", "tailwind"], default="json")
    parser.add_argument("--download-assets", action="store_true", help="Download logo locally")
    
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
