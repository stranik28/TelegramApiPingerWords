import os
from dotenv import load_dotenv
import asyncio
import aiohttp
import json
from aiogram import Bot, Dispatcher, types

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


async def get_log_pass():
    load_dotenv()

    # Извлечение логина и пароля из переменных окружения
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    return login, password


async def login():
    login_data = "http://212.109.221.160:7777/auth"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    async with aiohttp.ClientSession() as session:
        username, password = await get_log_pass()
        payload = {
            "username": username,
            "password": password
        }

        async with session.post(login_data, data=payload, headers=headers) as response:
            data = await response.json()
            token = data.get('access_token')
            return token


async def get_branch(phrase: str, token: str) -> str:
    url = f"http://212.109.221.160:7777/scenarios/statistics/test?phrase={phrase}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + token
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()

            max_weights_divided = 0
            max_weights_divided_branch = None
            for branch, branch_data in data.items():
                branch_data_partial = branch_data['partial']
                if branch_data_partial["hits"] == 0:
                    continue
                else:
                    if branch_data_partial["weights_divided"] > max_weights_divided:
                        max_weights_divided_branch = {branch: branch_data_partial}
                        max_weights_divided = branch_data_partial["weights_divided"]

            if max_weights_divided_branch:
                return json.dumps(max_weights_divided_branch, indent=4, ensure_ascii=False)
            else:
                return "Нет данных о ветках в ответе"


@dp.message()
async def echo(message: types.Message):
    phrase = message.text
    token = await login()
    if not token:
        await message.reply("Ошибка: токен не установлен")
        return
    result = await get_branch(phrase, token)
    await message.reply(result)


async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
