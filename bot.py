from datetime import datetime, time, timedelta
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
    "secret": "You found the hidden password! Good job.",
    "linnie": "Negap Kumushayyy bamisannn 😄."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Yo! Send me a secret word, type /help, or use /remind YYYY-MM-DD <message> to set reminders starting 3 days before at 4:00 PM."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("contact me at @snxr_a for assistance! Use /remind YYYY-MM-DD <message> to set a 3-day advance notice.")

async def alarm(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(chat_id=job.chat_id, text=f"⏰ {job.data}")

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        date_str = context.args[0]
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        reminder_text = " ".join(context.args[1:])
        
        if not reminder_text:
            reminder_text = f"Reminder for {date_str}!"

        reminder_time = time(16, 0, 0) # 4:00 PM
        days_before = [3, 2, 1] # 3 days in advance (e.g., if target is 24th, starts on the 21st)
        now = datetime.now()
        
        scheduled_count = 0
        for d in days_before:
            remind_date = target_date - timedelta(days=d)
            remind_datetime = datetime.combine(remind_date, reminder_time)
            
            if remind_datetime > now:
                context.job_queue.run_once(
                    alarm, 
                    when=remind_datetime, 
                    chat_id=update.effective_chat.id, 
                    data=f"Reminder ({d} days left until {date_str}): {reminder_text}"
                )
                scheduled_count += 1
        
        if scheduled_count > 0:
            await update.message.reply_text(f"Timer set! I will message you at 4:00 PM starting 3 days before {date_str}.")
        else:
            await update.message.reply_text("Those reminder dates are already in the past!")
            
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /remind YYYY-MM-DD <message>\nExample: /remind 2026-09-24 Project deadline")

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
    application.add_handler(CommandHandler('remind', set_reminder))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_secret_word))

    print("Bot is up and listening for secret words...")
    application.run_polling()