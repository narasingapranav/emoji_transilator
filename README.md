# AI Emoji Translator (ML + Pickle)

A Flask-based emoji translator that supports both:

1. Text to emoji prediction
2. Emoji to text interpretation

This branch includes a trainable ML model and saved pickle artifacts for text-to-emoji inference.

## Features

1. ML prediction path using a saved `.pkl` model
2. Emoji-to-text exact and multi-emoji parsing
3. Long story breakdown mode for narrative input
4. Edge-case handling (empty input, symbol-only input, unknown words)
5. Fallback methods when model confidence is low
6. Local-first setup (no OpenAI credits required)

## Tech Stack

1. Flask
2. scikit-learn (TF-IDF + Logistic Regression)
3. sentence-transformers (semantic fallback path)
4. pandas, numpy

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train ML model and create pickle files

```bash
python train_emoji_model.py
```

This creates:

1. `models/emoji_text_to_emoji.pkl`
2. `models/emoji_text_to_emoji_meta.pkl`

### 3. Run the app

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Project Structure

```text
emoji_transilator/
├── app.py
├── train_emoji_model.py
├── run_edge_case_tests.py
├── requirements.txt
├── models/
│   ├── emoji_text_to_emoji.pkl
│   └── emoji_text_to_emoji_meta.pkl
├── dataset/
│   └── emoji_dataset.csv
├── templates/
│   └── index.html
├── static/
│   └── styles.css
└── utils/
    ├── emoji_free.py
    ├── ml_emoji_model.py
    ├── emoji_to_text.py
    ├── text_to_emoji.py
    └── preprocess.py
```

## How Prediction Works

Text to emoji pipeline order:

1. Validation checks (empty/symbol-only)
2. Long narrative breakdown mode
3. Tech keyword mapping (quantum/blockchain/etc.)
4. Relation quick match (brother/sister for short queries)
5. ML model prediction from pickle (`ML Model (Pickle)`)
6. Semantic fallback / unknown fallback

Emoji to text pipeline:

1. Validation checks
2. Multi-emoji parse (`👋❤️` style inputs)
3. Exact emoji lookup
4. Fallback interpretation

## Example Inputs

1. `hello` -> `👋`
2. `i love pizza` -> `🍕`
3. `my brother is at home` -> `👨`
4. `👋` -> `hello, greeting, wave`
5. `👋❤️` -> parsed combined meaning

## Edge-Case Coverage

Handled cases include:

1. Extra spaces and mixed case
2. Punctuation-heavy input (`hello!!!`)
3. Unknown tokens (`asdfghjkl` -> `❓`)
4. Numbers/symbol-only text
5. Non-English and mixed text+emoji inputs
6. Very long paragraph stress tests

Run all edge-case tests:

```bash
python run_edge_case_tests.py
```

## Notes

1. First app startup can be slower due to local model loading.
2. Keep `.env` and API tokens out of git.
3. If needed, retrain anytime with `python train_emoji_model.py`.

## Security

1. Never commit real API keys/tokens.
2. Rotate any token that was previously exposed.

## License

MIT

