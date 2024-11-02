from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

router = Router()
load_dotenv()

class Generate(StatesGroup):
    text = State()
    abstracts = State()
    newabstract = State()
    process_message = State()

@router.message(Generate.abstracts)
async def abstracts(message: Message, state: FSMContext):
    data = await state.get_data()
    abst = data.get('abstracts', [])
    if not abst:
        await message.answer('У вас нет созданных конспектов')
    else:
        mes = 'Выберите конспект:\n' + "\n".join(abst)
        await message.answer(mes)

@router.message(Generate.newabstract)
async def newabstract(message: Message, state: FSMContext):
    if message.text == "сгенерировать":
        await message.answer('Идёт генерация...')
        # логика генерации конспекта
        await message.answer('Готово!')
        await message.answer('*Самый классный конспект*')
    else:
        # логика суммирования данных
        None

@router.message(Generate.process_message)
async def process_message(message: Message, state: FSMContext):
    if message.text == "Мои конспекты":
        await state.set_state(Generate.abstracts)
    elif message.text == "Создать конспект":
        await message.answer('Отправь материалы, на основе которых сделать конспект. Нажми "сгенерировать" чтобы начать генерацию')
        await state.set_state(Generate.newabstract)
    else:
        await message.answer('Воспользуйтесь командой "Создать конспект" или "Мои конспекты"!')

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать в бот! Самое время создать свой первый конспект!')
    await state.update_data(
        abstract_name=[''],
        abstracts=['']
    )

@router.message()
async def generate(message: Message, state: FSMContext):
    if message.text or message.photo:
        await state.set_state(Generate.text)
        await process_message(message, state)

@router.message(Generate.text)
async def genera_error(message: Message):
    await message.answer('Подождите, ваше сообщение обрабатывается...')
