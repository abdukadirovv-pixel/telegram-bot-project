from datetime import datetime, time
import logging
import os
import random
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Timezone configuration for Uzbekistan
TZ = ZoneInfo("Asia/Tashkent")

# Motivational quotes list
QUOTES = [
    "“The secret of getting ahead is getting started.” — Mark Twain",
    "“Don’t watch the clock; do what it does. Keep going.” — Sam Levenson",
    "“Success is the sum of small efforts, repeated day in and day out.” — Robert Collier",
    "“The expert in anything was once a beginner.” — Helen Hayes",
    "“Future belongs to those who believe in the beauty of their dreams.” — Eleanor Roosevelt",
    "“It always seems impossible until it’s done.” — Nelson Mandela",
    "“Small progress each day adds up to big results.” — Satya Nui",
]


def get_random_quote():
  return random.choice(QUOTES)


# Secret Files and Texts Configuration
SECRET_FILES = {"vocab": "documents/vocab.pdf"}

SECRET_TEXTS = {
    "hello": "Hey there! Welcome to my hybrid bot.",
    "secret": "You found the hidden password! Good job.",
    "linni": "matemman misal ishla hehe.",
}

# Complete Timetable Mapping (0: Monday, 4: Friday)
TIMETABLE = {
    0: [  # Monday
        {
            "num": 1,
            "time": "09:00 - 09:45",
            "subject": "Algebra",
            "room": "218",
            "teacher": "Umid / Muhammadsodiq",
        },
        {
            "num": 2,
            "time": "09:50 - 10:35",
            "subject": "Kelajak soati",
            "room": "204",
            "teacher": "Umarbek",
        },
        {
            "num": 3,
            "time": "10:40 - 11:25",
            "subject": "Ona tili",
            "room": "208",
            "teacher": "Q.Umid",
        },
        {
            "num": 4,
            "time": "11:30 - 12:15",
            "subject": "Informatika",
            "room": "220",
            "teacher": "Xursand / Umarbek",
        },
        {
            "num": 5,
            "time": "12:45 - 13:25",
            "subject": "Ingliz tili",
            "room": "220",
            "teacher": "Rufat / Muzaffar",
        },
        {
            "num": 6,
            "time": "13:30 - 14:10",
            "subject": "Rus tili",
            "room": "128",
            "teacher": "Gulzoda / Sevara",
        },
        {
            "num": 7,
            "time": "14:15 - 14:55",
            "subject": "Fizika",
            "room": "202",
            "teacher": "O'g'iljon / Ulug'bek",
        },
    ],
    1: [  # Tuesday
        {
            "num": 1,
            "time": "09:00 - 09:45",
            "subject": "O'zbek tarix",
            "room": "113",
            "teacher": "Murod",
        },
        {
            "num": 2,
            "time": "09:50 - 10:35",
            "subject": "Adabiyot",
            "room": "208",
            "teacher": "Q.Umid",
        },
        {
            "num": 3,
            "time": "10:40 - 11:25",
            "subject": "Algebra",
            "room": "218",
            "teacher": "Umid / Muhammadsodiq",
        },
        {
            "num": 4,
            "time": "11:30 - 12:15",
            "subject": "Geometriya",
            "room": "218",
            "teacher": "Umid / Muhammadsodiq",
        },
        {
            "num": 5,
            "time": "12:45 - 13:25",
            "subject": "CHQBT",
            "room": "220",
            "teacher": "To'qin",
        },
        {
            "num": 6,
            "time": "13:30 - 14:10",
            "subject": "Ingliz tili",
            "room": "220",
            "teacher": "Rufat / Muzaffar",
        },
        {
            "num": 7,
            "time": "14:15 - 14:55",
            "subject": "Fizika",
            "room": "202",
            "teacher": "O'g'iljon / Ulug'bek",
        },
    ],
    2: [  # Wednesday
        {
            "num": 1,
            "time": "09:00 - 09:45",
            "subject": "Ona tili",
            "room": "208",
            "teacher": "Q.Umid",
        },
        {
            "num": 2,
            "time": "09:50 - 10:35",
            "subject": "Algebra",
            "room": "218",
            "teacher": "Umid / Muhammadsodiq",
        },
        {
            "num": 3,
            "time": "10:40 - 11:25",
            "subject": "Fizika",
            "room": "202",
            "teacher": "O'g'iljon / Ulug'bek",
        },
        {
            "num": 4,
            "time": "11:30 - 12:15",
            "subject": "Rus tili",
            "room": "128",
            "teacher": "Gulzoda / Sevara",
        },
        {
            "num": 5,
            "time": "12:45 - 13:25",
            "subject": "Ingliz tili",
            "room": "220",
            "teacher": "Rufat / Muzaffar",
        },
        {
            "num": 6,
            "time": "13:30 - 14:10",
            "subject": "CHQBT",
            "room": "129",
            "teacher": "To'qin",
        },
    ],
    3: [  # Thursday
        {
            "num": 1,
            "time": "09:00 - 09:45",
            "subject": "Tarbiya",
            "room": "132",
            "teacher": "Azada",
        },
        {
            "num": 2,
            "time": "09:50 - 10:35",
            "subject": "Fizika",
            "room": "202",
            "teacher": "O'g'iljon / Ulug'bek",
        },
        {
            "num": 3,
            "time": "10:40 - 11:25",
            "subject": "Algebra",
            "room": "218",
            "teacher": "Umid / Muhammadsodiq",
        },
        {
            "num": 4,
            "time": "11:30 - 12:15",
            "subject": "Geometriya",
            "room": "218",
            "teacher": "Umid / Muhammadsodiq",
        },
        {
            "num": 5,
            "time": "12:45 - 13:25",
            "subject": "Ingliz tili",
            "room": "220",
            "teacher": "Rufat / Muzaffar",
        },
        {
            "num": 6,
            "time": "13:30 - 14:10",
            "subject": "Adabiyot",
            "room": "208",
            "teacher": "Q.Umid",
        },
    ],
    4: [  # Friday
        {
            "num": 1,
            "time": "09:00 - 09:45",
            "subject": "Jismoniy tarbiya",
            "room": "Sport zal",
            "teacher": "Ulug'bek",
        },
        {
            "num": 2,
            "time": "09:50 - 10:35",
            "subject": "Geometriya",
            "room": "218",
            "teacher": "Umid / Muhammadsodiq",
        },
        {
            "num": 3,
            "time": "10:40 - 11:25",
            "subject": "O'zbek tarix",
            "room": "113",
            "teacher": "Murod",
        },
        {
            "num": 4,
            "time": "11:30 - 12:15",
            "subject": "Fizika",
            "room": "202",
            "teacher": "O'g'iljon / Ulug'bek",
        },
        {
            "num": 5,
            "time": "12:45 - 13:25",
            "subject": "Jahon tarix",
            "room": "113",
            "teacher": "Murod",
        },
        {
            "num": 6,
            "time": "13:30 - 14:10",
            "subject": "Informatika",
            "room": "220",
            "teacher": "Xursand / Umarbek",
        },
    ],
}

