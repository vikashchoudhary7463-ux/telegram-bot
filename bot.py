from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import yt_dlp
import os

TOKEN = os.getenv("BOT_TOKEN")

os.makedirs("downloads", exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("⬇️ Downloader", callback_data="dl")]]
    await update.message.reply_text(
        "Welcome! Click below 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["mode"] = "dl"
    await query.edit_message_text("Send a YouTube / Instagram link")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("mode") == "dl":
        await update.message.reply_text("Downloading...")
        ydl_opts = {"outtmpl": "downloads/%(title)s.%(ext)s"}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(update.message.text, download=True)
                file = ydl.prepare_filename(info)
            await update.message.reply_video(video=open(file, "rb"))
            os.remove(file)
        except Exception:
            await update.message.reply_text("❌ Failed. Try another link.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("Bot running...")
app.run_polling()

