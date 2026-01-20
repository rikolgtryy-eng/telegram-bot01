from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os

TOKEN = "BOT_TOKEN"

FILTER_FILE = "filters.json"

def load_filters():
    if not os.path.exists(FILTER_FILE):
        return {}
    with open(FILTER_FILE, "r") as f:
        return json.load(f)

def save_filters(data):
    with open(FILTER_FILE, "w") as f:
        json.dump(data, f)

filters_data = load_filters()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot အလုပ်လုပ်နေပါတယ် ✅")

async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return

    if len(context.args) < 2:
        await update.message.reply_text("အသုံးပြုပုံ: /filter keyword reply")
        return

    keyword = context.args[0].lower()
    reply = " ".join(context.args[1:])

    filters_data[keyword] = reply
    save_filters(filters_data)

    await update.message.reply_text(f"Filter ထည့်ပြီးပါပြီ ✅ ({keyword})")

async def check_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    for key, reply in filters_data.items():
        if key in text:
            await update.message.reply_text(reply)
            break

async def dm_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("မင်္ဂလာပါ 👋 စာရထားပါတယ်")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
