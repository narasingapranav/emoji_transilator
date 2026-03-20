from utils.ml_emoji_model import train_and_save_model


if __name__ == "__main__":
    stats = train_and_save_model()
    print("ML model trained and saved")
    print(f"Rows used: {stats['rows']}")
    print(f"Emoji classes: {stats['classes']}")
    print(f"Model: {stats['model_path']}")
    print(f"Meta: {stats['meta_path']}")
