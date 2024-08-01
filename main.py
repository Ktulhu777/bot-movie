# Python API
import asyncio
import logging
import sys

# Third party modules
from aiogram import Dispatcher, Bot, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.methods import DeleteWebhook

# Our modules
from config.config import TOKEN, PASSWORD_ADMIN
from service_database.service import add_user_in_db, add_movie_in_db, movie_exists, add_super_user, exists_super_user
from middlewares.session_db import DataBaseSession
from database_engine import async_session_maker
from utils.utils import on_startup, on_shotdown, markup_subscription, cancel_button
from states.default_states import MovieState, AdminState
from models.models import Movie

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

groups = ['@movie99F']


async def exampl_subscription(user_id) -> bool:
    """Проверяет подписан ли пользователь на все группы, если подписан то True"""
    result = [await bot.get_chat_member(chat_id=i, user_id=user_id) for i in groups]
    if all(map(lambda x: x.status != 'left', result)):
        return True
    return False


@dp.message(CommandStart())
async def start_bot(message: types.Message, session: AsyncSession):
    await add_user_in_db(pk_user=message.from_user.id, session=session)
    if not await exampl_subscription(user_id=message.from_user.id):
        await message.answer(
            f"""🙋🏻‍♂️ Здравствуйте, <i>{message.from_user.username}</i>, подпишитесь что бы получить доступ к боту.""",
            reply_markup=markup_subscription)
    else:
        await message.answer("🆔 Отправьте мне код фильма с описания видео.")


@dp.callback_query(F.data == 'subscription')
async def subscription_verification(callback: types.CallbackQuery):
    if await exampl_subscription(user_id=callback.from_user.id):
        await callback.message.edit_text("🎉 Поздравляю, теперь вы можете прислать мне код фильма 🎉",
                                         show_alert=True)
    else:
        await callback.message.answer("❌ Вы не подписались на все каналы.",
                                      show_alert=True,
                                      reply_markup=markup_subscription)


@dp.callback_query(F.data == 'cancel')
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция сброса FSM"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.edit_text("❌ Вы сделали отмену ❌")


@dp.message(Command('appoint_an_administrator'))
async def appoint_an_administrator(message: types.Message, state: FSMContext):
    await state.set_state(AdminState.password)
    await message.answer("🆔 Введите пароль от администратора", reply_markup=cancel_button)


@dp.message(AdminState.password)
async def appoint_an_administrator_process(message: types.Message, state: FSMContext, session: AsyncSession):
    if PASSWORD_ADMIN == message.text:
        await state.update_data(password=message.text)
        await add_super_user(id_super_user=message.from_user.id, session=session)
        await state.clear()
        await message.answer("✅ Отлично, вы добавлены как администратор бота.")
    else:
        await message.answer("❌ Неправильный пароль",  reply_markup=cancel_button)


@dp.message(Command('add_movie'))
async def start_add_movie_process(message: types.Message, state: FSMContext, session: AsyncSession):
    if await exists_super_user(id_super_user=int(message.from_user.id),
                               session=session):
        await message.answer("Введите название фильма.", reply_markup=cancel_button)
        await state.set_state(MovieState.title)
    else:
        await message.answer("Данная команда не доступна.")


@dp.message(MovieState.title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("🆔 Введите код фильма.", reply_markup=cancel_button)
    await state.set_state(MovieState.code_movie)


@dp.message(MovieState.code_movie)
async def process_code_movie(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text.isdigit():
        if await movie_exists(movie_code=int(message.text), session=session):
            await state.update_data(code_movie=message.text)
            await message.answer("✅ Добавлено в базу данных.")
            data = await state.get_data()  # dict
            await state.clear()
            await add_movie_in_db(movie_code=int(data['code_movie']), title=data['title'], session=session)
        else:
            await message.answer("❌ Данный код занят другим фильмом.", reply_markup=cancel_button)
    else:
        await message.answer("❌ Это не число введите пожалуйста целое число.", reply_markup=cancel_button)


@dp.message()
async def get_title_movie(message: types.Message, session: AsyncSession):
    if message.text.isdigit():
        if not await exampl_subscription(user_id=message.from_user.id):
            await message.answer("❌ Вы не подписались на все каналы.",
                                 reply_markup=markup_subscription)
        else:
            result: Movie = await movie_exists(movie_code=int(message.text), session=session, get_movie=True)
            if result is None:
                await message.answer(f"❌ По данному коду ничего не найдено.")
            else:
                await message.answer(f"✅ Название фильма: {result.title}.")
    else:
        await message.answer("❌ Отправьте мне целое число.")


async def main() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    dp.message.register(bot)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shotdown)
    dp.update.middleware(DataBaseSession(session_pool=async_session_maker))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