DAY_NAMES = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
}

active_chats = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  chat_id = update.effective_chat.id
  active_chats.add(chat_id)
  await update.message.reply_text(
      "🤖 *School Assistant Bot Activated!*\n\n"
      "You will receive a **15-minute warning message every morning at 08:45 AM** "
      "with your full daily schedule and a fresh motivational quote!\n\n"
      "Send me a secret word (like `vocab`), type /help, or use /remind to set reminders.",
      parse_mode="Markdown",
  )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(
      "Contact me at @snxr_a for assistance!\n"
      "• Use /remind YYYY-MM-DD <message> to set a 3-day advance notice.\n"
      "• Type secret words like 'vocab', 'hello', or 'secret' for hidden triggers."
  )


async def send_morning_warning(context: ContextTypes.DEFAULT_TYPE):
  now = datetime.now(TZ)
  day_index = now.weekday()

  if day_index not in TIMETABLE:
    return

  lessons = TIMETABLE[day_index]
  day_name = DAY_NAMES[day_index]
  quote = get_random_quote()

  message_lines = [
      "🔔 *15-Min Warning: Your lessons start in 15 minutes (at 09:00 AM)!*\n",
      f"📋 *Today's Schedule ({day_name}):*\n",
  ]
  for lesson in lessons:
    message_lines.append(
        f"*{lesson['num']}. {lesson['subject']}* ({lesson['time']})\n"
        f"🏫 Room: {lesson['room']} | 👨‍🏫 {lesson['teacher']}\n"
    )

  message_lines.append(f"\n💡 *Motivation for today:* _{quote}_")

  full_text = "\n".join(message_lines)

  for chat_id in active_chats:
    try:
      await context.bot.send_message(
          chat_id=chat_id, text=full_text, parse_mode="Markdown"
      )
    except Exception as e:
      logger.error(f"Failed to send morning warning to {chat_id}: {e}")


async def handle_secret_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
  chat_id = update.effective_chat.id
  active_chats.add(chat_id)  # Auto-register chat on secret word use
  text = update.message.text.strip().lower()

  if text in SECRET_FILES:
    file_path = SECRET_FILES[text]
    try:
      await update.message.reply_chat_action("upload_document")
      with open(file_path, "rb") as file_to_send:
        await update.message.reply_document(document=file_to_send)
    except FileNotFoundError:
      await update.message.reply_text(
          f"Oops! I found the keyword, but the file at {file_path} is missing."
      )

  elif text in SECRET_TEXTS:
    response_text = SECRET_TEXTS[text]
    await update.message.reply_text(response_text)

  else:
    await update.message.reply_text(
        "Never heard of that word. Try another one!"
    )


if __name__ == "__main__":
  TOKEN = os.environ.get("BOT_TOKEN")

  application = ApplicationBuilder().token(TOKEN).build()

  # Command handlers
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("help", help_command))

  # Secret word / text handler
  application.add_handler(
      MessageHandler(filters.TEXT & (~filters.COMMAND), handle_secret_word)
  )

  # Automated 08:45 AM daily schedule warning job queue
  job_queue = application.job_queue
  for day_index in TIMETABLE.keys():
    job_queue.run_daily(
        send_morning_warning, time=time(8, 45, tzinfo=TZ), days=(day_index,)
    )

  print(
      "Bot is up and listening for secret words with automated morning"
      " schedule alerts..."
  )
  application.run_polling()