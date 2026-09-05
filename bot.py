import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Your secret words mapped to file paths
SECRET_FILES = {
    "vocab": "documents/vocab.pdf"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo! Send me one of your secret words and I'll drop the file.")

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
    else:
        await update.message.reply_text("Never heard of that word. Try another one!")

if __name__ == '__main__':
    application = ApplicationBuilder().token("8959582090:AAHg6Vj8NkahupJ8vC3EWt5iox6wRwgdFDo").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_secret_word))

    print("Bot is up and listening for secret words...")
    application.run_polling()