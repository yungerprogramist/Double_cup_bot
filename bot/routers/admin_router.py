from aiogram import Router

from aiogram import  F, Bot
from aiogram.types import Message, CallbackQuery 
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv
import os

from bot.utils.keyboards import admin_kb as kb
from bot.utils.FSMclasses import AddService, AddCategory, ChangeMessage
from bot.DataBase.categories_db import CategoriesDB
from bot.DataBase.offer_db import OfferDB
from bot.DataBase.message_db import MessagesDB

router = Router()



load_dotenv()
CHANEL_DATA_BASE = '@Double_Cup_agBot'
ADMINS= os.getenv('ADMINS').split(' ')


@router.message(F.text == '/admin')
async def admin_panel_mes(message: Message, state: FSMContext):
    await state.clear()
    if str(message.from_user.id) in ADMINS:
        await message.answer(f'Добро пожаловать администратор {message.from_user.username}', reply_markup=kb.admin_panel_keyboard) 

@router.callback_query(F.data == 'admin_panel')
async def admin_panel_call(call: CallbackQuery, state: FSMContext):
    await state.clear()
    # if str(message.from_user.id) in ADMINS:
    await call.message.answer(f'Добро пожаловать администратор {call.from_user.username}', reply_markup=kb.admin_panel_keyboard) 



"""=====================================добавление услуги============================="""

@router.callback_query(F.data == 'add_service')
async def add_tales(call: CallbackQuery):
    await call.message.answer(text='Выберите категорию, в которую хотите добавить контент', reply_markup=kb.categories_list_add())


@router.callback_query(lambda call: 'add_service:' in call.data )
async def service_add_category(call: CallbackQuery, state: FSMContext):
    category = call.data.split(':')[1]
    await call.message.answer(f'Введите название для добавляемого контента (не более 35 символов) \nКатегория - {category}')

    category_id = CategoriesDB().get_id_category(category=category)
    await state.update_data(category_id=category_id)
    await state.set_state(AddService.name)

@router.message(AddService.name)
async def service_add_name(message: Message, state: FSMContext):
    if len(message.text) < 35: 
        await message.answer(text='Введите описание для книги')
    
        await state.update_data(name=message.text)
        await state.set_state(AddService.description)
    else:
        await state.set_state(AddService.name)
        await message.answer(f'Название должно содержать не более 35 символов! \nОтправьте его еще раз')


@router.message(AddService.description)
async def servise_add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.answer(text='Отправьте фотографию, если она не нужна введите "готово"')
    await state.set_data(AddService.photo)


@router.message(AddService.description)
async def servise_add_photo(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    if message.text.lower().strip() == 'готово':
        if OfferDB().add_service(category_id=data['category_id'], name=data['name'], description=data['description']):
            await message.answer(text='добавление завершено', reply_markup=kb.menu_admin)
        else:
            await message.answer(text='Что то пошло не так', reply_markup=kb.menu_admin)

    else: 
        if message.photo: 
            file = message.photo[-1].file_id
            await bot.copy_message(chat_id=CHANEL_DATA_BASE, from_chat_id=message.from_user.id, message_id=file)
            OfferDB().add_service(category_id=data['category_id'], name=data['name'], description=data['description'], photo=file)
        else: 
            await message.answer(text='Что то пошло не так, пришлите именно фото', reply_markup=kb.menu_admin)




"""=====================================удаление услуги============================="""

@router.callback_query(F.data == 'delete_service')
async def delete_tales(call: CallbackQuery):
    await call.message.answer(text='Выберите категорию для удаления контента', reply_markup=kb.categories_list_delete())

    
@router.callback_query(lambda call: 'delete_service_cat:' in call.data )
async def delete_service_category(call: CallbackQuery):
    category = call.data.split(':')[1]
    category_id = CategoriesDB().get_id_category(category)
    await call.message.answer(text='Выберите книгу, которую желаете удалить', reply_markup=kb.service_list_delete(category_id))

@router.callback_query(lambda call: 'delete_service_name:' in call.data )
async def delete_service_name(call: CallbackQuery):
    name = call.data.split(':')[1]

    if OfferDB().delete_servise(name):
        await call.message.answer(text=f'услуга {name} успешно удалена', reply_markup=kb.menu_admin)
    else:
        await call.message.answer(text=f'Что то пошло не так во время удаления услуги {name}', reply_markup=kb.menu_admin)



"""=====================================Добавление категории============================="""
@router.callback_query(F.data == 'add_category')
async def add_category(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='Введите название новой категории. Название должно содержать не более 35 символов!', reply_markup=kb.menu_admin)
    await state.set_state(AddCategory.name)

@router.message(AddCategory.name)
async def add_category_name(message: Message, state: FSMContext):
    if len(message.text) < 35: 
        if CategoriesDB().add_category(message.text):
            await message.answer(text=f'Категория {message.text} успешно добавлена', reply_markup=kb.menu_admin)
            await state.clear()

        else:
            await state.clear()
            await message.answer(text='Что то пошло не так во время добавления в бд', reply_markup=kb.menu_admin)

    else:
        await state.set_state(AddCategory.name)
        await message.answer(f'Название должно содержать не более 35 символов! \nОтправьте его еще раз', reply_markup=kb.menu_admin)



"""=====================================Удаление категории============================="""
@router.callback_query(F.data == 'delete_category')
async def delete_category(call: CallbackQuery):
    await call.message.answer(text='Выберите категорию, которую желаете удалить', reply_markup=kb.categories_delete())

    
@router.callback_query(lambda call: 'delete_category:' in call.data )
async def delete_service_category(callback: CallbackQuery):
    category = callback.data.split(':')[1]
    if CategoriesDB().dell_category(category):
        await callback.message.answer(text=f'Категория {category} успешно удалена', reply_markup=kb.menu_admin)

    else:
        await callback.message.answer(text='Что то пошло не так', reply_markup=kb.menu_admin)



"""=====================================Работа с сообщениями============================="""
@router.callback_query(F.data == 'change_message')
async def change_message(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(text='Выберите сообщение для коректировки', reply_markup=kb.message_list())


@router.callback_query(lambda call: 'message:' in call.data )
async def input_message(call: CallbackQuery, state: FSMContext):
    mes = MessagesDB().get_message_for_name(call.data.split(':')[1])
    await call.message.answer(text=f'текущее сообщение \n{mes[0]}')
    await call.message.answer(text='Ввведите новое сообщение для этой записи или скопируйте и вставьте текущее', reply_markup=kb.menu_admin)

    await state.update_data(name = call.data.split(':')[1])
    await state.set_data(ChangeMessage.text)


@router.message(ChangeMessage.text)
async def input_photo(message: Message, state: FSMContext):
    await state.update_data(text = message.text)
    await message.answer(text='Текст принят, теперь пришлите мне новую фотографию, если желаете оставить предыдущую введите "готово"')

    await state.set_data(ChangeMessage.photo)

@router.message(ChangeMessage.photo)
async def change_message(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    name = data['name']
    text = data['text']

    if message.text.lower().strip() == 'готово':
        MessagesDB().change_text_message(name=name, text=text)

    else: 
        if message.photo: 
            file = message.photo[-1].file_id
            await bot.copy_message(chat_id=CHANEL_DATA_BASE, from_chat_id=message.from_user.id, message_id=file)
            MessagesDB().change_photo_message(name=name, photo=file)
        else: 
            await message.answer(text='Что то пошло не так, пришлите именно фото', reply_markup=kb.menu_admin)

