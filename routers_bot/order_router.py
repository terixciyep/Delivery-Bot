import datetime
import json

from aiogram.methods import SendPhoto

from core.texts import cancel_text, order_ready_text
from id_bot import id
from aiogram import types
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from core.validators import phone_validator
from .order_router_FSM import MainStates
from core import texts
from db.cursor import cur, sq_con
from config import bot
order_router = Router()

@order_router.message(Command('cancel'))
async def cancel_operation(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await message.answer(cancel_text)
    else:
        await message.answer("Лучше введите /order и сделайте заказ")

@order_router.message(lambda message: message.text.lower() == 'сделать заказ' or message.text.lower()=='/order')
async def order_start(message: types.Message, state: FSMContext):
    await message.delete()
    categories = cur.execute("SELECT delivery_type, id FROM delivery_type").fetchall()
    categories = [[category[0],category[1]] for category in categories]
    now_row = []
    query_row = []
    for i in range(len(categories)):
        callback_data = json.dumps(categories[i][1])
        now_row.append(InlineKeyboardButton(text=categories[i][0], callback_data=callback_data))
        if len(now_row)%2==0:
            query_row.append(now_row)
            now_row = []
    query_row.append(now_row)
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[*query_row])
    await message.answer('Выберите категорию доставки! 👇🏼', reply_markup=inline_kb)
    a = await state.get_data()
    if a:
        await state.clear()
    await state.set_state(MainStates.first)
    a = await state.get_data()

@order_router.callback_query(MainStates.first)
async def store_order(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    a = await state.get_state()
    await state.update_data(main2='2')
    a = await state.get_data()
    selected_category = int(callback_query.data)
    await state.update_data(category = selected_category)
    stores = cur.execute("SELECT s.store, st.store_id  FROM store_with_category st LEFT JOIN store s ON s.id=st.store_id WHERE st.delivery_type = (?) ORDER BY s.store",(selected_category,))
    stores = [[store[0],store[1]] for store in stores]
    now_row = []
    query_row = []
    for i in range(len(stores)):
        callback_data = json.dumps(stores[i][1])
        now_row.append(InlineKeyboardButton(text=stores[i][0], callback_data=callback_data))
        if len(now_row)%3==0:
            query_row.append(now_row)
            now_row = []
    query_row.append(now_row)
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[*query_row])
    await callback_query.message.answer(f'Выбери место, из которого ты хочешь заказать доставку! 👇🏼', parse_mode='HTML', reply_markup=inline_kb)
    await state.set_state(MainStates.second)

@order_router.callback_query(MainStates.second)
async def description_order(callback_query: types.CallbackQuery, state: FSMContext):
    global button
    await callback_query.message.delete()
    await state.update_data(store=callback_query.data)
    data = await state.get_data()
    conditions = cur.execute("SELECT * FROM condition_delivery_type WHERE delivery_type = (?) ORDER BY id DESC",
                                (data['category'],))
    conditions = [[*condition] for condition in conditions]
    answers = {}
    await state.update_data(questions = conditions)
    await state.update_data(answers=answers)
    if len(conditions) > 0:
        button = await callback_query.message.answer(f"{conditions[0][2]}")
        await state.set_state(MainStates.second_switcher)
    else:
        button = await callback_query.message.answer(f"Напиши свое имя ✍🏻")
        await state.set_state(MainStates.third)


@order_router.message(MainStates.first_switcher)
async def question_order(message: types.Message, state: FSMContext):
    global button
    data = await state.get_data()
    await message.delete()
    await button.delete()
    button = await message.answer(f"{data['questions'][0][2]}")
    questions = data['questions'][1:]
    await state.update_data(questions=questions)
    await state.set_state(MainStates.second_switcher)

@order_router.message(MainStates.second_switcher)
async def question_order(message: types.Message, state: FSMContext):
    global button
    data = await state.get_data()
    questions = data['questions']
    answers = data['answers']
    if questions:
        current_question = questions.pop(0)
        answers[current_question[0]] = message.text
        await state.update_data(answers=answers)
        await state.update_data(questions=questions)
        if questions:
            button = await message.answer(f"{questions[0][2]}")
            await state.set_state(MainStates.second_switcher)
        else:
            await button.delete()
            await message.delete()
            button = await message.answer(f"Напиши свои имя и фамилию ✍🏻")
            await state.set_state(MainStates.third)




