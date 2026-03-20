from utils.emoji_free import translate_text_to_emoji_free, translate_emoji_to_text_free

TEXT_CASES = [
    # 1. Simple Normal Inputs
    "hello", "brother", "sister", "love", "happy", "sad", "angry", "food", "dog", "cat", "school", "car", "sun", "moon", "star",

    # 2. Full Sentences
    "hello how are you",
    "my brother is at home",
    "i love pizza very much",
    "the sun is shining today",
    "my sister is studying at school",
    "i am feeling happy today",
    "the dog is running in the park",
    "we watched a movie at night",

    # 3. Long Paragraph Input
    "Today I woke up early, drank coffee, met my brother and sister, and went to college. After classes, I felt hungry and ate pizza with my friends. In the evening, I watched the sunset, listened to music, and then came home feeling happy and relaxed.",

    # 4. Mixed Case Inputs
    "HELLO", "Hello", "hElLo", "BROTHER", "SiStEr", "I LoVe PiZzA",

    # 5. Extra Spaces / Whitespace
    "   hello", "brother   ", "   sister   ", "   i love pizza   ",

    # 6. Punctuation Handling
    "hello!", "brother?", "sister...", "i love pizza!!!", "are you happy?", "wow, amazing!",

    # 7. Numbers + Text
    "i have 2 brothers", "my sister is 18 years old", "i ate 3 pizzas today", "school starts at 9", "movie at 7 pm",

    # 8. Special Characters
    "hello @home", "brother #1", "sister :)", "love <3", "happy :)", "sad :(",

    # 9. Unknown Words
    "quantum", "blockchain", "metaverse", "hyperloop", "neuralink", "asdfghjkl", "qwertyuiop", "blorptastic",

    # 10. Mixed Known + Unknown Words
    "hello quantum brother", "i love pizza and blockchain", "my sister likes hyperloop cars", "happy blorptastic day",

    # 11. Repeated Words
    "hello hello hello", "love love love", "pizza pizza pizza", "happy happy happy", "brother brother brother",

    # 14. Mixed Text + Emoji
    "hello 👋", "i love pizza 🍕", "my dog 🐶 is cute", "happy 😊 today", "good night 🌙",

    # 16. Empty / Almost Empty Inputs
    "", " ", "   ", ".", ",", "!", "?",

    # 17. Only Numbers
    "123", "99999", "2026", "007", "0",

    # 18. Only Symbols
    "!!!", "???", "@@@", "###", "$$$", "%%%", "&&&", "***",

    # 19. Non-English Inputs
    "నమస్తే", "హలో", "こんにちは", "hola", "bonjour", "مرحبا",

    # 20. Slang / Informal Chat
    "bro", "sis", "luv u", "gm", "gn", "lol", "omg", "brb", "ttyl",

    # 21. Very Long Repetitive Input
    "hello hello hello hello hello hello hello hello hello hello brother sister love pizza happy sad dog cat school movie car house phone sun moon star",

    # 22. Very Large Paragraph
    "This morning I woke up feeling a little tired but excited for the day ahead. I said hello to my family, had breakfast with my brother and sister, and then got ready for college. During the day, I attended classes, talked to my friends, used my phone, and worked on my laptop for a coding project. After returning home, I felt hungry and ate pizza while watching a funny movie. Later in the evening, I played with my dog, looked at the moon and stars in the sky, and spent some time listening to music before going to sleep feeling happy, peaceful, and thankful.",
]

EMOJI_CASES = [
    # 12. Emoji to Text - Single Emoji
    "👋", "❤️", "😂", "😢", "🍕", "🐶", "🐱", "☀️", "🌙", "⭐", "🚗", "🏠",

    # 13. Emoji to Text - Multiple Emojis
    "👋❤️", "🍕😂", "🐶🐱", "☀️🌙⭐", "🏠🚗📱",

    # 15. Unsupported / Rare Emojis
    "🫠", "🫨", "🪩", "🛜", "🫡", "🩷", "🫎",
]


def run_text_tests():
    print("\n=== TEXT -> EMOJI TESTS ===")
    for case in TEXT_CASES:
        result = translate_text_to_emoji_free(case)
        emoji_out = result.get("emoji", "")
        method = result.get("method", "")
        desc = result.get("description", "")
        print(f"Input: {repr(case)}")
        print(f"Output: {emoji_out} | Method: {method} | Meaning: {desc}")
        print("-" * 80)


def run_emoji_tests():
    print("\n=== EMOJI -> TEXT TESTS ===")
    for case in EMOJI_CASES:
        result = translate_emoji_to_text_free(case)
        text_out = result.get("text", "")
        method = result.get("method", "")
        print(f"Input: {case}")
        print(f"Output: {text_out} | Method: {method}")
        print("-" * 80)


if __name__ == "__main__":
    run_text_tests()
    run_emoji_tests()
