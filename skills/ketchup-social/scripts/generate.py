"""
Ketchup Social - Launch Thread Generator
Creates viral social media content from changelogs.
"""

import os
import sys
import argparse
from typing import Optional
from dataclasses import dataclass

try:
    from langchain_anthropic import ChatAnthropic
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install langchain-anthropic langchain-openai")
    sys.exit(1)


TWITTER_PROMPT = """You are a developer marketing expert who writes viral Twitter threads.

Your threads follow this structure:
1. HOOK: Attention-grabbing first tweet (emoji, bold claim, curiosity gap)
2. CONTEXT: Why this matters (1-2 tweets)
3. DETAILS: Key features/changes (2-3 tweets)
4. PROOF: Stats, screenshots, or testimonials (1 tweet)
5. CTA: Call-to-action with link (1 tweet)

Rules:
- Each tweet max 280 characters
- Use emojis strategically (not every tweet)
- Include "🧵" in the first tweet
- End with relevant hashtags (2-3 max)
- Write in present tense, active voice
- Be specific with numbers and outcomes"""

LINKEDIN_PROMPT = """You are a developer marketing expert who writes engaging LinkedIn posts.

Your posts follow this structure:
1. HOOK: Strong opening line (no emojis, professional tone)
2. STORY: Brief narrative about the problem solved
3. SOLUTION: What you built and why it matters
4. DETAILS: 3-5 bullet points with key features
5. CTA: Professional call-to-action

Rules:
- Keep under 1300 characters for optimal visibility
- Use line breaks for readability
- One emoji per section maximum
- Professional but not boring
- End with a question to drive engagement"""


@dataclass
class SocialConfig:
    platform: str = "twitter"
    style: str = "hype"  # hype, professional, casual
    thread_length: int = 5
    include_cta: bool = True


class SocialGenerator:
    """Generates social media content from changelogs."""
    
    def __init__(self, config: Optional[SocialConfig] = None, model: Optional[str] = None):
        self.config = config or SocialConfig()
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
    
    def generate(self, content: str) -> str:
        """Generate social content from changelog/release notes."""
        
        system_prompt = TWITTER_PROMPT if self.config.platform == "twitter" else LINKEDIN_PROMPT
        
        style_instruction = {
            "hype": "Write with excitement and energy. This is a big deal!",
            "professional": "Write professionally but engagingly. Focus on business value.",
            "casual": "Write conversationally, like you're telling a friend about cool new features.",
        }.get(self.config.style, "")
        
        user_prompt = f"""Create a {self.config.platform} {'thread' if self.config.platform == 'twitter' else 'post'} 
for this release/changelog:

---
{content}
---

Style: {style_instruction}
{'Thread length: ' + str(self.config.thread_length) + ' tweets' if self.config.platform == 'twitter' else ''}
{'Include a clear CTA at the end.' if self.config.include_cta else 'No explicit CTA needed.'}

Separate each tweet with "---" on its own line."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        print(f"📱 Generating {self.config.platform} content...")
        response = self.llm.invoke(messages)
        
        return response.content


def main():
    parser = argparse.ArgumentParser(description="📱 Ketchup Social - Viral launch threads")
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--changelog", help="Path to changelog/release notes file")
    input_group.add_argument("--content", help="Direct content string")
    
    parser.add_argument("--platform", choices=["twitter", "linkedin"], default="twitter")
    parser.add_argument("--style", choices=["hype", "professional", "casual"], default="hype")
    parser.add_argument("--thread-length", type=int, default=5)
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--no-cta", action="store_true", help="Omit call-to-action")
    parser.add_argument("--model", help="LLM model to use")
    
    args = parser.parse_args()
    
    # Get content
    if args.changelog:
        with open(args.changelog, 'r') as f:
            content = f.read()
    else:
        content = args.content
    
    config = SocialConfig(
        platform=args.platform,
        style=args.style,
        thread_length=args.thread_length,
        include_cta=not args.no_cta
    )
    
    generator = SocialGenerator(config, model=args.model)
    result = generator.generate(content)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"✅ Saved to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
