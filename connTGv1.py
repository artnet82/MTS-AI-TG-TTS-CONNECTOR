from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для синтеза речи.")

def handle_text(update: Update, context):
    text = update.message.text

    # Ограничение на количество символов
    if len(text) > 4000:
        text = text[:4000]

    config = read_api_config()
    synthesize_stream(text, config["API"]["server_address"], config["Auth"])

    # Отправка аудиофайла пользователю
    audio_file = open("synthesized_audio.wav", "rb")
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_file)

def main():
    config = read_api_config()
    updater = Updater(token=config["Telegram"]["bot_token"], use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
