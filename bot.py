import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ✅ Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
GROUP_LINK = os.getenv("GROUP_LINK")

# Regex pattern for YouTube playlist links
YOUTUBE_PLAYLIST_REGEX = r"(https?://)?(www\.)?youtube\.com/playlist\?list=[\w-]+"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(GROUP_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            # ✅ User joined → prompt to send playlist
            await update.message.reply_text("Send the YouTube Playlist Link")
        else:
            # ❌ Not joined → send join link
            await update.message.reply_text(
                f"❌ Please join our channel first to use this bot:\n👉 {GROUP_LINK}"
            )
    except:
        await update.message.reply_text(
            f"❌ Please join our channel first to use this bot:\n👉 {GROUP_LINK}"
        )

# Handle YouTube playlist links
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if re.search(YOUTUBE_PLAYLIST_REGEX, text):
        user_id = update.effective_user.id
        try:
            member = await context.bot.get_chat_member(GROUP_ID, user_id)
            if member.status in ["member", "administrator", "creator"]:
                await update.message.reply_text(
                    "⚠️ Already 10/10 Process Running\n\n"
                    "👉 Bot is Overloaded. So, Try after a few minutes."
                )
            else:
                await update.message.reply_text(
                    f"❌ Please join our channel first to use this bot:\n👉 {GROUP_LINK}"
                )
        except:
            await update.message.reply_text(
                f"❌ Please join our channel first to use this bot:\n👉 {GROUP_LINK}"
            )

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()