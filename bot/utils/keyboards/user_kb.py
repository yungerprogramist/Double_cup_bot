from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardRemove
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.DataBase.categories_db import CategoriesDB
from bot.DataBase.offer_db import OfferDB

main_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Главное меню', callback_data='main_menu')]])


choise_action = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Прайс лист', callback_data='service_list')],
    [InlineKeyboardButton(text='Связаться', callback_data='contact_admin')]
    ])



def categories_list():
    builder = InlineKeyboardBuilder()
    for name in CategoriesDB().get_categories_list():
        builder.button(text= f"{name}", callback_data= f'services:{name}')
    builder.adjust(1)
    return builder.as_markup()


def services_list(category_id):
    builder = InlineKeyboardBuilder()
    for name in OfferDB().get_services_for_category(category_id=category_id):
        builder.button(text= f"{name}", callback_data= f'service_name:{name}')
    builder.adjust(1)
    return builder.as_markup()