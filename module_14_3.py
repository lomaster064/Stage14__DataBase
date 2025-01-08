from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import keys

api_key = keys.api_key

bot = Bot(token=api_key)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text="Купить")
kb.add(button1, button2)
kb.add(button3)

kb_inline = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button4 = InlineKeyboardButton(text="Формула расчёта", callback_data="formulas")
kb_inline.add(button3, button4)

kb_inline2 = InlineKeyboardMarkup(row_width=4)
prod1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
prod2 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
prod3 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
prod4 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
kb_inline2.add(prod1, prod2, prod3, prod4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start_command(message):
    await message.answer('Привет! Я бот для рассчёта каллорий для похудения.', reply_markup=kb)


@dp.message_handler(text=["Информация"])
async def inform(message):
    await message.answer('Информация о боте.')


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}")
        await message.answer_photo(photo=open(f"product{i}.jpg", "rb"))

    await message.answer("Выберите продукт для покупки:", reply_markup=kb_inline2)


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    u_age = int(data['age'])
    u_weight = float(data['weight'])
    u_growth = float(data['growth'])
    calories = 10 * u_weight + 6.25 * u_growth - 5 * u_age
    await message.answer(f"Ваша норма каллорий: {calories}")
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
