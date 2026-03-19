import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import preprocess_text

# Load dataset
df = pd.read_csv("dataset/emoji_dataset.csv")

# Preprocess dataset text
df["processed_text"] = df["text"].apply(preprocess_text)

# Load AI model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings for dataset
dataset_embeddings = model.encode(df["processed_text"].tolist())

def translate_text_to_emoji(user_text):
    processed_input = preprocess_text(user_text)
    input_embedding = model.encode([processed_input])

    similarities = cosine_similarity(input_embedding, dataset_embeddings)[0]
    best_match_index = np.argmax(similarities)

    matched_text = df.iloc[best_match_index]["text"]
    matched_emoji = df.iloc[best_match_index]["emoji"]
    confidence = float(similarities[best_match_index])

    return {
        "input": user_text,
        "matched_text": matched_text,
        "emoji": matched_emoji,
        "confidence": round(confidence, 3)
    }