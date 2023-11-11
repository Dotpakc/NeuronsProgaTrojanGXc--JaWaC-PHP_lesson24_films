import os
import asyncio
import json

from random import choice, randint
from decouple import config

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder


API_TOKEN = config('TELEGRAM_API_TOKEN')
ADMIN_ID = config('TELEGRAM_ADMIN_ID')

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# 1. 🆓Безкоштовні фільми
# 2. 🎞️Платні фільми  🗄️Серіали
# 3. 📺Телеканали  🎧Музика
# 4. 🧾Профіль

mainmenu = InlineKeyboardBuilder()
mainmenu.row(types.InlineKeyboardButton(text="🆓Безкоштовні фільми", callback_data="free_films"))
mainmenu.row(types.InlineKeyboardButton(text="🎞️Платні фільми", callback_data="pay_films"), types.InlineKeyboardButton(text="🗄️Серіали", callback_data="serials"))
mainmenu.row(types.InlineKeyboardButton(text="📺Телеканали", callback_data="tv"), types.InlineKeyboardButton(text="🎧Музика", callback_data="music"))
mainmenu.row(types.InlineKeyboardButton(text="🧾Профіль", callback_data="profile"))



def open_db():
    with open('films.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def gen_button_film_list(number_film, films):
    markup = InlineKeyboardBuilder()
    length_films = len(films)
    
    if number_film == 0:
        markup.row(
            types.InlineKeyboardButton(text="🔚Кінець", callback_data=f'film_list_{length_films-1}'), # 'film_list_2'
            types.InlineKeyboardButton(text=f"{number_film+1}/{length_films}", callback_data="none"),
            types.InlineKeyboardButton(text="⏭️Наступний", callback_data=f"film_list_{number_film+1}")
            )
    elif number_film == length_films-1:
        markup.row(
            types.InlineKeyboardButton(text="⏮️Назад", callback_data=f"film_list_{number_film-1}"),
            types.InlineKeyboardButton(text=f"{number_film+1}/{length_films}", callback_data="none"),
            types.InlineKeyboardButton(text="🔚Початок", callback_data="film_list_0")
            )
    else:
        markup.row(
            types.InlineKeyboardButton(text="⏮️Назад", callback_data=f"film_list_{number_film-1}"),
            types.InlineKeyboardButton(text=f"{number_film+1}/{length_films}", callback_data="none"),
            types.InlineKeyboardButton(text="⏭️Наступний", callback_data=f"film_list_{number_film+1}")
            )
    return markup


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Вітаю, я бот для пошуку фільмів на megogo.net", reply_markup=mainmenu.as_markup())

@dp.callback_query(F.data == "free_films")
async def free_films(call: types.CallbackQuery):
    films = open_db()
    film = films[0]
    
    photo = film['image_url']
    text = f"<b>{film['title']}</b>\n<i>{film['year']}</i>\n<i>{film['country']}</i>\n\n{film['discription']}"
    
    markup = gen_button_film_list(0, films)
    markup.row(types.InlineKeyboardButton(text="🎞️Переглянути фільм", url=film['video_url']))
    markup.row(types.InlineKeyboardButton(text="🔙Головне Меню", callback_data="mainmenu"))
    
    
    await call.message.answer_photo(photo, text, reply_markup=markup.as_markup())
    await call.message.delete()

@dp.callback_query(F.data.startswith("film_list_"))
async def next_film(call: types.CallbackQuery):
    call.message.delete_reply_markup()
    films = open_db()
    number_film = int(call.data.split("_")[-1])
    print(number_film)
    try:
        film = films[number_film]
    except IndexError:
        call.message.answer("Такого фільму не існує")
        try:
            await call.message.delete()
        except:
            pass

    
    photo = film['image_url']
    text = f"<b>{film['title']}</b>\n<i>{film['year']}</i>\n<i>{film['country']}</i>\n\n{film['discription']}"
    
    markup = gen_button_film_list(number_film, films)
    markup.row(types.InlineKeyboardButton(text="🎞️Переглянути фільм", url=film['video_url']))
    markup.row(types.InlineKeyboardButton(text="🔙Головне Меню", callback_data="mainmenu"))
    await call.message.answer_photo(photo, text, reply_markup=markup.as_markup())
    try:
        await call.message.delete()
    except:
        pass
    
@dp.callback_query(F.data == "mainmenu")
async def mainmenu1(call: types.CallbackQuery):
    await call.message.answer("Головне меню", reply_markup=mainmenu.as_markup())
    try:
        await call.message.delete()
    except:
        pass

async def main():
    print("Start....")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())