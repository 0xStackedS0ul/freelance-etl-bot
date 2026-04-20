import os
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str) -> bool:
    """
    Sends a text message to a configured Telegram chat using the Bot API.

    Args:
        message (str): The text content of the message to send. Supports basic HTML/Markdown
                       depending on the parse_mode, but defaults to plain text here.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[ERROR] Missing Telegram credentials in .env file.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("[INFO] Telegram notification sent successfully.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to send Telegram message: {e}")
        return False


# --- Testing Level 2 ---
if __name__ == "__main__":
    print("Initiating Level 2: Notifier Test...\n")

    test_msg = "🚨 <b>Test Alert!</b>\n\nLevel 2 is online and ready for deployment."

    success = send_telegram_message(test_msg)

    if success:
        print("\nTest passed! Check your Telegram app.")
    else:
        print("\nTest failed. Please verify your .env file credentials.")