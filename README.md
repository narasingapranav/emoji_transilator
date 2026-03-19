# AI Emoji Translator

Free emoji translator built with Flask and local Hugging Face models.

It supports:
1. Text to emoji translation
2. Emoji to text translation
3. Fast fallback keyword matching when model loading is slow or unavailable

## Features

1. No OpenAI credits required
2. Uses local embedding model (`all-MiniLM-L6-v2`)
3. Optional Hugging Face token support via `.env`
4. Responsive web UI with confidence score and translation method
5. Exact emoji match path for fast emoji-to-text lookups

## Tech Stack

1. Flask
2. sentence-transformers
3. scikit-learn
4. pandas
5. Hugging Face ecosystem (local model runtime)

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Optional environment setup

Create a `.env` file in the project root:

```bash
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

Note:
1. The app works without this key in local mode.
2. Never commit real tokens.

### 3. Run the app

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Usage Examples

### Text to Emoji

1. Input: `sister`
2. Output: `👩`

1. Input: `is your brother here`
2. Output: `👨`

### Emoji to Text

1. Input: `👋`
2. Output: `hello, greeting, wave`

## Project Structure

```text
emoji_transilator/
├── app.py
├── requirements.txt
├── requirments.txt
├── dataset/
│   └── emoji_dataset.csv
├── static/
│   └── styles.css
├── templates/
│   └── index.html
└── utils/
	├── emoji_free.py
	├── emoji_api.py
	├── text_to_emoji.py
	├── emoji_to_text.py
	└── preprocess.py
```

## Notes

1. First launch can take longer while the model initializes.
2. If the model cannot load, the app falls back to keyword-based quick matching.
3. Keep both `requirements.txt` and `requirments.txt` only if you intentionally support both names.

## Troubleshooting

### App not starting

Run from the project directory:

```bash
cd d:\coding\projects\emoji_transilator
python app.py
```

### Slow first request

This is expected while local model resources are loaded.

### Wrong emoji for a phrase

Update mapping logic in `utils/emoji_free.py` and add/clean relevant rows in `dataset/emoji_dataset.csv`.

## Security

1. Do not commit `.env`.
2. Rotate any token that was ever exposed.

## License

MIT
