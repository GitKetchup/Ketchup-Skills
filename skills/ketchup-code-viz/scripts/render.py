"""
Ketchup Code Viz - Beautiful Code Image Generator
Renders syntax-highlighted code diffs as shareable images.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List, Tuple
from dataclasses import dataclass

try:
    from PIL import Image, ImageDraw, ImageFont
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import ImageFormatter
    from pygments.styles import get_style_by_name
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install Pillow pygments")
    sys.exit(1)


@dataclass
class RenderConfig:
    theme: str = "monokai"
    font_size: int = 14
    padding: int = 32
    max_lines: int = 30
    show_line_numbers: bool = True
    show_filename: bool = True


class CodeRenderer:
    """Renders code snippets as beautiful images."""
    
    # Theme to Pygments style mapping
    THEME_MAP = {
        "github-dark": "github-dark",
        "github-light": "github",
        "dracula": "dracula",
        "nord": "nord",
        "one-dark-pro": "one-dark",
        "monokai": "monokai",
    }
    
    def __init__(self, config: Optional[RenderConfig] = None):
        self.config = config or RenderConfig()
        
    def render_code(
        self,
        code: str,
        language: str = "python",
        filename: Optional[str] = None,
        output_path: str = "code.png"
    ) -> str:
        """Render code to an image file."""
        
        # Get lexer for syntax highlighting
        try:
            lexer = get_lexer_by_name(language)
        except:
            lexer = guess_lexer(code)
        
        # Get Pygments style
        style_name = self.THEME_MAP.get(self.config.theme, "monokai")
        
        # Truncate if too long
        lines = code.split('\n')
        if len(lines) > self.config.max_lines:
            lines = lines[:self.config.max_lines]
            lines.append(f"... ({len(code.split(chr(10))) - self.config.max_lines} more lines)")
            code = '\n'.join(lines)
        
        # Create image formatter
        formatter = ImageFormatter(
            style=style_name,
            font_size=self.config.font_size,
            line_numbers=self.config.show_line_numbers,
            line_pad=4,
            image_pad=self.config.padding,
        )
        
        # Render to image
        img_data = highlight(code, lexer, formatter)
        
        # Save to file
        with open(output_path, 'wb') as f:
            f.write(img_data)
        
        print(f"✅ Rendered to: {output_path}")
        return output_path
    
    def render_diff(
        self,
        diff_text: str,
        filename: Optional[str] = None,
        output_path: str = "diff.png"
    ) -> str:
        """Render a git diff with +/- highlighting."""
        
        # Use diff lexer for proper coloring
        lexer = get_lexer_by_name("diff")
        
        # Get style
        style_name = self.THEME_MAP.get(self.config.theme, "monokai")
        
        # Truncate
        lines = diff_text.split('\n')
        if len(lines) > self.config.max_lines:
            lines = lines[:self.config.max_lines]
            lines.append(f"... ({len(diff_text.split(chr(10))) - self.config.max_lines} more lines)")
            diff_text = '\n'.join(lines)
        
        # Create formatter
        formatter = ImageFormatter(
            style=style_name,
            font_size=self.config.font_size,
            line_numbers=self.config.show_line_numbers,
            line_pad=4,
            image_pad=self.config.padding,
        )
        
        # Render
        img_data = highlight(diff_text, lexer, formatter)
        
        with open(output_path, 'wb') as f:
            f.write(img_data)
        
        print(f"✅ Rendered diff to: {output_path}")
        return output_path


def get_commit_diff(repo_path: str, commit_sha: str, file_path: Optional[str] = None) -> str:
    """Extract diff from a specific commit."""
    try:
        from git import Repo
        repo = Repo(repo_path)
        
        commit = repo.commit(commit_sha)
        parent = commit.parents[0] if commit.parents else None
        
        if parent:
            diff = repo.git.diff(parent.hexsha, commit.hexsha, file_path) if file_path else repo.git.diff(parent.hexsha, commit.hexsha)
        else:
            diff = repo.git.show(commit.hexsha, file_path, format="") if file_path else repo.git.show(commit.hexsha, format="")
        
        return diff
    except ImportError:
        print("⚠️ GitPython not installed. Use --diff flag instead.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="🥑 Code Guacamole - Beautiful code images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Render a file
  python render.py --code "print('hello')" --language python --output hello.png
  
  # Render a diff
  python render.py --diff "$(git diff HEAD~1)" --output changes.png
  
  # Render from commit
  python render.py --repo . --commit abc123 --file src/auth.ts --output auth.png
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--code", help="Raw code string to render")
    input_group.add_argument("--diff", help="Raw diff text to render")
    input_group.add_argument("--commit", help="Commit SHA to extract diff from (requires --repo)")
    
    # Additional options
    parser.add_argument("--repo", help="Path to git repository")
    parser.add_argument("--file", help="Specific file to extract from commit")
    parser.add_argument("--language", default="python", help="Language for syntax highlighting")
    parser.add_argument("--output", "-o", default="code.png", help="Output file path")
    parser.add_argument("--theme", default="monokai", 
                       choices=["github-dark", "github-light", "dracula", "nord", "one-dark-pro", "monokai"],
                       help="Color theme")
    parser.add_argument("--font-size", type=int, default=14, help="Font size")
    parser.add_argument("--max-lines", type=int, default=30, help="Max lines to show")
    parser.add_argument("--no-line-numbers", action="store_true", help="Hide line numbers")
    
    args = parser.parse_args()
    
    # Build config
    config = RenderConfig(
        theme=args.theme,
        font_size=args.font_size,
        max_lines=args.max_lines,
        show_line_numbers=not args.no_line_numbers,
    )
    
    renderer = CodeRenderer(config)
    
    # Route to appropriate render method
    if args.code:
        renderer.render_code(args.code, args.language, output_path=args.output)
    elif args.diff:
        renderer.render_diff(args.diff, output_path=args.output)
    elif args.commit:
        if not args.repo:
            print("❌ --repo is required when using --commit")
            sys.exit(1)
        diff_text = get_commit_diff(args.repo, args.commit, args.file)
        renderer.render_diff(diff_text, filename=args.file, output_path=args.output)


if __name__ == "__main__":
    main()
