import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("dataset/emoji_dataset.csv")

# Load AI model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings based on TEXT descriptions (not emoji characters)
# This is more reliable than trying to embed emoji characters
text_embeddings = model.encode(df["text"].tolist())

def translate_emoji_to_text(user_emoji):
    # Try direct emoji match first (exact match takes precedence)
    exact_match = df[df["emoji"] == user_emoji]
    
    if not exact_match.empty:
        matched_text = exact_match.iloc[0]["text"]
        matched_emoji = exact_match.iloc[0]["emoji"]
        return {
            "input": user_emoji,
            "matched_emoji": matched_emoji,
            "text": matched_text,
            "confidence": 1.0
        }
    
    # If no exact match, create embedding from the emoji's semantic description
    # We'll use the text column embeddings as reference
    user_input_embedding = model.encode([user_emoji])
    
    similarities = cosine_similarity(user_input_embedding, text_embeddings)[0]
    best_match_index = np.argmax(similarities)

    matched_emoji = df.iloc[best_match_index]["emoji"]
    matched_text = df.iloc[best_match_index]["text"]
    confidence = float(similarities[best_match_index])

    return {
        "input": user_emoji,
        "matched_emoji": matched_emoji,
        "text": matched_text,
        "confidence": round(confidence, 3)
    }