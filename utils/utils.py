from aiogram import types


async def on_startup():
    print("Бот включен")


async def on_shotdown():
    print("Бот выключен")


markup_subscription = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='Канал 1', url='t.me/movie99F')],
    [types.InlineKeyboardButton(text='✅ Я подписался', callback_data='subscription')]
])

cancel_button = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text='✅ Отмена', callback_data='cancel')]
])
