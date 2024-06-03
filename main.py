import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

n = 1

API_TOKEN = '7393947317:AAEiQvRCjdVKw1rdxLatveeLEjxVapmAaEU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Game(StatesGroup):
    question = State()
    answer = State()

questions = [
    {"question": "Какое животное является символом США?",
     "answers": ["Орел", "Медведь", "Слон", "Лось"],
     "correct_answer": "Орел"},
    {"question": "Какой музыкальный инструмент изображен на флаге Ирландии?",
     "answers": ["Гитара", "Арфа", "Флейта", "Аккордеон"],
     "correct_answer": "Арфа"},
    {"question": "Какая страна является самой большой по площади?",
     "answers": ["Россия", "Канада", "Китай", "США"],
     "correct_answer": "Россия"},
    {"question": "Как называется столица Италии?",
     "answers": ["Неаполь", "Милан", "Венеция", "Рим"],
     "correct_answer": "Рим"},
    {"question": "Какое животное является символом Китая?",
     "answers": ["Собака", "Дракон", "Панда", "Леопард"],
     "correct_answer": "Панда"}
]

def get_random_question():
    return random.choice(questions)

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    await message.reply("Привет! Хочешь стать миллионером? Начни игру с /играть")

@dp.message_handler(commands=['играть'])
async def play_game(message: types.Message, state: FSMContext):
    question = get_random_question()
    await state.update_data(question=question)
    await message.answer(question["question"])
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for answer in question["answers"]:
        keyboard.add(answer)
    await message.answer("Выбери правильный ответ:", reply_markup=keyboard)
    await state.set_state(Game.answer)


@dp.message_handler(state=Game.answer)
async def check_answer(message: types.Message, state: FSMContext):
    global n
    if (n != 5):
        data = await state.get_data()
        question = data['question']
        n = n + 1
        if message.text == question["correct_answer"]:
            await message.reply("Правильно! Ты на шаг ближе к миллиону!")
            await play_game(message, state)
        else:
            await message.reply(f"Неверно! Правильный ответ: {question['correct_answer']}")
            await message.answer("Игра окончена!")
            await state.finish()

    elif (n==5):
        await message.answer(f"Поздравляем, Вы выиграли миллион!!\n\n(Если хочешь сыграть заново, то перезапусти бота)")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

