
1) Ввести актуальные данные, токен вашего бота, данные к ресурсу (BitBucket)

TOKEN = "telegramm_token_bot"

HOST_NAME = "адресс ресурса где находится проект"
USER_NAME = "логин"
USER_PASSWORD = "пароль"

2) Ввести данные по проекту BitBucket

PROJECT_NAME = "имя проекта"
REPO_NAME = "имя репозитория"

3) Ввести id группы, там где будет работать бот

await bot.send_message("id группы", mess, parse_mode=ParseMode.MARKDOWN)

4) Переименовать файл UtilsBot.py -> Utils.py
