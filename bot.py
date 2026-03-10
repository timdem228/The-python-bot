import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = "YOUR_BOT_TOKEN"
OWNER = "@timdem228"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# состояние ожидания идеи
class IdeaState(StatesGroup):
    waiting_for_idea = State()


# меню снизу
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💡 Предложить идею")],
        [KeyboardButton(text="💖 Поддержка автора")],
        [KeyboardButton(text="👤 Автор")]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! Используй меню ниже 👇",
        reply_markup=menu
    )


# предложить идею
@dp.message(lambda message: message.text == "💡 Предложить идею")
async def suggest(message: types.Message, state: FSMContext):
    await message.answer("Напиши свою идею ✍️")
    await state.set_state(IdeaState.waiting_for_idea)


# получение идеи
@dp.message(IdeaState.waiting_for_idea)
async def get_idea(message: types.Message, state: FSMContext):

    username = message.from_user.username
    text = message.text

    await bot.send_message(
        OWNER,
        f"📩 Новая идея:\n\n{text}\n\n👤 @{username}"
    )

    await message.answer("Спасибо! Идея отправлена автору 👍")
    await state.clear()


# поддержка автора
@dp.message(lambda message: message.text == "💖 Поддержка автора")
async def donate(message: types.Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💰 DonateAlerts", url="https://dalink.to/timdem228")],
            [InlineKeyboardButton(text="💎 TON (@send)", url="https://t.me/send")]
        ]
    )

    await message.answer(
        "Поддержать автора:",
        reply_markup=keyboard
    )


# автор
@dp.message(lambda message: message.text == "👤 Автор")
async def author(message: types.Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Перейти в канал", url="https://t.me/scenaristpornuhi")]
        ]
    )

    await message.answer(
        "Канал автора:",
        reply_markup=keyboard
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
