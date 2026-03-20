import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
import re
import emoji as emoji_lib
from utils.ml_emoji_model import load_model_if_available, predict_text

# Load environment variables
load_dotenv()

# Load the local dataset
df = pd.read_csv("dataset/emoji_dataset.csv")


def _has_single_emoji(value):
    emojis = emoji_lib.emoji_list(str(value))
    return len(emojis) == 1


# Ignore noisy rows containing multiple chained emojis (e.g., 📞👨‍👩‍👧‍👦)
clean_df = df[df["emoji"].apply(_has_single_emoji)].reset_index(drop=True)

# Load ML pickle model if available.
ml_model, ml_meta = load_model_if_available()

# Check if Hugging Face API key is available
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Use lightweight model for FAST loading
print("📦 Loading embedding model (lightweight, fast)...")
model = None
try:
    # Avoid blocking startup on slow/no internet. Use cached model only.
    model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
    print("✅ Model loaded successfully!")
except BaseException as e:
    print(f"⚠️ Error loading model: {e}")
    model = None

# Create embeddings for dataset text descriptions (cached for speed)
print("🔄 Creating embeddings...")
try:
    if model is not None:
        dataset_embeddings = model.encode(clean_df["text"].tolist())
        print("✅ Embeddings ready!\n")
    else:
        dataset_embeddings = None
except BaseException:
    dataset_embeddings = None


RELATION_KEYWORDS = {
    r"\bsister\b|\bhermana\b": "👩",
    r"\bbrother\b|\bhermano\b": "👨",
    r"\bmother\b|\bmom\b|\bmummy\b": "👩",
    r"\bfather\b|\bdad\b|\bdaddy\b": "👨",
    r"\bfamily\b|\bparents\b|\bsiblings\b": "👨‍👩‍👧‍👦",
    r"\bhere\b.*\?|\bis\b.*\bhere\b|\bare\b.*\bhere\b": "❓",
}


