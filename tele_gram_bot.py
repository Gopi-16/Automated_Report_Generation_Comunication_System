import json
import asyncio
from telegram import Bot
import os
import re
from dotenv import load_dotenv
load_dotenv()

# Fetch API key from .env securely
TOKEN = os.getenv("Tele_Token")
if not TOKEN:
    raise ValueError("API key not found. Make sure it's set in the .env file Token Error")

bot = Bot(token=TOKEN)


async def safe_send_message(chat_id, text, max_retries=5):
    """Try sending a message with retry + exponential backoff."""
    retry_delay = 2
    for attempt in range(1, max_retries + 1):
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            return True
        except Exception as e:
            print(f"⚠️ Send message attempt {attempt} failed: {e}")
            if attempt < max_retries:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
            else:
                return False


async def safe_send_audio(chat_id, audio_path, max_retries=5):
    """Try sending audio with retry + exponential backoff."""
    retry_delay = 2
    for attempt in range(1, max_retries + 1):
        try:
            with open(audio_path, 'rb') as audio_file:
                await bot.send_audio(chat_id=chat_id, audio=audio_file)
            return True
        except Exception as e:
            print(f"⚠️ Send audio attempt {attempt} failed: {e}")
            if attempt < max_retries:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
            else:
                return False


async def send_reports(reports_df, audio_folder):
    sent = []
    failed = []

    try:
        with open("parents.json", "r") as f:
            parents = json.load(f)

        for index, row in reports_df.iterrows():
            mobile = str(row["Parent_Mobile"])

            for number, chat_id in parents.items():
                if number[-10:] == mobile:

                    refining = re.sub(r"[*#-]", "", row["Generated_Report"])
                    refining = refining.replace("\\n", "\n")

                    print(f"📤 Sending report to: {mobile}")

                    # --- TRY SENDING MESSAGE ---
                    message_success = await safe_send_message(chat_id, refining)

                    # --- TRY SENDING AUDIO ---
                    audio_path = os.path.join(audio_folder, f"student_{index}.mp3")
                    audio_success = True

                    if os.path.exists(audio_path):
                        audio_success = await safe_send_audio(chat_id, audio_path)

                    if message_success and audio_success:
                        sent.append(mobile)
                        print(f"✅ Successfully sent to: {mobile}")
                    else:
                        failed.append(mobile)
                        print(f"❌ Failed after retries: {mobile}")

                    break

    except Exception as e:
        print("❌ Error loading parents.json:", e)

    return sent, failed

