import os
import re
import pickle
from collections import Counter, defaultdict

import pandas as pd
import emoji as emoji_lib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


MODEL_PATH = os.path.join("models", "emoji_text_to_emoji.pkl")
META_PATH = os.path.join("models", "emoji_text_to_emoji_meta.pkl")

CURATED_SAMPLES = [
    ("hello", "👋"), ("hi", "👋"), ("good morning", "👋"), ("hey there", "👋"),
    ("brother", "👨"), ("my brother", "👨"), ("sister", "👩"), ("my sister", "👩"),
    ("love", "❤️"), ("i love you", "❤️"), ("heart", "❤️"),
    ("happy", "😊"), ("feeling happy", "😊"), ("smile", "😊"),
    ("sad", "😢"), ("feeling sad", "😢"), ("crying", "😢"),
    ("angry", "😡"), ("very angry", "😡"),
    ("pizza", "🍕"), ("i love pizza", "🍕"), ("food", "🍕"), ("hungry", "🍕"),
    ("coffee", "☕"), ("drink coffee", "☕"),
    ("dog", "🐶"), ("my dog", "🐶"),
    ("cat", "🐱"), ("my cat", "🐱"),
    ("school", "🏫"), ("go to school", "🏫"),
    ("car", "🚗"), ("drive car", "🚗"),
    ("sun", "☀️"), ("sunny day", "☀️"),
    ("moon", "🌙"), ("good night", "🌙"),
    ("star", "⭐"), ("stars in sky", "⭐"),
    ("movie", "🎬"), ("watching movie", "🎬"),
    ("home", "🏠"), ("go home", "🏠"),
    ("music", "🎵"), ("listening music", "🎵"),
    ("phone", "📱"), ("mobile phone", "📱"),
    ("coding", "💻"), ("computer", "💻"), ("laptop", "💻"),
    ("sleep", "😴"), ("going to sleep", "😴"),
]


def _normalize_text(text):
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s\u0080-\uFFFF]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _has_single_emoji(value):
    return len(emoji_lib.emoji_list(str(value))) == 1


def _first_emoji(value):
    items = emoji_lib.emoji_list(str(value))
    if not items:
        return "❓"
    return items[0]["emoji"]


def train_and_save_model(dataset_path="dataset/emoji_dataset.csv"):
    df = pd.read_csv(dataset_path)
    df = df[df["emoji"].apply(_has_single_emoji)].copy()

    df["emoji"] = df["emoji"].apply(_first_emoji)
    df["text"] = df["text"].astype(str).apply(_normalize_text)
    df = df[(df["text"] != "") & (df["emoji"] != "")]

    # De-duplicate exact training pairs.
    df = df.drop_duplicates(subset=["text", "emoji"]).reset_index(drop=True)

    # Focus dataset on practical emoji set and stabilize with curated samples.
    curated_df = pd.DataFrame(CURATED_SAMPLES, columns=["text", "emoji"])
    curated_df["text"] = curated_df["text"].astype(str).apply(_normalize_text)

    allowed = set(curated_df["emoji"].tolist())
    counts = df["emoji"].value_counts()
    keep_labels = set(counts[counts >= 4].index).intersection(allowed)
    df = df[df["emoji"].isin(keep_labels)].reset_index(drop=True)

    # Combine curated examples with filtered dataset.
    df = pd.concat([df, curated_df], ignore_index=True)

    X = df["text"].tolist()
    y = df["emoji"].tolist()

    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=1,
                    sublinear_tf=True,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=3000,
                    solver="lbfgs",
                    multi_class="auto",
                ),
            ),
        ]
    )

    pipeline.fit(X, y)

    # Build human-readable metadata for emoji meaning.
    text_by_emoji = defaultdict(list)
    for t, e in zip(X, y):
        text_by_emoji[e].append(t)

    emoji_to_text = {}
    for e, texts in text_by_emoji.items():
        common = Counter(texts).most_common(1)[0][0]
        emoji_to_text[e] = common

    os.makedirs("models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    with open(META_PATH, "wb") as f:
        pickle.dump({"emoji_to_text": emoji_to_text}, f)

    return {
        "rows": len(df),
        "classes": len(set(y)),
        "model_path": MODEL_PATH,
        "meta_path": META_PATH,
    }


def load_model_if_available():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(META_PATH):
        return None, None

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)

    return model, meta


def predict_text(model, meta, text, min_confidence=0.12):
    normalized = _normalize_text(text)
    if not normalized:
        return None

    try:
        probs = model.predict_proba([normalized])[0]
        classes = model.classes_
        best_idx = probs.argmax()
        pred_emoji = classes[best_idx]
        confidence = float(probs[best_idx])

        if confidence < min_confidence:
            return None

        description = meta.get("emoji_to_text", {}).get(pred_emoji, "ml predicted emoji")
        return {
            "input": text,
            "matched_text": description,
            "description": description,
            "emoji": pred_emoji,
            "confidence": round(confidence, 3),
            "method": "ML Model (Pickle)",
        }
    except Exception:
        return None