TECH_KEYWORDS = {
    r"\bquantum\b": ("⚛️", "quantum computing / advanced science"),
    r"\bblockchain\b|\bcrypto\b|\bbitcoin\b": ("⛓️", "blockchain / distributed ledger"),
    r"\bmetaverse\b|\bvirtual reality\b|\bvr\b": ("🥽", "metaverse / virtual world"),
    r"\bhyperloop\b": ("🚄", "hyperloop / high-speed transport"),
    r"\bneuralink\b|\bbrain[-\s]?computer\b": ("🧠", "brain-computer interface"),
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


def _normalize_text_input(text):
    # Normalize whitespace and keep original language characters.
    return re.sub(r"\s+", " ", str(text).strip())


def _is_symbol_only(text):
    # Treat punctuation-only/symbol-only input as unknown.
    return re.search(r"[A-Za-z0-9\u0080-\uFFFF]", text) is None and len(emoji_lib.emoji_list(text)) == 0


def _keyword_first_match(text):
    lowered = re.sub(r"[^\w\s]", " ", text.lower())
    for pattern, mapped_emoji in RELATION_KEYWORDS.items():
        if re.search(pattern, lowered):
            return mapped_emoji
    return None


def _tech_match(text):
    lowered = re.sub(r"[^\w\s]", " ", text.lower())
    for pattern, (mapped_emoji, mapped_desc) in TECH_KEYWORDS.items():
        if re.search(pattern, lowered):
            return mapped_emoji, mapped_desc
    return None


def _is_short_query(text):
    words = re.findall(r"\w+", _normalize_text_input(text))
    return len(words) <= 8


def _generate_story_breakdown(user_text):
    """Create grouped emoji lines for long narrative inputs."""
    lowered = _normalize_text_input(user_text).lower()
    words = re.findall(r"\w+", lowered)
    if len(words) < 40:
        return None

    groups = [
        {
            "name": "morning routine",
            "rules": [
                (r"hello|hi|hey", "👋"),
                (r"today|morning|sunrise", "🌅"),
                (r"wake|woke|early|alarm", "⏰"),
                (r"coffee", "☕"),
                (r"walk|walking|stroll", "🚶"),
                (r"park|tree|trees|garden", "🌳"),
                (r"music|song|songs|listening", "🎵"),
                (r"phone|mobile", "📱"),
            ],
        },
        {
            "name": "family and plans",
            "rules": [
                (r"brother", "👨‍👦‍👦"),
                (r"sister", "👩‍👧"),
                (r"home|house", "🏠"),
                (r"talk|talked|chat|discuss", "🗣️"),
                (r"school|class", "🏫"),
                (r"work|office", "💼"),
                (r"weekend|plan|plans", "📅"),
            ],
        },
        {
            "name": "food and friends",
            "rules": [
                (r"pizza", "🍕"),
                (r"hungry|eat|ate|food", "😋"),
                (r"movie|film|watching", "🎬"),
                (r"friends", "👬"),
            ],
        },
        {
            "name": "study and tech",
            "rules": [
                (r"evening", "🌆"),
                (r"coding|code|laptop|computer", "💻"),
                (r"coding|code|laptop|computer|typing|keyboard", "⌨️"),
                (r"message|messages|text|chat", "💬"),
                (r"classmate|classmates|student|students", "👨‍🎓"),
                (r"ai|artificial intelligence", "🤖"),
                (r"machine learning|ml", "🧠"),
                (r"read|reading|book|books", "📚"),
            ],
        },
        {
            "name": "night wrap-up",
            "rules": [
                (r"night", "🌙"),
                (r"star|stars|sky", "⭐"),
                (r"happy", "😊"),
                (r"relaxed|calm|peaceful", "😌"),
                (r"sleep|slept", "😴"),
                (r"tomorrow|better|hope", "✨"),
            ],
        },
    ]

    lines = []
    matched_groups = 0
    for group in groups:
        line = []
        for pattern, emoji_symbol in group["rules"]:
            if re.search(pattern, lowered):
                line.append(emoji_symbol)
        if line:
            matched_groups += 1
            lines.append("".join(line))

    # Only use story mode when we have broad context coverage.
    if matched_groups >= 3:
        return {
            "input": user_text,
            "matched_text": "long narrative emoji breakdown",
            "description": "long narrative emoji breakdown",
            "emoji": "\n\n".join(lines),
            "confidence": 0.9,
            "method": "Story Breakdown"
        }
    return None


def translate_text_to_emoji_free(user_text):
    """
    Fast emoji translation using lightweight local models.
    ✅ No OpenAI credits needed!
    """
    try:
        normalized_text = _normalize_text_input(user_text)
        if not normalized_text:
            return {
                "input": user_text,
                "matched_text": "empty input",
                "description": "empty input",
                "emoji": "❓",
                "confidence": 0.0,
                "method": "Validation"
            }

        if _is_symbol_only(normalized_text):
            return {
                "input": user_text,
                "matched_text": "symbols only",
                "description": "symbols only",
                "emoji": "❓",
                "confidence": 0.1,
                "method": "Validation"
            }

        story_result = _generate_story_breakdown(normalized_text)
        if story_result:
            return story_result

        tech_result = _tech_match(normalized_text)
        if tech_result is not None:
            mapped_emoji, mapped_desc = tech_result
            return {
                "input": normalized_text,
                "matched_text": mapped_desc,
                "description": mapped_desc,
                "emoji": mapped_emoji,
                "confidence": 0.93,
                "method": "Tech Mapping"
            }

        keyword_emoji = _keyword_first_match(normalized_text) if _is_short_query(normalized_text) else None
        if keyword_emoji:
            return {
                "input": normalized_text,
                "matched_text": "keyword relation/question mapping",
                "description": "keyword relation/question mapping",
                "emoji": keyword_emoji,
                "confidence": 0.92,
                "method": "Quick Match"
            }

        ml_prediction = predict_text(ml_model, ml_meta, normalized_text) if ml_model is not None else None
        if ml_prediction is not None:
            return ml_prediction

        if model is None or dataset_embeddings is None:
            return fallback_text_to_emoji(normalized_text)
            
        # Preprocess input
        processed_input = normalized_text.lower()
        
        # Create embedding for user input
        input_embedding = model.encode([processed_input])
        
        # Find similarities with dataset
        similarities = cosine_similarity(input_embedding, dataset_embeddings)[0]
        best_match_index = np.argmax(similarities)
        
        matched_text = clean_df.iloc[best_match_index]["text"]
        matched_emoji = _normalize_emoji(clean_df.iloc[best_match_index]["emoji"])
        confidence = float(similarities[best_match_index])

        # If semantic match is weak, return a clear unknown marker instead of noisy guesses.
        if confidence < 0.42:
            return {
                "input": user_text,
                "matched_text": "no strong semantic match",
                "description": "no strong semantic match",
                "emoji": "❓",
                "confidence": round(max(confidence, 0.0), 3),
                "method": "Unknown Fallback"
            }
        
        return {
            "input": normalized_text,
            "matched_text": matched_text,
            "description": matched_text,
            "emoji": matched_emoji,
            "confidence": min(round(max(confidence, 0.0), 3), 1.0),
            "method": "Free AI"
        }
    except Exception as e:
        return fallback_text_to_emoji(user_text)


def fallback_text_to_emoji(user_text):
    """Fallback when AI models unavailable - uses keyword matching"""
    normalized = _normalize_text_input(user_text)
    text_lower = re.sub(r"[^\w\s]", " ", normalized.lower())
    
    # Simple keyword matching
    keywords = [
        (r"happy|joyful|cheerful|smile|good|great|relaxed", "😊"),
        (r"sad|unhappy|cry|down|bad", "😢"),
        (r"angry|mad|furious|upset", "😡"),
        (r"love|affection|heart|like|adore", "❤️"),
        (r"cool|awesome|excellent", "😎"),
        (r"laugh|funny|hilarious|lol", "😂"),
        (r"shock|surprised|wow|omg", "😲"),
        (r"excited|thrilled|pumped|yay|woohoo", "🎉"),
        (r"sleep|night|tired|rest", "😴"),
        (r"home|house|living", "🏠"),
        (r"pizza|food|eat|hungry", "🍕"),
        (r"coffee|beverage|morning", "☕"),
        (r"movie|film|watching", "🎬"),
        (r"code|coding|laptop|computer", "💻"),
        (r"phone|message|messages|text", "📱"),
        (r"music|song|listening", "🎵"),
        (r"sun|sunny|sunshine", "☀️"),
        (r"moon|night", "🌙"),
        (r"star|stars|sky", "⭐"),
        (r"hello|hi|greet|wave|hey|goodbye", "👋"),
    ]

    best = None
    best_count = 0
    best_pattern = ""
    for pattern, emoji in keywords:
        count = len(re.findall(pattern, text_lower))
        if count > best_count:
            best_count = count
            best = emoji
            best_pattern = pattern

    if best is not None and best_count > 0:
        confidence = 0.65 if best_count == 1 else min(0.9, 0.65 + 0.07 * (best_count - 1))
        return {
            "input": user_text,
            "matched_text": best_pattern.replace("|", " / "),
            "description": best_pattern.replace("|", " / "),
            "emoji": best,
            "confidence": round(confidence, 3),
            "method": "Quick Match"
        }
    
    # Default if no match
    return {
        "input": user_text,
        "matched_text": "no clear keyword match",
        "description": "no clear keyword match",
        "emoji": "❓",
        "confidence": 0.2,
        "method": "Fallback"
    }


def translate_emoji_to_text_free(user_emoji):
    """
    Fast emoji interpretation using lightweight models.
    ✅ No OpenAI credits needed!
    """
    try:
        normalized_emoji_input = _normalize_text_input(user_emoji)
        if not normalized_emoji_input:
            return {
                "input": user_emoji,
                "emoji": "❓",
                "text": "empty input",
                "confidence": 0.0,
                "method": "Validation"
            }

        emoji_items = [e["emoji"] for e in emoji_lib.emoji_list(normalized_emoji_input)]
        if len(emoji_items) > 1:
            parts = []
            for emo in emoji_items:
                exact = clean_df[clean_df["emoji"] == emo]
                if not exact.empty:
                    parts.append(exact.iloc[0]["text"])
                else:
                    parts.append(fallback_emoji_to_text(emo)["text"])
            return {
                "input": normalized_emoji_input,
                "emoji": normalized_emoji_input,
                "text": " | ".join(parts),
                "confidence": 0.9,
                "method": "Multi Emoji Parse"
            }

        # Try exact match first (fastest)
        exact_match = clean_df[clean_df["emoji"] == normalized_emoji_input]
        
        if not exact_match.empty:
            matched_text = exact_match.iloc[0]["text"]
            return {
                "input": user_emoji,
                "emoji": normalized_emoji_input,
                "text": matched_text,
                "confidence": 1.0,
                "method": "Exact Match"
            }
        
        # If no exact match and model available
        if model is None or dataset_embeddings is None:
            return fallback_emoji_to_text(normalized_emoji_input)
        
        # Create embedding for emoji
        emoji_embedding = model.encode([normalized_emoji_input])
        
        # Find similarities with dataset
        similarities = cosine_similarity(emoji_embedding, dataset_embeddings)[0]
        best_match_index = np.argmax(similarities)
        
        matched_text = df.iloc[best_match_index]["text"]
        confidence = float(similarities[best_match_index])
        
        return {
            "input": user_emoji,
            "emoji": normalized_emoji_input,
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


