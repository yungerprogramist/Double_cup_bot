from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardRemove
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


from bot.DataBase.categories_db import CategoriesDB
from bot.DataBase.offer_db import OfferDB
from bot.DataBase.message_db import MessagesDB


menu_admin =  InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Вернуться в меню', callback_data='admin_panel')]])

admin_panel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить услугу', callback_data='add_service')],
    [InlineKeyboardButton(text='Удалить услугу', callback_data='delete_service')],
    [InlineKeyboardButton(text='Добавить категорию', callback_data='add_category')],
    [InlineKeyboardButton(text='Удалить категорию', callback_data='delete_category')],
    [InlineKeyboardButton(text='Сообщения в боте', callback_data='change_message')],

    ])


# добавление услуги
def categories_list_add():
    builder = InlineKeyboardBuilder()
    for name in CategoriesDB().get_categories_list():
        builder.button(text= f"{name}", callback_data= f'add_service:{name}')
    builder.adjust(1)
    return builder.as_markup()

# удаление книги выбор категории
def categories_list_delete():
    builder = InlineKeyboardBuilder()
    for name in CategoriesDB().get_categories_list():
        builder.button(text= f"{name}", callback_data= f'delete_service_cat:{name}')
    builder.adjust(1)
    return builder.as_markup()

# удаление книги - выбор книги для удаления
def service_list_delete(category_id):
    builder = InlineKeyboardBuilder()
    for name in OfferDB().get_services_for_category(category_id=category_id):
        builder.button(text= f"{name}", callback_data= f'delete_service_name:{name}')
    builder.adjust(1)
    return builder.as_markup()

# удаление категории
def categories_delete():
    builder = InlineKeyboardBuilder()
    for name in CategoriesDB().get_categories_list():
        builder.button(text= f"{name}", callback_data= f'delete_category:{name}')
    builder.adjust(1)
    return builder.as_markup()


# работа с сообщениями бота
def message_list():
    builder = InlineKeyboardBuilder()
    for name in MessagesDB().get_message_list():
        builder.button(text= f"{name[1][10:]}...", callback_data= f'message:{name[0]}')
    builder.adjust(1)
    return builder.as_markup()