import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Words that trigger a file response
SECRET_FILES = {
    "vocab": "documents/vocab.pdf"
}

# Words that trigger a text message response
SECRET_TEXTS = {
    "hello": "Hey there! Welcome to my hybrid bot.",
    "secret": "You found the hidden password! Good job."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo! Send me a secret word to get a file or a text response, or type /help for assistance.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send 'vocab' for a file, or try other secret words like 'hello' or 'secret' for text!")

async def handle_secret_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    
    if text in SECRET_FILES:
        file_path = SECRET_FILES[text]
        try:
            await update.message.reply_chat_action("upload_document")
            with open(file_path, 'rb') as file_to_send:
                await update.message.reply_document(document=file_to_send)
        except FileNotFoundError:
            await update.message.reply_text(f"Oops! I found the keyword, but the file at {file_path} is missing.")
            
    elif text in SECRET_TEXTS:
        response_text = SECRET_TEXTS[text]
        await update.message.reply_text(response_text)
        
    else:
        await update.message.reply_text("Never heard of that word. Try another one!")

if __name__ == '__main__':
    TOKEN = os.environ.get("BOT_TOKEN")
    
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_secret_word))

    print("Bot is up and listening for secret words...")
    application.run_polling()