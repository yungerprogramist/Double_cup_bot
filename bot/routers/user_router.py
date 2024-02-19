from aiogram import Router

from aiogram import  F, Bot
from aiogram.types import Message, CallbackQuery 
from aiogram.fsm.context import FSMContext

from bot.utils.keyboards import user_kb as kb
from bot.DataBase.categories_db import CategoriesDB
from bot.DataBase.offer_db import OfferDB
from bot.utils.FSMclasses import AskQuestion

from dotenv import load_dotenv
import os
load_dotenv()
ADMINS= os.getenv('ADMINS').split(' ')


router = Router()

@router.callback_query(F.data == 'main_menu')
async def main_menu(call: CallbackQuery):
    await call.message.answer(text='Выберите что дальше', reply_markup=kb.choise_action)




"""===========================Просмотр услуг=============================="""

@router.callback_query(F.data == 'service_list')
async def prise_list(call: CallbackQuery):
    await call.message.answer(text='Выберите категорию', reply_markup=kb.categories_list())


@router.callback_query(lambda call: 'services:' in call.data )
async def services_list(call: CallbackQuery):
    category = call.data.split(':')[1]
    category_id = CategoriesDB().get_id_category(category)

    await call.message.answer(text='Перечень услуг', reply_markup=kb.services_list(category_id))


@router.callback_query(lambda call: 'services_name:' in call.data )
async def services_name(call: CallbackQuery, bot: Bot):
    name = call.data.split(':')[1]

    data = OfferDB().get_info_service(name)
    description = data[1]
    photo_file = data[3]

    if photo_file == 'None': await call.message.answer(text=description, reply_markup=kb.choise_action)

    else: await bot.send_photo(chat_id=call.from_user.id, caption=description, photo=photo_file, reply_markup=kb.choise_action)


"""===========================задать вопрос=============================="""

@router.callback_query(F.data == 'contact_admin')
async def ask_question(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='Введите вопрос и отправьте его', reply_markup=kb.main_menu)
    await state.set_state(AskQuestion.text)

@router.message(AskQuestion.text)
async def ask_question_send(message: Message, state: FSMContext, bot: Bot):
    await state.clear()

    text = f'Вам пришел вопрос от @{message.from_user.username} \n {message.text}'
    for admin in ADMINS:
        await bot.send_message(chat_id=int(admin), text=text)
    
    await message.answer(text='Ваш вопрос успешно отправлен администратору, дожидайтесь ответа', reply_markup=kb.main_menu)


