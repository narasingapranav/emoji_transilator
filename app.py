from flask import Flask, render_template, request
from utils.emoji_free import translate_text_to_emoji_free, translate_emoji_to_text_free

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    mode = "text_to_emoji"
    error = None
    using_free_ai = True

    if request.method == "POST":
        mode = request.form.get("mode", "text_to_emoji")
        user_input = request.form.get("user_input", "").strip()

        if not user_input:
            error = "Please enter some text or emojis to translate"
        else:
            try:
                if mode == "text_to_emoji":
                    result = translate_text_to_emoji_free(user_input)
                else:
                    result = translate_emoji_to_text_free(user_input)
            except Exception as e:
                error = f"Error during translation: {str(e)}"

    return render_template("index.html", result=result, mode=mode, error=error, using_free_ai=using_free_ai)

if __name__ == "__main__":
    print("\n✅ Emoji Translator - FREE VERSION (No Credits Needed!)")
    print("🚀 Running on http://127.0.0.1:5000")
    print("💡 Uses local AI models - No API costs!\n")
    app.run(debug=True, host="127.0.0.1", port=5000)