@order_router.message(MainStates.third)
async def last_name_order(message: types.Message, state: FSMContext):
    global button
    await state.update_data(name = message.text)
    await button.delete()
    await message.delete()
    button = await message.answer('Укажи свой номер телефона для связи📲', parse_mode='HTML')
    await state.set_state(MainStates.fourth)


@order_router.message(MainStates.fourth)
async def full_order(message: types.Message, state: FSMContext):
    global button
    if phone_validator(message.text):
        await button.delete()
        await state.update_data(phone=message.text)
        community = cur.execute('SELECT id, name FROM community')
        community = [[com[0], com[1]] for com in community]
        now_row = []
        query_row = []
        for i in range(len(community)):
            callback_data = json.dumps(community[i][0])
            now_row.append(InlineKeyboardButton(text=community[i][1], callback_data=callback_data))
            if len(now_row) % 2 == 0:
                query_row.append(now_row)
                now_row = []
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[*query_row])
        button = await message.answer(f'Укажи номер общежития 🏠', reply_markup=inline_kb)
        await state.set_state(MainStates.fifth)
        await message.delete()
    else:
        await button.delete()
        await message.delete()
        button = await message.answer('Вы ввели неправильный номер телефона, введите начиная с +7/7/8')
        await state.set_state(MainStates.fourth)


@order_router.callback_query(MainStates.fifth)
async def number_order(callback_query: types.CallbackQuery, state: FSMContext):
    global button
    await button.delete()
    community_id = callback_query.data
    await state.update_data(community_id=community_id)
    button = await callback_query.message.answer('Укажи номер блока 🚪')
    await state.set_state(MainStates.sixth)

@order_router.message(MainStates.sixth)
async def promo_order(message: types.Message, state: FSMContext):
    global button
    await state.update_data(block=message.text)
    await message.delete()
    await button.delete()
    button = await message.answer('Введи промокод (если нет, поставь - )')
    await state.set_state(MainStates.seven)

@order_router.message(MainStates.seven)
async def number_order(message: types.Message, state: FSMContext):
    global button
    await button.delete()
    data = await state.get_data()
    name = data['name']
    phone_number = data['phone']
    telegram_link_on_user = f"@{message.from_user.username}"
    type_of_delivery = data['category']
    store_id = data['store']
    community_id = data['community_id']
    block = data['block']
    await message.delete()
    cur.execute(
            "INSERT INTO orders(name,phone_number, telegram_link_on_user, community_id,type_of_delivery, store_id) VALUES (?,?,?,?,?,?)",
            (name, phone_number, telegram_link_on_user, community_id, type_of_delivery, store_id))
    order_id = cur.lastrowid
    sq_con.commit()
    for key, value in data['answers'].items():
        cur.execute("INSERT INTO users_condition_orders(order_id,condition_id, answer) VALUES (?,?,?)",
                    (order_id, key, value))
    sq_con.commit()
    await state.clear()
    order = cur.execute(
        "SELECT o.name, o.phone_number, o.telegram_link_on_user, dt.delivery_type, community.name, store.store FROM orders o LEFT JOIN delivery_type dt ON dt.id = o.type_of_delivery LEFT JOIN community ON community.id=o.community_id LEFT JOIN store ON store.id=o.store_id WHERE o.id = (?)",
        (order_id,)).fetchall()[0]
    answers = cur.execute("SELECT uco.answer,cdt.condition_name FROM users_condition_orders uco LEFT JOIN condition_delivery_type cdt ON uco.condition_id=cdt.id WHERE uco.order_id=(?)", (order_id,)).fetchall()
    text = f"Имя:{order[0]}\n" \
           f"Телефон: {order[1]} \n" \
           f"Телеграм ссылка: {order[2]} \n" \
           f"Тип доставки: {order[3]} \n" \
           f"Место доставки: {order[4]} \n" \
           f"Блок: {block} \n" \
           f"Магазин доставки: {order[5]} \n" \

    for ans in answers:
        text+=f"{ans[1]}: {ans[0]} \n"
    text+=f"Промокод: {message.text} \n"
    await bot.send_message(chat_id=1252861265, text=text)
    return SendPhoto(photo='https://github.com/terixciyep/photos/blob/main/order_ready.jpg?raw=true', caption=texts.order_ready_text, chat_id=message.from_user.id)


