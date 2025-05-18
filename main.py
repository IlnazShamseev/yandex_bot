import json
import logging
from random import randint

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components import *

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = "8095134379:AAE4j6lv55NdJPoyIpFaSCQdZe0bp0Ah1ZU"

# Инициализация бота и диспетчера с FSM
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher()

db_debugger = DataBaseDebugging()

USERS = {}


# Обработчик команды /start
@dp.message(Command("start"))
async def bot_start(message: types.Message):
    info = json.loads(message.model_dump_json())
    print(info)

    USERS[info["chat"]["id"]] = User()
    USERS[info["chat"]["id"]].StartMessageId = message.message_id

    await message.answer(
        "Привет! Я бот от разработчика ILNI.\n"
    )
    await message.answer(
        text=(
            "Выберите действие:\n"
            "/log  Войти в систему\n"
            "/reg  Зарегистрироваться в системе\n"
        )
    )


@dp.message()
async def bot_message(message: types.Message, bot: Bot):
    info = json.loads(message.model_dump_json())
    print(info)

    user = USERS[info["chat"]["id"]]
    text = message.text

    # 1
    if user.Logged:
        pass

    # 2
    elif user.Log_Btn:
        if user.Login is None:
            user.Login = text
            await message.answer(
                text="Введите пароль"
            )
        elif user.Password is None:
            user.Password = text
            if db_debugger.check_user(login_=user.Login, password_=user.Password):
                user.Status = 1
                await message.answer(
                    text="Добро пожаловать\nЧтобы продолжить работу введите \help"
                )
            elif db_debugger.check_admin(login_=user.Login, password_=user.Password):
                user.Status = 2
                await message.answer(
                    text="Добро пожаловать\nЧтобы продолжить работу введите /help"
                )
            else:
                user.Login = None
                user.Password = None
                await message.answer(
                text="Неправильный логин или пароль"
                )
                await message.answer(
                    text="Введите логин"
                )
    # 3
    elif user.Reg_Btn:
        if user.Name is None:
            user.Name = text
            await message.answer(
                text="Придумайте логин"
            )
        elif user.Login is None:
            user.Login = text
            await message.answer(
                text="Придумайте пароль"
            )
        elif user.Password is None:
            user.Password = text
            await message.answer(
                text="В каком ты классе?\n"
                     "пример ввода: 11 a "
            )
        else:
            class_, letter_ = text.split()
            db_debugger.new_user(
                name_=user.Name,
                login_=user.Login, password_=user.Password,
                class_=class_, letter_=letter_
            )

            user.Logged = True
            await message.answer(text="Регистрация прошла успешно")
            await message.answer(
                text=f"Здравствуй {user.Name}"
            )


    elif text == "/log":
        user.Log_Btn = True
        await message.answer(
            text="Введите логин"
        )
    elif text == "/reg":
        user.Reg_Btn = True
        await message.answer(
            text="Как вас зовут?"
        )
    else:
        if not user.Login:
            await message.answer(
                text=f"Для начала авторизуйтесь в системе"
            )
        if user.Status == 1:
            await message.answer(
                text=f""
            )

    else:
        await message.answer(
            text="Я вас не понял("
        )
        await message.answer(
            text=(
                "Выберите действие:\n"
                "/log  Войти в систему\n"
                "/reg  Зарегистрироваться в системе\n"
            )
        )

    # await message.answer(
    #     text="Введите как вас зовут",
    #     keyboard=keyboard
    # )


# @dp.callback_query(F.data == "reg")
# async def bot_log(message: types.Message, bot: Bot, mes=F):
#     info = json.loads(message.model_dump_json())
#     print(info)
#     user = USERS[info["chat"]["id"]]
#     user.Reg_Btn = True
#     try:
#         if user.StartMessageId != -1:
#             await bot.delete_message(message.from_user.id, user.StartMessageId)
#             user.StartMessageId = -1
#     except TelegramBadRequest as ex:
#         user.StartMessageId = -1
#     if user.Name is None:
#         await message.answer(text="Введите как вас зовут")
#     elif user.


@dp.message()
async def bot_message(message: types.Message, bot: Bot):
    info = json.loads(message.model_dump_json())
    print(info)

    if USERS[info["chat"]["id"]].Logged:
        pass
    elif USERS[info["chat"]["id"]].Log_Btn:
        pass
    elif USERS[info["chat"]["id"]].Reg_Btn:
        pass


async def authorization(message: types.Message):
    await message.answer()


# @dp.message(Command("/log"))
# async def cmd_random(message: types.Message):
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="Нажми меня",
#         callback_data="random_value")
#     )
#     await message.answer(
#         "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
#         reply_markup=builder.as_markup()
#     )


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        text="Спасибо, что воспользовались ботом!",
        show_alert=True
    )
    # или просто await callback.answer()


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
