# 🚀 Quick Start Guide for Emoji Translator

## Step 1: Get OpenAI API Key (5 minutes)

1. Visit: https://platform.openai.com/api-keys
2. Sign up or log in with your OpenAI account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-`)
5. **Keep it secret** - don't share it

## Step 2: Install Dependencies

Open PowerShell and run:
```powershell
cd d:\coding\projects\emoji_transilator
pip install -r requirments.txt
```

## Step 3: Configure API Key

Create a `.env` file in the project root (same folder as app.py):

**Using PowerShell:**
```powershell
# Create the .env file
"OPENAI_API_KEY=sk-your-api-key-here" | Out-File -FilePath .env -Encoding UTF8
```

**Or edit manually:**
1. Open `.env.example`
2. Replace `your_api_key_here` with your actual key
3. Save as `.env` (remove `.example`)

Example `.env` file:
```
OPENAI_API_KEY=sk-proj-abc123XYZ789...
```

## Step 4: Run the App

```powershell
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

## Step 5: Open in Browser

Visit: http://localhost:5000

## Test It!

Try these inputs:

**Text → Emoji Mode:**
- "is your brother here" → Should give you a relevant emoji
- "i want to go to your home" → Should suggest 🏠 or related
- "I'm so excited!" → Should suggest 🎉

**Emoji → Text Mode:**
- 👋 → "Hello, greeting, wave"
- 🍕 → "Pizza, food"
- 🚀 → "Rocket, space, launch"

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```powershell
pip install openai
```

### "API key not configured"
- Check that `.env` file exists in project root
- Restart the Flask app after creating `.env`
- Verify key starts with `sk-`

### "Authentication error from OpenAI"
- Your API key may be invalid
- Check for typos
- Generate a new key from https://platform.openai.com/api-keys

### "Rate limit exceeded"
- You've made too many requests
- Wait a minute before continuing
- Upgrade your OpenAI plan for higher limits

## System Requirements

- Python 3.8 or higher
- Internet connection (for OpenAI API)
- Windows/Mac/Linux

## Important Notes

⚠️ **Keep your API key secret!**
- Don't share it online
- Don't commit `.env` to GitHub
- Generate a new key if compromised

💰 **Monitor your usage**
- GPT-3.5 Turbo is cheap (~$0.002 per 1K tokens)
- Each translation costs ~$0.00001-0.00002
- Set usage limits in OpenAI dashboard

## Next Steps

After setup, you can:
1. Customize the emoji dataset in `dataset/emoji_dataset.csv`
2. Adjust UI colors in `static/styles.css`
3. Modify prompts in `utils/emoji_api.py`
4. Deploy to Heroku, AWS, or Azure

## Support

If you get stuck:
1. Check error messages in the terminal
2. Review OpenAI docs: https://platform.openai.com/docs
3. Verify your API key is active

---

**Happy emoji translating!** 🎉
