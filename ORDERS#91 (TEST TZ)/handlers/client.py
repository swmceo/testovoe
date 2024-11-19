from aiogram import types
from main import dp
from main import bot
from function import user_func as usfn
import requests
import asyncio
 
@dp.message_handler(commands=['start'])
async def start_handler_bot(message: types.Message):
    connect = await usfn.create_connection()
    check_user = await usfn.get_user(connect, message.from_user.id)
    if check_user == None:
        await usfn.add_user(connect, message.from_user.id, message.from_user.username)
    else:
        pass
    await bot.send_message(message.from_user.id, """Привет! Я бот для отслеживания балансов кошельков TON. С помощью меня ты можешь добавлять кошельки для мониторинга и получать уведомления при изменении их балансов.
<a href="https://gist.github.com/s0urce-c0d3/eb9d476c94610b3cd037023916de2fa1">Бот с уведами от TON</a>""", parse_mode='HTML')
    await bot.send_message(message.from_user.id, 'Если возникли вопросы по кномандам - /help', parse_mode='HTML')

@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await bot.send_message(message.from_user.id, """Команды:
/add_wallet <code> адрес </code> - добавить кошелёк для отслеживания
/remove_wallet <code> адрес </code> - удалить кошелёк из списка отслеживаемых
/list_wallets - показать все отслеживаемые кошельки
/check_balance <code> адрес </code> - проверить баланс кошелька
/help - помощь по командам""")

@dp.message_handler(commands=['add_wallet'])
async def add_wallet_handler(message: types.Message):
    # try:
        address = message.text.split(' ')[1]
        check_wallet = requests.get(f'https://toncenter.com/api/v2/getAddressInformation?address={address}')
        if check_wallet.json()["ok"] == True:
            connect = await usfn.create_connection()
            uniqueness_check = await usfn.get_wallet(connect, address, message.from_user.id)
            if uniqueness_check == None:
                await usfn.add_wallet(connect, address, message.from_user.id, check_wallet.json()['result']['balance'])
                await bot.send_message(message.from_user.id, f"""Успешно! <code>{address}</code> <b>Добавлен</b>""", parse_mode='HTML')
                await check_wallet_changes(message)
            else:
                await bot.send_message(message.from_user.id, """Вы уже привязали этот кошелек""")
        if check_wallet.json()["ok"] == False:
            await bot.send_message(message.from_user.id, """Некорректный адрес""")
    # except:
        await bot.send_message(message.from_user.id, """Некорректный адрес""")

@dp.message_handler(commands=['list_wallets'])
async def list_wallet_handler(message: types.Message):
    try:
        connect = await usfn.create_connection()
        wallet_list = await usfn.get_all_wallets_user(connect, message.from_user.id)
        output = ''
        for i in wallet_list:
            output += f'<code>{i[0]}</code>\n\n'
        await bot.send_message(message.from_user.id, output, parse_mode='HTML')
    except:
        await bot.send_message(message.from_user.id, 'У вас нет кошельков', parse_mode='HTML')
    
@dp.message_handler(commands=['check_balance'])
async def check_balance_handler_bot(message: types.Message):
    try:
        address = message.text.split(' ')[1]
        check_wallet = requests.get(f'https://toncenter.com/api/v2/getAddressInformation?address={address}')
        if check_wallet.json()["ok"] == True:
            await bot.send_message(message.from_user.id, f"""Баланс кошелька <code>{address}</code>\n<b>Составляет: <i>{round(float(check_wallet.json()['result']['balance']) * 0.000000001, 2)} TON</i></b>""", parse_mode='HTML')
        if check_wallet.json()["ok"] == False:
            await bot.send_message(message.from_user.id, """Некорректный адрес""")
    except:
        await bot.send_message(message.from_user.id, """Некорректный адрес""")
    
@dp.message_handler(commands=['remove_wallet'])
async def remove_wallet_handler_bot(message: types.Message):
    try:
        connect = await usfn.create_connection()
        address = message.text.split(' ')[1]
        try:
            asd = await usfn.delete_wallets(connect, message.from_user.id, address)
            await bot.send_message(message.from_user.id, """Успешно""")
            print(asd)
        except:
            await bot.send_message(message.from_user.id, """Ошибка""")
    except:
        await bot.send_message(message.from_user.id, """Некорректный адрес""")
    
async def check_wallet_changes(message):
    connect = await usfn.create_connection()
    while True:
        print(1)
        wallets = await usfn.get_all_wallets_user(connect, message.from_user.id)
        for i in wallets:
            await asyncio.sleep(1)
            check_wallet = requests.get(f'https://toncenter.com/api/v2/getAddressInformation?address={i[0]}')
            if round(float(check_wallet.json()['result']['balance']), 2) == round(float(i[2]), 2):
                pass
            else:
                await bot.send_message(message.from_user.id, f"""💰 Баланс изменился!
Кошелёк: {i[0]}
Новый баланс: {round(float(check_wallet.json()['result']['balance']) * 0.000000001, 2)} TON""")
        await asyncio.sleep(900)