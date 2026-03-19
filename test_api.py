#!/usr/bin/env python3
"""
Test script for emoji translator API
Run this to verify your setup is correct
"""

import os
from dotenv import load_dotenv
from utils.emoji_api import translate_text_to_emoji_gpt, translate_emoji_to_text_gpt

# Load environment variables
load_dotenv()

def test_api():
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("\n" + "="*50)
    print("🤖 EMOJI TRANSLATOR API TEST")
    print("="*50)
    
    # Check API key
    if not api_key or api_key == "your_api_key_here":
        print("\n❌ ERROR: OpenAI API key not configured!")
        print("   1. Get API key from: https://platform.openai.com/api-keys")
        print("   2. Create .env file with: OPENAI_API_KEY=sk-xxx...")
        print("   3. Save and restart the app\n")
        return
    
    print("\n✅ API Key found!")
    print(f"   Key preview: {api_key[:10]}...{api_key[-5:]}\n")
    
    # Test 1: Text to Emoji
    print("-" * 50)
    print("Test 1: Text → Emoji Translation")
    print("-" * 50)
    test_texts = [
        "is your brother here",
        "I'm excited about the party",
        "I want to go home",
        "This is awesome"
    ]
    
    for text in test_texts:
        print(f"\n  Input: {text}")
        result = translate_text_to_emoji_gpt(text)
        print(f"  Output: {result['emoji']} ({result['description']})")
        print(f"  Confidence: {result['confidence']*100:.0f}%")
    
    # Test 2: Emoji to Text
    print("\n" + "-" * 50)
    print("Test 2: Emoji → Text Translation")
    print("-" * 50)
    test_emojis = ["👋", "🍕", "🚀", "💻", "❤️"]
    
    for emoji in test_emojis:
        print(f"\n  Input: {emoji}")
        result = translate_emoji_to_text_gpt(emoji)
        print(f"  Output: {result['text']}")
        print(f"  Confidence: {result['confidence']*100:.0f}%")
    
    print("\n" + "="*50)
    print("✅ ALL TESTS COMPLETED!")
    print("="*50 + "\n")

if __name__ == "__main__":
    test_api()
