
# AI Emoji Translator

A free **Emoji Translator** built with **Flask** and **local Hugging Face models**.

It supports:
- **Text to Emoji** translation
- **Emoji to Text** translation
- **Fast fallback keyword matching** when the model is slow or unavailable

---

## Features

- No OpenAI credits required
- Uses a local embedding model: `all-MiniLM-L6-v2`
- Optional Hugging Face token support via `.env`
- Responsive web UI
- Displays **confidence score** and **translation method**
- Exact emoji match path for faster emoji-to-text lookups
- Fallback keyword-based translation if the model fails to load

---

## Tech Stack

- Flask
- sentence-transformers
- scikit-learn
- pandas
- Hugging Face ecosystem (local model runtime)

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
````

### 2. (Optional) Environment Setup

Create a `.env` file in the project root:

```env
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

> **Note:**
>
> * The app works without this key in local mode
> * Never commit real tokens to GitHub

### 3. Run the App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## Usage Examples

### Text to Emoji

**Input:**

```text
sister
```

**Output:**

```text
👩
```

**Input:**

```text
is your brother here
```

**Output:**

```text
👨
```

### Emoji to Text

**Input:**

```text
👋
```

**Output:**

```text
hello, greeting, wave
```

---

## Project Structure

```text
emoji_transilator/
├── app.py
├── requirements.txt
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

---

## How It Works

1. User enters either plain text or an emoji
2. The app detects the input type
3. For text input:

   * It uses a local sentence embedding model to find the closest matching emoji
   * If the model is unavailable, it falls back to keyword matching
4. For emoji input:

   * It performs a direct lookup for exact emoji matches
5. The app returns:

   * The translated result
   * Confidence score
   * Translation method used

---

## Notes

* The **first launch may take longer** while the local model initializes
* If the model cannot load, the app automatically falls back to **keyword-based matching**
* Keep both `requirements.txt` and `requirments.txt` only if you intentionally support both filenames

---

## Troubleshooting

### App Not Starting

Make sure you are running the app from the project directory:

```bash
cd d:\coding\projects\emoji_transilator
python app.py
```

### Slow First Request

This is expected while local model resources are being loaded.

### Incorrect Emoji for a Phrase

You can improve results by:

* Updating the mapping logic in `utils/emoji_free.py`
* Adding or cleaning relevant rows in `dataset/emoji_dataset.csv`

---

## Security

* Do not commit `.env`
* Rotate any token that was ever exposed

---

## Future Improvements

* Add support for multi-emoji output
* Improve phrase-level semantic matching
* Add translation history
* Add dark mode UI
* Deploy online with Docker or Render
* Expand the emoji dataset for better accuracy

---

```

