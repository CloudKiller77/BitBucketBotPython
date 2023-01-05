from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_1 = KeyboardButton("/start")
button_2 = KeyboardButton("/requests")
button_3 = KeyboardButton("/currency")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.row(button_1, button_2, button_3)
