import asyncio
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes
from dotenv import load_dotenv
from keyboard import *
from keyboard_admin import *

load_dotenv()
tg_token = os.getenv('TG_BOT_TOKEN')
admintg_id = os.getenv('ADMIN_ID')
bot = Bot(token=tg_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class D(StatesGroup):
    contact = State()
    accept = State()


async def on_startup(_):
    pass


@dp.callback_query_handler(text=['admin', 'user'])
async def get_role(call: types.CallbackQuery):
    if call.data == 'user':
        user = call.message.from_user.username
        await call.message.answer(f'Добро пожаловать, {user}! Выберите интересующий вас раздел:', reply_markup=kb1())
    elif call.data == 'admin':
        await call.message.answer('Вы вошли в режим админа. Выберите интересующий вас раздел:', reply_markup=kb_admin_1())


@dp.callback_query_handler(text=['no_time', 'active', 'ad', 'full_boxes'])
async def admin_pannel(call: types.CallbackQuery):
    if call.data == 'no_time':
        await call.message.answer('Просроченные боксы:', reply_markup=kb_admin_2())
    elif call.data == 'active':
        await call.message.answer('Активные заказы:', reply_markup=kb_admin_3())
    elif call.data == 'ad':
        await call.message.answer('Активные рекламные интеграции:')
    elif call.data == 'full_boxes':
        await call.message.answer('Занятые боксы:', reply_markup=kb_admin_4())


@dp.callback_query_handler(text='take_order')
async def accept_orders_w(call: types.CallbackQuery):
    await call.message.answer('Выберите вес вещей:', reply_markup=choose_weight_adm())


@dp.callback_query_handler(text=['10', '10-20', '4-7', '7-10', '100'])
async def accept_orders_h(call: types.CallbackQuery):
    await call.message.answer('Выберите высоту вещей', reply_markup=choose_height_adm())


@dp.callback_query_handler(text=['less_3', '3-7', '7-10'])
async def accept_order(call: types.CallbackQuery):
    await call.message.answer('Подтвердите выполнение заказа:', reply_markup=accept_orde())
    await D.accept.set()


@dp.callback_query_handler(state=D.accept)
async def adm_finish(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Заказ успешно подтвержден.', reply_markup=kb_admin_1())
    await state.finish()


@dp.callback_query_handler(text='adm_menu')
async def back_to_adm_menu(call: types.CallbackQuery):
    await call.message.answer('Вы вернулись в меню', reply_markup=kb_admin_1())


@dp.callback_query_handler(text='storage_list')
async def u_send_good_list(call: types.CallbackQuery):
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
async def u_to_support(call: types.CallbackQuery):
    await call.message.answer('Выберите опцию:', reply_markup=kb2())


@dp.callback_query_handler(text='faq')
async def u_send_faq(call: types.CallbackQuery):
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


@dp.callback_query_handler(text='my_boxes')
async def u_get_user_boxes(call: types.CallbackQuery):
    await call.message.answer('Выберите подходящую опцию из меню ниже:', reply_markup=boxes_main())


@dp.callback_query_handler(text=['box1', 'furniture'])
async def u_get_boxes_back(call: types.CallbackQuery):
    await call.message.answer('Выберите подходящую опцию:', reply_markup=boxes2())


@dp.callback_query_handler(text=['get_back_main', 'get_back'])
async def u_get_boxes_back(call: types.CallbackQuery):
    if call.data == 'get_back_main':
        await call.message.answer('Отлично! Выберите удобный для вас способ доставки:', reply_markup=kb3())
    elif call.data == 'get_back':
        await call.message.answer('Выберите бокс, из которого вы хотите забрать вещи:', reply_markup=boxes_main())


@dp.callback_query_handler(text='back_to_menu')
async def u_back_to_menu(call: types.CallbackQuery):
    await call.message.answer(text='Вы вернулись обратно в меню', reply_markup=kb1())


@dp.callback_query_handler(text='application')
async def u_leave_a_request(call: types.CallbackQuery):
    await call.message.answer('Подтвердите согласие на обработку персональных данных', reply_markup=data_processing())


@dp.callback_query_handler(text=['runner', 'myself', 'by_runner', 'by_myself'])
async def u_delivery(call: types.CallbackQuery):
    if call.data == 'runner':
        await call.message.answer("""Вы выбрали курьерскую доставку! 
Наши муверы приедут к вам по указанному адресу, измерят (если это необходимо) и упакуют ваши вещи.
Муверы приедут по указанному адресу, чтобы измерить, упаковать и забрать ваши вещи на склад""", kb7())
    elif call.data == 'myself':
        await call.message.answer('Отлично! Ждем вас по адресу: Юбилейный проспект, 17к1', reply_markup=kb7())
    elif call.data == 'by_runner':
        await call.message.answer("""Курьер приедет в течение 20 минут.
Чтобы подтвердить заказ, покажите курьеру этот QR-код.""", reply_markup=back())
    elif call.data == 'by_myself':
        await call.message.answer("""Отлично! Можете забрать свои вещи по адресу: Юбилейный проспект, 17к1
QR-код для получения:""", reply_markup=back())


@dp.callback_query_handler(text=['ten', 'ten_twenty', '40_70', '70-100', 'more100', 'idk'])
async def u_choose_w(call: types.CallbackQuery):
    if call.data == 'idk':
        await call.message.answer("""Конечно! Мы поможем вам рассчитать вес ваших вещей.
Выберите высоту ваших вещей, если она известна. Мы также можем помочь вам с рассчетом!""", reply_markup=choose_height())
    else:
        await call.message.answer('Теперь укажите высоту ваших вещей:', reply_markup=choose_height())


@dp.callback_query_handler(text='idkh')
async def u_help_w_height(call: types.CallbackQuery):
    await call.message.answer("Конечно, мы поможем вам рассчитать высоту ваших вещей. Выберите удобный способ доставки:",
                              reply_markup=choose_del())


@dp.callback_query_handler(text=['less3', '3-7m', '7-10m'])
async def u_choose_h(call: types.CallbackQuery):
    await call.message.answer('Оставьте комментарий к заказу и выберите нужную опцию: 👇', reply_markup=choose_del())


@dp.callback_query_handler(text='letter_to_sup')
async def u_send_letter_to_sup(call: types.CallbackQuery):
    await call.message.answer("""Данные для обращения в поддержку:
storagebot@gmail.com
+79215897941""")
    await asyncio.sleep(1)
    await call.message.answer('Для продолжения воспользуйтесь кнопками из меню ниже 👇:', reply_markup=kb6())


@dp.callback_query_handler(text=['yes', 'no'])
async def u_person_data_processing(call: types.CallbackQuery):
    if call.data == 'yes':
        await D.contact.set()
        await call.message.answer('Для продолжения отправьте свой номер телефона, используя кнопку ниже',
                                  reply_markup=contact())
        await asyncio.sleep(1)
        await call.message.answer('Введите ваш адрес в формате: ул. Южная, д. 13, кв. 7')
    if call.data == 'no':
        await call.message.answer('Выберите подходящую опцию из меню ниже 👇:', reply_markup=kb2())


@dp.message_handler(state=D.contact)
async def u_make_application(msg: types.Message, state: FSMContext, content_types=ContentTypes.CONTACT):
    await state.get_data()
    await state.update_data(address=msg.text)
    await msg.answer('Ваши контактные данные получены.\nВыберите вес ваших вещей 👇:',
                     reply_markup=choose_weight())
    await state.finish()


@dp.message_handler(commands=['start'])
async def u_start(msg: types.Message):
    text = """Добро пожаловать! 
Мы компания, предоставляющая малогабаритные ячейки для сезонного хранения вещей.
Например велосипеды, каяки, cнегоходы. 
Мы заберём ваши вещи на наш склад, сохраним и привезём обратно в любую точку Москвы.
Для выбора роли воспользуйтесь кнопками из меню ниже 👇
        """
    await msg.answer(text, reply_markup=choose_role())


if '__main__' == __name__:
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
