import os
from dotenv import load_dotenv

def load_env():
    """
    Загружает переменные окружения из файла .env
    Вызывать нужно один раз при старте программы
    """
    load_dotenv()

def get_token():
    """
    Возвращает значение токена из переменной окружения TELEGRAM_TOKEN
    """
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("Токен TELEGRAM_TOKEN не найден в переменных окружения")
    return token
