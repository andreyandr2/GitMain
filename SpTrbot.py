import openai
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Загружаем переменные окружения из .env файла
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Устанавливаем ключ OpenAI
openai.api_key = OPENAI_API_KEY

# Функция для перевода текста через ChatGPT
def translate_to_spanish(text):
    messages = [
        {"role": "system", "content": "Ты переводчик с русского на испанский."},
        {"role": "user", "content": f"Переведи следующий текст с русского на испанский: \"{text}\""}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=100,
        temperature=0.7
    )
    translation = response.choices[0].message.content.strip()
    return translation

# Обработчик сообщений
async def handle_message(update: Update, context):
    user_text = update.message.text
    try:
        translated_text = translate_to_spanish(user_text)
        await update.message.reply_text(translated_text)
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при переводе. Попробуйте снова позже.")
        print(f"Ошибка: {e}")

# Команда /start
async def start_command(update: Update, context):
    await update.message.reply_text("Привет! Отправь мне текст на русском, и я переведу его на испанский.")

# Основная функция
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()