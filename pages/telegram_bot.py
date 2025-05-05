import json
import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7226566019:AAFbejFkrE5U4_TbtJ_qrMLGOhXBEqg7NT0"
PARENTS_FILE = "parents.json"

# Load or create parents.json
def load_parents():
    if os.path.exists(PARENTS_FILE):
        with open(PARENTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_parents(data):
    with open(PARENTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("Share Contact", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please share your contact so we can send you updates.", reply_markup=markup)

# Handles contact
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone_number = contact.phone_number
    chat_id = update.message.chat_id

    parents = load_parents()
    parents[phone_number] = chat_id
    save_parents(parents)

    await update.message.reply_text(f"Thank you! Your number has been registered.")

# Run bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

