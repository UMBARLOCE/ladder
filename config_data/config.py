import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    # exit("Переменные окружения не загружены т.к отсутствует файл .env")
    TG_BOT_TOKEN = input("Введите TOKEN телеграм-бота:\n")
    with open(".env", "w", encoding="utf-8") as file:
        file.write(f"TG_BOT_TOKEN = {TG_BOT_TOKEN}\n")

load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
