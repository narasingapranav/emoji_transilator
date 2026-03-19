import os
from openai import OpenAI
from dotenv import load_dotenv
import emoji as emoji_lib

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_text_to_emoji_gpt(user_text):
    """
    Use OpenAI GPT to predict the most appropriate emoji for given text.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an emoji translator AI. Given text input, respond with ONLY a single emoji that best represents the meaning. Do not include any other text, just the emoji character."
                },
                {
                    "role": "user",
                    "content": f"Translate this to the most appropriate emoji: {user_text}"
                }
            ],
            temperature=0.7,
            max_tokens=5
        )
        
        emoji_result = response.choices[0].message.content.strip()
        
        # Get emoji description
        emoji_name = emoji_lib.emoji_list(emoji_result)
        emoji_description = emoji_name[0]['emoji_name'] if emoji_name else "Unknown"
        
        # Clean up description
        description = emoji_description.replace("_", " ").title() if emoji_description else "Unknown emoji"
        
        return {
            "input": user_text,
            "emoji": emoji_result,
            "description": description,
            "confidence": 0.95
        }
    except Exception as e:
        return {
            "input": user_text,
            "emoji": "❓",
            "description": f"Error: {str(e)}",
            "confidence": 0
        }


def translate_emoji_to_text_gpt(user_emoji):
    """
    Use OpenAI GPT to get meaning of emoji and translate to text description.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an emoji interpreter. Given an emoji, describe what it means in 2-4 words. Be concise."
                },
                {
                    "role": "user",
                    "content": f"What does this emoji mean? {user_emoji}"
                }
            ],
            temperature=0.5,
            max_tokens=10
        )
        
        text_result = response.choices[0].message.content.strip()
        
        return {
            "input": user_emoji,
            "emoji": user_emoji,
            "text": text_result,
            "confidence": 0.95
        }
    except Exception as e:
        return {
            "input": user_emoji,
            "emoji": user_emoji,
            "text": f"Error: {str(e)}",
            "confidence": 0
        }
