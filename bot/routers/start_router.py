from aiogram import Router

from aiogram import  F, Bot
from aiogram.types import Message

from bot.DataBase.user_db import UserDB

from bot.utils.keyboards import user_kb as kb
from bot.DataBase.message_db import MessagesDB


router = Router()


@router.message(F.text == '/start')
async def start(message:Message, bot: Bot):

    username = message.from_user.username
    chat_id = message.from_user.id

    if username is not None:
        UserDB().start_db(username, chat_id)

        text, photo = MessagesDB().get_message('start')
        await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=text, reply_markup=kb.main_menu)

    else: 
        await message.answer('Для использования этого бота, установите username')