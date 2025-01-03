import asyncio
import logging
import sys
from os import getenv
import json

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage

from buttons_bot import main_keyboard, moderator_keyboard

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TOKEN")
storage = MemoryStorage()

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher(storage=storage)
user_indices = {}


with open('projects.json', 'r', encoding='utf-8') as file:
    orders = json.load(file)
    

def create_order_message(order):
    """Форматирование сообщения с информацией о заказе"""
    description = order['description'].replace("<br>", "\n")  # Заменяем <br> на перенос строки
    return (
        f"📋 <b>{order['title']}</b>\n"
        f"💰 Цена: {order['price']} рублей\n"
        f"📝 Описание: {description}\n"
        f"👤 Автор: <a href='{order['project_url']}'>{order['username']}</a>\n"
        f"🔗 [Ссылка на проект]({order['project_url']})"
    )


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Привет!, {html.bold(message.from_user.full_name)}!\nВот твое меню:",
        reply_markup=main_keyboard()
    )


@dp.message(F.text == "Kwork")
async def command_back_handler(message: Message) -> None:
    """
    Сообщение после команды `Kwork`
    """
    user_id = message.from_user.id
    user_indices[user_id] = 0  # Устанавливаем начальный индекс для пользователя

    # Формируем первое сообщение
    order = orders[user_indices[user_id]]
    msg = create_order_message(order)

    await message.answer(msg, parse_mode="HTML", reply_markup=moderator_keyboard())


@dp.callback_query(lambda call: call.data == "next_order")
async def next_order_handler(callback_query: CallbackQuery):
    """Обработка нажатия кнопки 'Далее'"""
    user_id = callback_query.from_user.id

    # Увеличиваем индекс или обнуляем, если достигнут конец списка
    user_indices[user_id] = (user_indices[user_id] + 1) % len(orders)

    # Формируем сообщение
    order = orders[user_indices[user_id]]
    msg = create_order_message(order)

    await callback_query.message.edit_text(msg, parse_mode="HTML", reply_markup=moderator_keyboard())
    await callback_query.answer()


@dp.callback_query(lambda call: call.data == "prev_order")
async def prev_order_handler(callback_query: CallbackQuery):
    """Обработка нажатия кнопки 'Назад'"""
    user_id = callback_query.from_user.id

    # Уменьшаем индекс или переходим к последнему заказу, если текущий индекс равен 0
    user_indices[user_id] = (user_indices[user_id] - 1) % len(orders)

    # Формируем сообщение
    order = orders[user_indices[user_id]]
    msg = create_order_message(order)

    await callback_query.message.edit_text(msg, parse_mode="HTML", reply_markup=moderator_keyboard())
    await callback_query.answer()


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())