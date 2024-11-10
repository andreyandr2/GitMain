import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Ваш API ключ OpenAI
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Токен Telegram-бота
TELEGRAM_TOKEN = "7858760812:AAHBQehxe8qqcO2IUDC_DN4sNAbNLxxJwRQ"

# Функция для перевода текста через ChatGPT
def translate_to_spanish(text):
    prompt = f"Переведи следующий текст с русского на испанский: \"{text}\""
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    translation = response.choices[0].text.strip()
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