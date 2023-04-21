import asyncio
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes
from dotenv import load_dotenv
from keyboard import *

load_dotenv()
tg_token = os.getenv('TG_BOT_TOKEN')
bot = Bot(token=tg_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class D(StatesGroup):
    contact = State()
    make_order = State()


async def on_startup(_):
    pass


@dp.callback_query_handler(text='storage_list')
async def send_good_list(call: types.CallbackQuery):
    good_list = """Что принимается на хранение:                                                                                                                              
✅ Мебель                             
✅ Бытовая техника                 
✅ Одежда и обувь                      
✅ Инструменты
✅ Посуда
✅ Книги
✅ Шины
✅ Велосипеды
✅ Мотоциклы и скутеры
✅ Спортивный инвентарь
Что не принимается на хранение:
❌ Алкоголь
❌ Продукты
❌ Деньги и драгоценности
❌ Изделия из натурального меха
❌ Живые цветы и растения
❌ Домашние питомцы
❌ Оружие и боеприпасы
❌ Взрывоопасные вещества и токсины
❌ Лаки и краски в негерметичной таре
❌ Любой мусор и отходы
    """
    await call.message.answer(good_list, reply_markup=kb6())


@dp.callback_query_handler(text='support')
async def to_support(call: types.CallbackQuery):
    await call.message.answer('Выберите опцию:', reply_markup=kb2())


@dp.callback_query_handler(text='faq')
async def send_faq(call: types.CallbackQuery):
    faq = """
1. Оформите заявку, используя бота.
2. Мы рассчитаем подходящий тариф, исходя из объема вещей.
3. В удобное время к вам приедет команда муверов, упакует вещи, вынесет и отвезёт их на склад или на ваше новое место жительства.
4. Когда какая-то вещь снова понадобится, закажите возврат, и мы привезем её в любую точку Москвы.
5. Наша система не предусматривает дополнительных платежей за неиспользованное пространство. Это означает, \
что вы платите только за тот объем пространства, который фактически занимают ваши вещи, а не за весь объем комнаты для хранения.
6. Мы предлагаем услугу мобильного хранения, которая включает доставку наших профессиональных упаковочных материалов. \
Наша команда муверов соберет, упакует и маркирует все ваши вещи, а затем транспортирует их на наш склад. \
Все вещи хранятся на отдельных паллетах в надежных условиях. \
Наш склад постоянно контролируется видеокамерами без слепых зон, и круглосуточно охраняется.
7. Вы можете контролировать свои вещи через специальное меню нашего бота. \
Там вы можете заказать возврат вещей в любое удобное для вас время или добавить новые вещи для хранения. \
Все ваши вещи всегда находятся в безопасности и готовы к использованию.
    """
    await call.message.answer(faq, reply_markup=kb5())


@dp.callback_query_handler(text='back_to_menu')
async def back_to_menu(call: types.CallbackQuery):
    await call.message.answer(text='Вы вернулись обратно в меню', reply_markup=kb1())


@dp.callback_query_handler(text='application')
async def leave_a_request(call: types.CallbackQuery):
    await call.message.answer('Подтвердите согласие на обработку персональных данных', reply_markup=data_processing())


@dp.callback_query_handler(text=['runner', 'myself'])
async def delivery(call: types.CallbackQuery):
    if call.data == 'runner':
        await call.message.answer("""Вы выбрали курьерскую доставку! 
Наши муверы приедут к вам по указанному адресу, измерят (если это необходимо) и упакуют ваши вещи.""",
                                  reply_markup=choose_weight())
    elif call.data == 'myself':
        await call.message.answer('Ждем вас по адресу: Юбилейный проспект, 17к1', reply_markup=choose_weight())


@dp.callback_query_handler(text=['ten', 'ten_twenty', '40_70', '70-100', 'more100', 'idk'])
async def choose_w(call: types.CallbackQuery):
    if call.data == 'idk':
        await call.message.answer("""Конечно! Мы поможем вам рассчитать вес и высоту ваших вещей. 
Вы можете привезти вещи сами или мы пришлем к вам команду муверов, чтобы рассчитать рост и вес на месте.""",
                                  reply_markup=choose_del2())
    else:
        await call.message.answer('Теперь укажите высоту ваших вещей:', reply_markup=choose_height())


@dp.callback_query_handler(text='idkmyself')
async def del_by_myself(call: types.CallbackQuery):
    await call.message.answer('Ждем вас по адресу: Юбилейный проспект, 17к1', reply_markup=kb2())


@dp.callback_query_handler(text='idkrunners')
async def callrunners(call: types.CallbackQuery):
    await call.message.answer(
        'Муверы приедут по указанному адресу, чтобы измерить, упаковать и забрать ваши вещи на склад')
    await asyncio.sleep(1)
    await call.message.answer('Для продолжения воспользуйтесь кнопками из меню ниже 👇:', reply_markup=kb1())


@dp.callback_query_handler(text='letter_to_sup')
async def send_letter_to_sup(call: types.CallbackQuery):
    await call.message.answer("""Данные для обращения в поддержку:
storagebot@gmail.com
+79215897941""")
    await asyncio.sleep(1)
    await call.message.answer('Для продолжения воспользуйтесь кнопками из меню ниже 👇:', reply_markup=kb6())


@dp.callback_query_handler(text=['yes', 'no'])
async def person_data_processing(call: types.CallbackQuery):
    if call.data == 'yes':
        await D.contact.set()
        await call.message.answer('Для продолжения отправьте свой номер телефона, используя кнопку ниже', reply_markup=contact())
        await asyncio.sleep(1)
        await call.message.answer('Введите ваш адрес в формате: ул. Южная, д. 13, кв. 7')
    if call.data == 'no':
        await call.message.answer('Выберите подходящую опцию из меню ниже:', reply_markup=kb2())


@dp.message_handler(state=D.contact)
async def make_application(msg: types.Message, state: FSMContext, content_types=ContentTypes.CONTACT):
    await msg.answer('Ваши контактные данные получены.\nВыберите подходящую опцию из меню ниже 👇:',
                     reply_markup=choose_del())
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    text = """Добро пожаловать! 
Мы компания, предоставляющая малогабаритные ячейки для сезонного хранения вещей.
Например велосипеды, каяки, cнегоходы. 
Мы заберём ваши вещи на наш склад, сохраним и привезём обратно в любую точку Москвы.
Для выбора интересующего вас раздела воспользуйтесь кнопками из меню ниже 👇
        """
    await msg.answer(text, reply_markup=kb1())


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
