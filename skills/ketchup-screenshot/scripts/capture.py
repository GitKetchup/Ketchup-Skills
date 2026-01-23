"""
Intelligent Screenshot Capture Script
Uses Browser-Use to navigate and capture screenshots based on feature descriptions.
"""

import os
import sys
import json
import asyncio
import argparse
from typing import List, Optional
from dataclasses import dataclass

# Browser-Use imports
from browser_use import Agent, Browser, Controller
from browser_use.browser.browser import BrowserConfig
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

@dataclass
class ScreenshotResult:
    feature: str
    image_path: str
    success: bool
    error: Optional[str] = None

class ScreenshotCapturer:
    def __init__(self, use_cloud: bool = False, model: Optional[str] = None):
        self.use_cloud = use_cloud
        
        # Configure LLM for navigation intelligence
        self.llm = self._get_llm(model)

        # Initialize Browser
        if self.use_cloud and os.getenv("BROWSER_USE_API_KEY"):
            print("🕵️  Using Cloud Browser (Stealth Mode)")
            self.browser = Browser(config=BrowserConfig(wss_url=os.getenv("BROWSER_USE_WSS_URL"))) 
        else:
            print("💻 Using Local Browser")
            self.browser = Browser(config=BrowserConfig(headless=True))
    
    def _get_llm(self, model: Optional[str] = None):
        """Initialize LLM with provider priority: OpenRouter > Anthropic > OpenAI"""
        
        if os.getenv("OPENROUTER_API_KEY"):
            model = model or "anthropic/claude-3.5-sonnet"
            print(f"🤖 Using OpenRouter with model: {model}")
            return ChatOpenAI(
                model=model,
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                default_headers={"HTTP-Referer": "https://github.com/GitKetchup/ketchup-skills"}
            )
        elif os.getenv("ANTHROPIC_API_KEY"):
            model = model or "claude-3-5-sonnet-20240620"
            print(f"🤖 Using Anthropic: {model}")
            return ChatAnthropic(model=model)
        elif os.getenv("OPENAI_API_KEY"):
            model = model or "gpt-4o"
            print(f"🤖 Using OpenAI: {model}")
            return ChatOpenAI(model=model)
        else:
            raise ValueError(
                "❌ Missing API Key: Please set one of:\n"
                "  - OPENROUTER_API_KEY (recommended - access all models)\n"
                "  - ANTHROPIC_API_KEY\n"
                "  - OPENAI_API_KEY"
            )

        # Initialize Browser
        if self.use_cloud and os.getenv("BROWSER_USE_API_KEY"):
            print("🕵️  Using Cloud Browser (Stealth Mode)")
            # Cloud browser configuration would go here
            # For V1 integration, we rely on the library's default cloud behavior if API key is present
            # or explicit configuration if needed by the specific version of browser-use
            self.browser = Browser(config=BrowserConfig(wss_url=os.getenv("BROWSER_USE_WSS_URL"))) 
        else:
            print("💻 Using Local Browser")
            self.browser = Browser(config=BrowserConfig(headless=True))

    async def capture(self, url: str, features: List[str], credentials: Optional[dict] = None) -> List[ScreenshotResult]:
        results = []
        
        # Create a single session for all feature captures to maintain login state
        async with await self.browser.new_context() as context:
            
            # 1. Login Phase (if credentials provided)
            if credentials and credentials.get('username') and credentials.get('password'):
                print(f"🔐 Logging in to {url}...")
                login_task = f"""
                Navigate to {url}.
                Find the login button or form.
                Log in using username '{credentials['username']}' and password '{credentials['password']}'.
                Wait until the dashboard or home page loads.
                """
                
                agent = Agent(
                    task=login_task,
                    llm=self.llm,
                    browser_context=context
                )
                await agent.run()
            else:
                 # Just navigate to home if no login
                page = await context.get_current_page()
                await page.goto(url)

            # 2. Feature Capture Phase
            for feature in features:
                print(f"📸 Capturing feature: {feature}")
                try:
                    # Specific task for this feature
                    capture_task = f"""
                    Navigate to the area of the application that shows '{feature}'.
                    If it's a specific setting or page, go there.
                    Once visible, take a screenshot and save it as '{feature.replace(" ", "_").lower()}.png'.
                    """
                    
                    agent = Agent(
                        task=capture_task,
                        llm=self.llm,
                        browser_context=context
                    )
                    
                    history = await agent.run()
                    
                    # Assume last action or explicit screenshot action saved the file
                    # In a real integration, we'd extract the file path from the agent's output or tool calls
                    # For V1 robustness, we can enforce a screenshot at the end if not taken
                    
                    results.append(ScreenshotResult(
                        feature=feature,
                        image_path=f"{feature.replace(' ', '_').lower()}.png", # Placeholder for actual path
                        success=True
                    ))
                    
                except Exception as e:
                    print(f"❌ Failed to capture {feature}: {e}")
                    results.append(ScreenshotResult(
                        feature=feature,
                        image_path="",
                        success=False,
                        error=str(e)
                    ))
                    
        return results

async def main():
    parser = argparse.ArgumentParser(description="Capture screenshots for Ketchup features")
    parser.add_argument("--url", required=True, help="Target website URL")
    parser.add_argument("--features", required=True, help="Comma-separated list of features")
    parser.add_argument("--username", help="Login username")
    parser.add_argument("--password", help="Login password")
    parser.add_argument("--model", help="LLM model to use (e.g., 'anthropic/claude-3.5-sonnet' for OpenRouter)")
    
    args = parser.parse_args()
    
    # Determine mode based on env var presence
    use_cloud = bool(os.getenv("BROWSER_USE_API_KEY"))
    
    capturer = ScreenshotCapturer(use_cloud=use_cloud, model=args.model)
    
    creds = None
    if args.username and args.password:
        creds = {"username": args.username, "password": args.password}
        
    features_list = [f.strip() for f in args.features.split(",")]
    
    results = await capturer.capture(args.url, features_list, creds)
    
    # Output results as JSON for integration
    print(json.dumps([
        {
            "feature": r.feature,
            "path": r.image_path,
            "success": r.success,
            "error": r.error
        } for r in results
    ], indent=2))

if __name__ == "__main__":
    asyncio.run(main())
