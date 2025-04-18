import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

TIMER = 5


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = f'Вернусь через 5 с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


async def set_timer_2(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    try:
        temp = int(context.args[0])
        if temp < 0:
            await update.effective_message.reply_text('В прошлое мы не отправляемся')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, temp, chat_id=chat_id, name=str(chat_id), data=temp)

        text = f'Вернусь через {temp} с.!'
        if job_removed:
            text += ' Старая задача удалена.'
        await update.effective_message.reply_text(text)

    except(IndexError, ValueError):
        await update.effective_message.reply_text('Использование: /set_timer <секунд>')


async def task(context):
    """Выводит сообщение"""
    job = context.job
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {job.data}c. прошли!')


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?", reply_markup=markup)


async def get_time(update, context):
    await update.message.reply_text(datetime.now().strftime("%H:%M:%S"))


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение "{update.message.text}"')


async def get_date(update, context):
    await update.message.reply_text(datetime.now().strftime("%d.%m.%Y"))


async def help_command(update, context):
    await update.message.reply_text("Я бот справочник.")


async def address(update, context):
    await update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


async def phone(update, context):
    await update.message.reply_text("Телефон: +7(495)776-3030")


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


async def work_time(update, context):
    await update.message.reply_text(
        "Время работы: круглосуточно.")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_timer", set_timer_2))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", get_time))
    application.add_handler(CommandHandler("date", get_date))
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("phone", phone))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("work_time", work_time))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("close", close_keyboard))

    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
