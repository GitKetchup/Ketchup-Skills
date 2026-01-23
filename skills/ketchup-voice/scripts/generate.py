"""
Ketchup Voice - Professional Voiceover Generator
Uses ElevenLabs to create studio-quality narration.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    from elevenlabs import ElevenLabs, VoiceSettings
except ImportError:
    print("❌ Missing dependency: elevenlabs")
    print("Install with: pip install elevenlabs")
    sys.exit(1)


# Voice preset configurations
VOICE_PRESETS = {
    "storyteller": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.3,
    },
    "professional": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "stability": 0.7,
        "similarity_boost": 0.8,
        "style": 0.2,
    },
    "hype": {
        "voice_id": "yoZ06aMxZJJ28mfd3POQ",  # Sam
        "stability": 0.3,
        "similarity_boost": 0.9,
        "style": 0.8,
    },
    "calm": {
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella
        "stability": 0.8,
        "similarity_boost": 0.6,
        "style": 0.1,
    },
    "documentary": {
        "voice_id": "VR6AewLTigWG4xSOukaG",  # Arnold
        "stability": 0.6,
        "similarity_boost": 0.7,
        "style": 0.4,
    },
}


@dataclass
class VoiceConfig:
    preset: str = "storyteller"
    speed: float = 1.0
    stability: float = 0.5
    clarity: float = 0.75
    output_format: str = "mp3"


class VoiceGenerator:
    """Generates voiceovers using ElevenLabs."""
    
    def __init__(self, config: Optional[VoiceConfig] = None):
        self.config = config or VoiceConfig()
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ Missing API Key: Please set ELEVENLABS_API_KEY environment variable.\n"
                "Get your key at: https://elevenlabs.io"
            )
        
        self.client = ElevenLabs(api_key=api_key)
    
    def generate(
        self,
        text: str,
        output_path: str = "narration.mp3",
        preset: Optional[str] = None
    ) -> str:
        """Generate voiceover from text."""
        
        preset_name = preset or self.config.preset
        preset_config = VOICE_PRESETS.get(preset_name, VOICE_PRESETS["storyteller"])
        
        print(f"🎙️ Generating voiceover with '{preset_name}' voice...")
        print(f"   Text length: {len(text)} characters")
        
        # Generate audio
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=preset_config["voice_id"],
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=preset_config.get("stability", self.config.stability),
                similarity_boost=preset_config.get("similarity_boost", self.config.clarity),
                style=preset_config.get("style", 0.5),
            ),
        )
        
        # Save to file
        with open(output_path, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"✅ Saved to: {output_path}")
        return output_path
    
    def list_voices(self) -> list:
        """List available voices."""
        voices = self.client.voices.get_all()
        return [(v.voice_id, v.name) for v in voices.voices]


def main():
    parser = argparse.ArgumentParser(
        description="🎙️ Ketchup Voice - Professional voiceovers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from text
  python generate.py --script "Hello world!" --output hello.mp3
  
  # Generate from file
  python generate.py --file script.txt --voice hype --output launch.mp3
  
  # List available voices
  python generate.py --list-voices
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--script", help="Text to convert to speech")
    input_group.add_argument("--file", help="Path to text file")
    input_group.add_argument("--list-voices", action="store_true", help="List available voices")
    
    # Voice options
    parser.add_argument("--voice", default="storyteller",
                       choices=list(VOICE_PRESETS.keys()),
                       help="Voice preset to use")
    parser.add_argument("--output", "-o", default="narration.mp3", help="Output file path")
    parser.add_argument("--speed", type=float, default=1.0, help="Playback speed (0.5-2.0)")
    
    args = parser.parse_args()
    
    # Handle list voices
    if args.list_voices:
        config = VoiceConfig()
        generator = VoiceGenerator(config)
        voices = generator.list_voices()
        print("\n🎤 Available Voices:")
        for voice_id, name in voices:
            print(f"  - {name} ({voice_id})")
        return
    
    # Require input
    if not args.script and not args.file:
        parser.error("Either --script or --file is required")
    
    # Get text
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    else:
        text = args.script
    
    # Generate
    config = VoiceConfig(preset=args.voice, speed=args.speed)
    generator = VoiceGenerator(config)
    generator.generate(text, output_path=args.output, preset=args.voice)


if __name__ == "__main__":
    main()
