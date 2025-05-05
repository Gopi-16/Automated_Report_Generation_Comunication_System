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
#TOKEN = "7226566019:AAFbejFkrE5U4_TbtJ_qrMLGOhXBEqg7NT0"  # replace with your bot token
bot = Bot(token=TOKEN)

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
                    try:
                        refining = re.sub(r"[*#-]", "", row["Generated_Report"])
                        refining=refining.replace("\\n","\n")
                        await bot.send_message(chat_id=chat_id, text=refining)
                        #print(row["Generated_Report"])
                        audio_path = os.path.join(audio_folder, f"student_{index}.mp3")
                        if os.path.exists(audio_path):
                            with open(audio_path, 'rb') as audio_file:
                                await bot.send_audio(chat_id=chat_id, audio=audio_file)
                        sent.append(mobile)
                    except Exception as e:
                        print(f"❌ Failed to send to {mobile}: {e}")
                        failed.append(mobile)
                    break
    except Exception as e:
        print("❌ Error loading parents.json:", e)

    return sent, failed

# Run the async function
#asyncio.run(send_reports())
