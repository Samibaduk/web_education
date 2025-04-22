import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text(
        "Привет. Добро пожаловать в музей!\n"
        "Пожалуйста, сдайте верхнюю одежду в гардероб.\n"
        "Приглашаем вас в первый зал room_1")
    return 1


async def repeat_text(update, context):
    await update.message.reply_text(
        "Что вы имели ввиду?\n")


async def room_1(update, context):
    await update.message.reply_text(
        "В данном зале представлен скелет Мегаладона!\n"
        "Проходите в следующий зал room_2\n"
        "Или вы можете покинуть музей exit")
    return 2


async def room_2(update, context):
    await update.message.reply_text(
        "Представлена выставка дирижаблей. Имейте при себе огнетушитель!\n"
        "Проходите в третий зал room_3\n")
    return 3


async def room_3(update, context):
    await update.message.reply_text(
        "Комната готической культуры. Надеюсь, у вас с собой чеснок...\n"
        "Проходите в следующий зал room_4\n"
        "Или, если вам надоело, вернитесь в первый зал room_1")
    return 4


async def room_4(update, context):
    await update.message.reply_text(
        "Экскурсия завершена. Здесь вы можете поесть тематической еды!\n"
        "Возвращайтесь в первый зал room_1\n")
    return 1


async def exit(update, context):
    await update.message.reply_text(
        "Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, repeat_text),
                CommandHandler('room_1', room_1)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, repeat_text),
                CommandHandler('room_2', room_2)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, repeat_text),
                CommandHandler('room_3', room_3)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, repeat_text),
                CommandHandler('room_4', room_4),
                CommandHandler('room_1', room_1)]
        },

        fallbacks=[CommandHandler('exit', exit)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
