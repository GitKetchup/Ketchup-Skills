"""
Ketchup Diff Analyzer - Intelligent Git Diff Summarization
Uses LLMs to explain code changes in plain English.
"""

import os
import sys
import argparse
from typing import Optional
from dataclasses import dataclass

try:
    from git import Repo
except ImportError:
    Repo = None

# LLM imports
try:
    from langchain_anthropic import ChatAnthropic
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install langchain-anthropic langchain-openai")
    sys.exit(1)


SYSTEM_PROMPT = """You are a senior software engineer analyzing git diffs.
Your job is to explain code changes in clear, concise language.

When analyzing diffs:
1. Identify the PURPOSE of the change (why was this done?)
2. Summarize WHAT changed at a high level
3. Flag any BREAKING CHANGES that affect APIs or schemas
4. Classify the change type (feature, fix, refactor, docs, etc.)
5. Assess the RISK level (low, medium, high)

Output format: Markdown with sections for Summary, Changes, Breaking Changes, and Classification.
Be concise but thorough. Developers should understand the change without reading the diff."""


@dataclass
class AnalysisConfig:
    detail_level: str = "normal"  # brief, normal, verbose
    format: str = "md"  # md, json, text
    focus: str = "all"  # all, breaking, features


class DiffAnalyzer:
    """Analyzes git diffs using LLMs."""
    
    def __init__(self, config: Optional[AnalysisConfig] = None, model: Optional[str] = None):
        self.config = config or AnalysisConfig()
        self.llm = self._get_llm(model)
    
    def _get_llm(self, model: Optional[str] = None):
        """Initialize LLM with provider priority: OpenRouter > Anthropic > OpenAI"""
        
        if os.getenv("OPENROUTER_API_KEY"):
            model = model or "anthropic/claude-3.5-sonnet"
            return ChatOpenAI(
                model=model,
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                default_headers={"HTTP-Referer": "https://github.com/GitKetchup/ketchup-skills"}
            )
        elif os.getenv("ANTHROPIC_API_KEY"):
            model = model or "claude-3-5-sonnet-20240620"
            return ChatAnthropic(model=model)
        elif os.getenv("OPENAI_API_KEY"):
            model = model or "gpt-4o"
            return ChatOpenAI(model=model)
        else:
            raise ValueError(
                "❌ Missing API Key: Please set one of:\n"
                "  - OPENROUTER_API_KEY (recommended)\n"
                "  - ANTHROPIC_API_KEY\n"
                "  - OPENAI_API_KEY"
            )
    
    def analyze(self, diff_text: str) -> str:
        """Analyze a diff and return a summary."""
        
        # Truncate very long diffs
        max_chars = 15000
        if len(diff_text) > max_chars:
            diff_text = diff_text[:max_chars] + "\n\n... (diff truncated for analysis)"
        
        # Build prompt based on detail level
        detail_instruction = {
            "brief": "Keep the summary under 100 words.",
            "normal": "Provide a balanced summary with key details.",
            "verbose": "Provide a comprehensive analysis with all relevant details.",
        }.get(self.config.detail_level, "")
        
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"""Analyze this git diff:

```diff
{diff_text}
```

{detail_instruction}""")
        ]
        
        print("🔍 Analyzing diff...")
        response = self.llm.invoke(messages)
        
        return response.content
    
    def analyze_repo(
        self,
        repo_path: str,
        from_ref: str,
        to_ref: str = "HEAD"
    ) -> str:
        """Analyze changes between two refs in a repo."""
        
        if Repo is None:
            raise ImportError("GitPython required. Install with: pip install GitPython")
        
        repo = Repo(repo_path)
        diff_text = repo.git.diff(from_ref, to_ref)
        
        if not diff_text:
            return "No changes found between the specified refs."
        
        return self.analyze(diff_text)


def main():
    parser = argparse.ArgumentParser(
        description="🔍 Ketchup Diff Analyzer - AI-powered diff summaries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze between tags
  python analyze.py --repo . --from v1.0.0 --to v1.1.0
  
  # Analyze from stdin
  git diff HEAD~5 | python analyze.py --stdin
  
  # Brief summary
  python analyze.py --repo . --from main --detail brief
        """
    )
    
    # Input options
    parser.add_argument("--repo", help="Path to git repository")
    parser.add_argument("--from", dest="from_ref", help="Starting ref (tag, branch, commit)")
    parser.add_argument("--to", default="HEAD", help="Ending ref")
    parser.add_argument("--stdin", action="store_true", help="Read diff from stdin")
    
    # Output options
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["md", "json", "text"], default="md")
    parser.add_argument("--detail", choices=["brief", "normal", "verbose"], default="normal")
    parser.add_argument("--model", help="LLM model to use")
    
    args = parser.parse_args()
    
    config = AnalysisConfig(detail_level=args.detail, format=args.format)
    analyzer = DiffAnalyzer(config, model=args.model)
    
    # Get diff
    if args.stdin:
        diff_text = sys.stdin.read()
        result = analyzer.analyze(diff_text)
    elif args.repo and args.from_ref:
        result = analyzer.analyze_repo(args.repo, args.from_ref, args.to)
    else:
        parser.error("Either --stdin or (--repo and --from) is required")
        return
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"✅ Saved to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
