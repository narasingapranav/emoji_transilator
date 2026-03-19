import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
import re
import emoji as emoji_lib

# Load environment variables
load_dotenv()

# Load the local dataset
df = pd.read_csv("dataset/emoji_dataset.csv")

# Check if Hugging Face API key is available
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Use lightweight model for FAST loading
print("📦 Loading embedding model (lightweight, fast)...")
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    model = None

# Create embeddings for dataset text descriptions (cached for speed)
print("🔄 Creating embeddings...")
try:
    dataset_embeddings = model.encode(df["text"].tolist())
    print("✅ Embeddings ready!\n")
except:
    dataset_embeddings = None


RELATION_KEYWORDS = {
    r"\bsister\b|\bhermana\b": "👩",
    r"\bbrother\b|\bhermano\b": "👨",
    r"\bmother\b|\bmom\b|\bmummy\b": "👩",
    r"\bfather\b|\bdad\b|\bdaddy\b": "👨",
    r"\bfamily\b|\bparents\b|\bsiblings\b": "👨‍👩‍👧‍👦",
    r"\bhere\b.*\?|\bis\b.*\bhere\b|\bare\b.*\bhere\b": "❓",
}


def _normalize_emoji(value):
    """Return a single best emoji character from any noisy value."""
    if value is None:
        return "❓"
    emoji_list = emoji_lib.emoji_list(str(value))
    if emoji_list:
        # Keep the first detected emoji to avoid multi-emoji chains like 📞👨‍👩‍👧‍👦
        return emoji_list[0]["emoji"]
    return "❓"


def _keyword_first_match(text):
    lowered = text.lower()
    for pattern, mapped_emoji in RELATION_KEYWORDS.items():
        if re.search(pattern, lowered):
            return mapped_emoji
    return None


def translate_text_to_emoji_free(user_text):
    """
    Fast emoji translation using lightweight local models.
    ✅ No OpenAI credits needed!
    """
    try:
        keyword_emoji = _keyword_first_match(user_text)
        if keyword_emoji:
            return {
                "input": user_text,
                "matched_text": "keyword relation/question mapping",
                "description": "keyword relation/question mapping",
                "emoji": keyword_emoji,
                "confidence": 0.92,
                "method": "Quick Match"
            }

        if model is None or dataset_embeddings is None:
            return fallback_text_to_emoji(user_text)
            
        # Preprocess input
        processed_input = user_text.lower().strip()
        
        # Create embedding for user input
        input_embedding = model.encode([processed_input])
        
        # Find similarities with dataset
        similarities = cosine_similarity(input_embedding, dataset_embeddings)[0]
        best_match_index = np.argmax(similarities)
        
        matched_text = df.iloc[best_match_index]["text"]
        matched_emoji = _normalize_emoji(df.iloc[best_match_index]["emoji"])
        confidence = float(similarities[best_match_index])
        
        return {
            "input": user_text,
            "matched_text": matched_text,
            "description": matched_text,
            "emoji": matched_emoji,
            "confidence": min(round(max(confidence, 0.5), 3), 1.0),
            "method": "Free AI"
        }
    except Exception as e:
        return fallback_text_to_emoji(user_text)


def fallback_text_to_emoji(user_text):
    """Fallback when AI models unavailable - uses keyword matching"""
    text_lower = user_text.lower()
    
    # Simple keyword matching
    keywords = {
        "hello|hi|greet|wave|hey|goodbye": "👋",
        "happy|joyful|cheerful|smile|good|great": "😊",
        "sad|unhappy|cry|down|bad": "😢",
        "angry|mad|furious|upset": "😡",
        "love|affection|heart|like|adore": "❤️",
        "cool|awesome|excellent|great": "😎",
        "laugh|funny|hilarious|lol": "😂",
        "shock|surprised|surprised|wow|omg": "😲",
        "excited|thrilled|pumped|yay|woohoo": "🎉",
        "home|house|living": "🏠",
        "pizza|food|eat|hungry": "🍕",
        "coffee|drink|beverage|morning": "☕",
        "party|celebration|fun|enjoy": "🎊",
        "dog|puppy|pet|canine": "🐶",
        "cat|kitten|feline": "🐱",
        "rocket|space|launch|explore": "🚀",
    }
    
    for pattern, emoji in keywords.items():
        if re.search(pattern, text_lower):
            return {
                "input": user_text,
                "matched_text": pattern.replace("|", " / "),
                "description": pattern.replace("|", " / "),
                "emoji": emoji,
                "confidence": 0.6,
                "method": "Quick Match"
            }
    
    # Default if no match
    return {
        "input": user_text,
        "matched_text": "Generic",
        "description": "Generic",
        "emoji": "😊",
        "confidence": 0.3,
        "method": "Fallback"
    }


def translate_emoji_to_text_free(user_emoji):
    """
    Fast emoji interpretation using lightweight models.
    ✅ No OpenAI credits needed!
    """
    try:
        # Try exact match first (fastest)
        exact_match = df[df["emoji"] == user_emoji]
        
        if not exact_match.empty:
            matched_text = exact_match.iloc[0]["text"]
            return {
                "input": user_emoji,
                "emoji": user_emoji,
                "text": matched_text,
                "confidence": 1.0,
                "method": "Exact Match"
            }
        
        # If no exact match and model available
        if model is None or dataset_embeddings is None:
            return fallback_emoji_to_text(user_emoji)
        
        # Create embedding for emoji
        emoji_embedding = model.encode([user_emoji])
        
        # Find similarities with dataset
        similarities = cosine_similarity(emoji_embedding, dataset_embeddings)[0]
        best_match_index = np.argmax(similarities)
        
        matched_text = df.iloc[best_match_index]["text"]
        confidence = float(similarities[best_match_index])
        
        return {
            "input": user_emoji,
            "emoji": user_emoji,
            "text": matched_text,
            "confidence": min(round(max(confidence, 0.5), 3), 1.0),
            "method": "Free AI"
        }
    except Exception as e:
        return fallback_emoji_to_text(user_emoji)


def fallback_emoji_to_text(user_emoji):
    """Fallback when AI models unavailable"""
    emoji_meanings = {
        "👋": "Hello, greeting, wave",
        "😊": "Happy, cheerful, smile",
        "😢": "Sad, unhappy, crying",
        "😡": "Angry, mad, furious",
        "❤️": "Love, affection, heart",
        "😎": "Cool, awesome, confident",
        "😂": "Laughing, funny, hilarious",
        "😲": "Shocked, surprised, wow",
        "🎉": "Party, celebration, excited",
        "🏠": "Home, house, building",
        "🍕": "Pizza, food, delicious",
        "☕": "Coffee, drink, morning",
        "🎊": "Celebration, party, festive",
        "🐶": "Dog, pet, puppy, animal",
        "🐱": "Cat, kitten, feline",
        "🚀": "Rocket, space, launch",
        "🌹": "Rose, flower, beautiful",
        "⭐": "Star, excellent, bright",
        "🔥": "Fire, hot, awesome",
        "💕": "Love, hearts, affection",
    }
    
    text = emoji_meanings.get(user_emoji, "Unknown emoji")
    
    return {
        "input": user_emoji,
        "emoji": user_emoji,
        "text": text,
        "confidence": 0.8,
        "method": "Quick Match"
    }


