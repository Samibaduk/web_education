import logging
from pyexpat.errors import messages

from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

AUTHOR = "Сергей Есенин"
TITLE = "Берёза"
POEM = ("""Белая берёза
Под моим окном
Принакрылась снегом,
Точно серебром.
На пушистых ветках
Снежною каймой
Распустились кисти
Белой бахромой.
И стоит берёза
В сонной тишине,
И горят снежинки
В золотом огне.
А заря, лениво
Обходя кругом,
Обсыпает ветки
Новым серебром.""").split('\n')


async def start(update, context):
    await update.message.reply_text(
        f"Бот литератор поможет вам выучить стихотворение {TITLE} - {AUTHOR}\n"
        f"Читать будем построчно. Я начинаю:\n"
        f"{POEM[0]}")
    context.user_data['count_line'] = 1


async def suphler(update, context):
    await update.message.reply_text(
        f"{POEM[context.user_data['count_line']]}")


async def speech_bot(update, context):
    if context.user_data['count_line'] == len(POEM):
        context.user_data['count_line'] = 0
        await update.message.reply_text(
            "Вы справились!")
        return
    message = update.message.text
    if message == POEM[context.user_data['count_line']]:
        context.user_data['count_line'] += 1
        if context.user_data['count_line'] == len(POEM):
            context.user_data['count_line'] = 0
            await update.message.reply_text(
                "Вы справились!")
            return
        await update.message.reply_text(
            f"{POEM[context.user_data['count_line']]}")
        context.user_data['count_line'] += 1
    else:
        await update.message.reply_text(
            f"Вы ошиблись. /suphler")


async def stop(update, context):
    context.user_data['count_line'] = 0
    await update.message.reply_text(
        "До свидания")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, speech_bot))
    application.add_handler(CommandHandler('suphler', suphler))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.run_polling()


if __name__ == '__main__':
    main()
