import logging

import urllib3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, Message
from aiogram.utils.markdown import text, bold, code
from urllib3.exceptions import InsecureRequestWarning

import bitBacketUtils
import utils
import jsonWork
from currency import ExchangeCurrency
from keyboards import kb_client
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = utils.TOKEN
repository = bitBacketUtils.REPO_NAME
project = bitBacketUtils.PROJECT_NAME

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()
# -1001664997152

global user_id
global mess
size_2 = jsonWork.read_last_count()["last_count"]

# Configure logging
logging.root.handlers = []
# Логгирование по умолчанию в файл
logging.basicConfig(filename='bot_info.log',
                    filemode="w",
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

# Установка логгирования ОШИБОК в консоли
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
# Установка заданного формата вывода в консоли
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# Игнорировать предупреждение InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


async def start(_):
    """
    Инфо команда о состоянии бота при запуске (выводится в консоль), запускает расписание
    """
    schedule_jobs()
    print("Привет! Я бот)")


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    """
    Стартовая команда, для приветствия и инфо о боте
    """
    try:
        msg = text(code("Привет, это бот BitBucket\n") +
                    code("Для проекта:  ") + bold(project.upper() + "\n") +
                    code("Репозитория:  ") + bold(repository + "\n") +
                    code("Нажмите, просмотреть:   ") + bold("/requests") + "\n" +
                    code("Посмотреть курсы валют:  ") + bold("/currency"))

        await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_client)
    except:
        await message.reply("ВАЖНО: Вам нужно добавиться к боту, все уведомления идут в ЛС!!!")


@dp.message_handler(commands=['currency'])
async def send_today_currency(message: types.Message):
    """
    Команда для вывода Курса вылют на текуший день

    :currency Курс валют (59.8378)
    :param message: класс Message от которого можно использовать
                    разные методы отправки сообщений
    :return: currency Курс валют (59.8378)
    """
    try:
        currency = ExchangeCurrency()
        msg = text(code("📌 Курсы валют на сегодня:\n") +
                   currency.get_currency_info())
        await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_client)
    except:
        await message.reply("Возникла ошибка, повторите команду! Или добавьтесь к боту!")


@dp.message_handler(commands=['branches'])
async def send_group_open_requests(message: Message):
    """
    Команда для вывода Pull-requests в группу

    :param message: класс Message от которого можно использовать
                    разные методы отправки сообщений
    """
    size = bitBacketUtils.get_size_pull_requests()
    try:
        msg = text("🔥 У вас есть - " + bold(str(size)) + " Pull requests в статусе OPEN:\n")
        await bot.send_message(message.chat.id, msg, parse_mode=ParseMode.MARKDOWN)
    except:
        await message.reply("❗ Возникла ошибка, повторите команду! Или добавьтесь к боту!")

    try:
        if size == 0:
            msg = text("Pull requests в статусе OPEN нету")
            await bot.send_message(message.chat.id, msg, parse_mode=ParseMode.MARKDOWN)
        else:
            for request in bitBacketUtils.get_open_pull_requests():
                mess = text("🔹 Имя автора:  " + bold(request["Имя автора"]) + "\n"
                            "🔹 Имя ветки:  " + request["Commit branch"].replace("_", " ") + "\n"                                   
                            "Состояние:  " + code(request["Состояние"]) + "\n"                         
                            "👉 Кол-во проверок:  " + bold(str(request["Кол-во проверок"])) + "\n"
                            "👉 Кол-во комментариев:  " + bold(str(request["Кол-во комментариев"])) + "\n"                                                              
                            "🙏 Проверьте меня): ", request["Проверьте меня)"])
                await bot.send_message(message.chat.id, mess, parse_mode=ParseMode.MARKDOWN)
    except:
        await message.reply("❗ Возникла ошибка, повторите команду! Или добавьтесь к боту!")


