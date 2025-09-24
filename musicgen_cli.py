#!/usr/bin/env python3
"""
Command-line interface for MusicGen
Usage: python musicgen_cli.py "prompt" --duration 10 --model small
"""

import argparse
import sys
from musicgen_api import generate_music_with_musicgen, get_available_models
from config import MUSICGEN_CONFIG

def main():
    parser = argparse.ArgumentParser(description='Generate music using MusicGen')
    parser.add_argument('prompt', type=str, help='Text prompt describing the music')
    parser.add_argument('--duration', type=float, default=MUSICGEN_CONFIG['DEFAULT_DURATION'],
                       help=f'Duration in seconds (default: {MUSICGEN_CONFIG["DEFAULT_DURATION"]})')
    parser.add_argument('--model', type=str, default=MUSICGEN_CONFIG['DEFAULT_MODEL'],
                       choices=['small', 'medium', 'large', 'melody'],
                       help=f'Model size (default: {MUSICGEN_CONFIG["DEFAULT_MODEL"]})')
    parser.add_argument('--temperature', type=float, default=MUSICGEN_CONFIG['DEFAULT_TEMPERATURE'],
                       help=f'Sampling temperature (default: {MUSICGEN_CONFIG["DEFAULT_TEMPERATURE"]})')
    parser.add_argument('--guidance', type=float, default=MUSICGEN_CONFIG['DEFAULT_GUIDANCE_SCALE'],
                       help=f'Guidance scale (default: {MUSICGEN_CONFIG["DEFAULT_GUIDANCE_SCALE"]})')
    parser.add_argument('--list-models', action='store_true', help='List available models')
    
    args = parser.parse_args()
    
    if args.list_models:
        print("\nAvailable MusicGen Models:")
        print("-" * 60)
        for model in get_available_models():
            print(f"  {model['name']:<20} Size: {model['size']:<10} {model['description']}")
        print()
        return
    
    print(f"\n🎵 Generating music...")
    print(f"   Prompt: {args.prompt}")
    print(f"   Duration: {args.duration}s")
    print(f"   Model: {args.model}")
    print(f"   Temperature: {args.temperature}")
    print(f"   Guidance: {args.guidance}")
    print()
    
    try:
        result = generate_music_with_musicgen(
            prompt=args.prompt,
            duration=args.duration,
            temperature=args.temperature,
            guidance_scale=args.guidance,
            model_size=args.model
        )
        
        print(f"✅ Success! Generated: {result['filename']}")
        print(f"   Location: {result['filepath']}")
        print(f"   Sample rate: {result['sample_rate']} Hz")
        print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()