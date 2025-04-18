import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение "{update.message.text}"')


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def get_time(update, context):
    await update.message.reply_text(datetime.now().strftime("%H:%M:%S"))


async def get_date(update, context):
    await update.message.reply_text(datetime.now().strftime("%d.%m.%Y"))


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", get_time))
    application.add_handler(CommandHandler("date", get_date))

    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