@dp.message_handler(commands=['requests'])
async def send_open_pull_requests(message: Message):
    """
    Команда для вывода Pull-requests в личку пользователю

    :param message: класс Message от которого можно использовать
                    разные методы отправки сообщений
    """
    size = bitBacketUtils.get_size_pull_requests()
    try:
        msg = text("🔥 У вас есть - " + bold(str(size)) + " Pull requests в статусе OPEN:\n")
        await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)
    except:
        await message.reply("❗ Возникла ошибка, повторите команду! Или добавьтесь к боту!")

    try:
        if size == 0:
            msg = text("Pull requests в статусе OPEN нет")
            await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)
        else:
            for request in bitBacketUtils.get_open_pull_requests():
                mess = text("🔹 Имя автора:  " + bold(request["Имя автора"]) + "\n"
                            "🔹 Имя ветки:  " + request["Commit branch"].replace("_", " ") + "\n"                                   
                            "Состояние:  " + code(request["Состояние"]) + "\n"                         
                            "Роль:  " + code(request["Роль"]) + "\n"
                            "Статус проверки:  " + code(request["Статус проверки"]) + "\n"
                            "👉 Кол-во проверок:  " + bold(str(request["Кол-во проверок"])) + "\n"
                            "👉 Кол-во комментариев:  " + bold(str(request["Кол-во комментариев"])) + "\n"
                            "🙏 Проверьте меня): ", request["Проверьте меня)"])
                await bot.send_message(message.from_user.id, mess, parse_mode=ParseMode.MARKDOWN)
    except:
        await message.reply("❗ Возникла ошибка, повторите команду! Или добавьтесь к боту!")


async def scheduler_start(message: Message):
    """
    Вывод Pull-requests в группу по графику

    :param size: Кол-во элементов в массиве с реквестами
    :param message: класс Message от которого можно использовать
                    разные методы отправки сообщений
    :param mess: Сообщение с реквестом
    """
    size = bitBacketUtils.get_size_pull_requests()
    global size_2

    try:
        if size > size_2:
            try:
                msg = text("🔥 У вас есть - " + bold(str(size)) + " Pull requests в статусе OPEN:\n")
                await bot.send_message("id группы", msg, parse_mode=ParseMode.MARKDOWN)
            except:
                await message.reply("❗ ВАЖНО: Вам нужно добавиться к боту, все уведомления идут в ЛС!!!")

            for request in bitBacketUtils.get_open_pull_requests():
                mess = text("🔹 Имя автора:  " + bold(request["Имя автора"]) + "\n"
                            "🔹 Имя ветки:  " + request["Commit branch"].replace("_", " ") + "\n"
                            "Состояние:  " + code(request["Состояние"]) + "\n"
                            "Роль:  " + code(request["Роль"]) + "\n"
                            "👉 Кол-во проверок:  " + bold(str(request["Кол-во проверок"])) + "\n"
                            "👉 Кол-во комментариев:  " + bold(str(request["Кол-во комментариев"])) + "\n"
                            "🙏 Проверьте меня): ", request["Проверьте меня)"])
                await bot.send_message("id группы", mess, parse_mode=ParseMode.MARKDOWN)
            print("Wow " + str(size) + " " + str(size_2))
            size_2 = size
            jsonWork.write_last_count("last_count", size_2)
        else:
            size_2 = size
            jsonWork.write_last_count("last_count", size_2)
        print(str(size) + " " + str(size_2))
    except:
        await message.reply("❗ Возникла ошибка, повторите команду! Или добавьтесь к боту!")
        print("Error")

    await send_info_about_comment(size, bitBacketUtils.get_new_comment_request())


async def send_info_about_comment(size: int, list_requests: list):
    try:
        if size > 0:
            for request in list_requests:
                mess = text("🔥 У вас есть новый комментарий!!!\n" + "\n"
                            "❇ Имя автора:  " + bold(request["Имя автора"]) + "\n"
                            "❇ Имя ветки:  " + request["Commit branch"].replace("_", " ") + "\n"
                            "👉 Кол-во комментариев:  " + bold(str(request["Кол-во комментариев"])) + "\n"
                            "🙏 Проверьте меня):  ", request["Проверьте меня)"])
                await bot.send_message("id группы", mess, parse_mode=ParseMode.MARKDOWN)
        else:
            print("Нет реквестов")
    except:
        print("Error")


def schedule_jobs():
    """
    Настройка расписания для вывода Pull-reauests в группу

    :param scheduler: Для настройки расписания (создание графиков исполнения команд)
    :return: Сообщает о Pull-requests в группу по расписанию
    """
    scheduler.add_job(scheduler_start,
                      "interval",
                      minutes=2,
                      args=(Message,))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp,
                           skip_updates=True,
                           timeout=10000,
                           on_startup=start)
