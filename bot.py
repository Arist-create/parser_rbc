import requests
from bs4 import BeautifulSoup
from telebot import types
import telebot
import asyncio
import os
import random
from dotenv import load_dotenv
load_dotenv()
from telebot.async_telebot import AsyncTeleBot
import mysql.connector

def SQL(func, what, chat_id, key):
    db = mysql.connector.connect(
        host=os.getenv('HOST'),
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        port=os.getenv('PORT'),
        tls_versions=['TLSv1.1', 'TLSv1.2']
    )
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories(
        chat_id INT,
        categories VARCHAR(100)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS random(
        chat_id INT,
        random INT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS checks(
        chat_id INT,
        checks VARCHAR(100)
    )''')
    db.commit()
    global items
    items = []
    if func == 'SELECT':
        if what == 'categories':
            cursor.execute("SELECT categories FROM categories WHERE chat_id = %s", (chat_id, ))
            b_items = cursor.fetchall()
            for i in b_items:
                items.append(i[0])
        if what == 'random':
            cursor.execute("SELECT random FROM random WHERE chat_id = %s", (chat_id, ))
            b_items = cursor.fetchall()
            for i in b_items:
                items.append(i[0])
        if what == 'checks':
            cursor.execute("SELECT checks FROM checks WHERE chat_id = %s", (chat_id, ))
            b_items = cursor.fetchall()
            for i in b_items:
                items.append(i[0])
    if func == 'UPDATE':
        if what == 'random':
            cursor.execute("UPDATE random SET random = %s WHERE chat_id = %s", (key, chat_id))
        if what == 'checks':
            cursor.execute("UPDATE checks SET checks = %s WHERE chat_id = %s", (key, chat_id))
    if func == 'INSERT':
        if what == 'categories':
            cursor.execute("INSERT INTO categories VALUES (%s,%s)", (chat_id, key))
        if what == 'random':
            cursor.execute("INSERT INTO random VALUES (%s,%s)", (chat_id, key))
        if what == 'checks':
            cursor.execute("INSERT INTO checks VALUES (%s,%s)", (chat_id, key))
    if func == 'DELETE':
        cursor.execute("DELETE FROM categories WHERE chat_id = %s",(chat_id, ))
    db.commit()
    db.close()

bot = AsyncTeleBot(os.getenv('TOKEN'))
@bot.message_handler(content_types=['text'])
async def get_text_messages(message):
    global items
    if message.text == '/start' or message.text == 'Вернуться в главное меню' or message.text == 'Парсить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sub = types.KeyboardButton('Подписки')
        markup.add(sub)
        await bot.send_message(message.chat.id, text= 'Нажмите "Подписки" если хотите выбрать или отредактировать категории новостей',reply_markup=markup)
    if message.text == 'Выбрать категории':
        SQL('DELETE', 'categories', message.chat.id, None)
        key = random.randrange(1, 1000000)
        SQL('SELECT', 'random', message.chat.id, None)
        if len(items) != 0:
            SQL('UPDATE', 'random', message.chat.id, key)
        else:
            SQL('INSERT', 'random', message.chat.id, key)
            
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cat1 = types.KeyboardButton('Политика')
        cat2 = types.KeyboardButton('Экономика')
        cat3 = types.KeyboardButton('Спорт')
        cat4 = types.KeyboardButton('Общество')
        cat5 = types.KeyboardButton('Финансы')
        cat6 = types.KeyboardButton('Технологии и медиа')
        back = types.KeyboardButton('Парсить')
        markup.add(cat1, cat2, cat3, cat4, cat5, cat6, back)
        await bot.send_message(message.chat.id, 'Выберите категории или нажмите вернитесь в меню подписок для завершения', reply_markup=markup)
    
    if message.text == 'Активные категории':
        SQL('SELECT', 'categories', message.chat.id, None)
        if len(items) == 0:
            await bot.send_message(message.chat.id, 'Нет')
        else:
            for el in items:
                await bot.send_message(message.chat.id, el)
    if message.text == 'Подписки' or message.text == 'Вернуться в меню подписок':
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sub = types.KeyboardButton('Активные категории')
        reload = types.KeyboardButton('Выбрать категории')
        back = types.KeyboardButton('Вернуться в главное меню')
        markup.add(sub, reload, back)
        await bot.send_message(message.chat.id, 'Выберите пункт',reply_markup=markup)
       
    if message.text == 'Экономика' or message.text == 'Политика' or message.text == 'Спорт' or message.text == 'Общество' or message.text == 'Финансы' or message.text == 'Технологии и медиа':
        SQL('SELECT', 'categories', message.chat.id, None)
        if (message.text in items):
            await bot.send_message(message.chat.id, 'Уже добавлено!')
        else:
            SQL('INSERT', 'categories', message.chat.id, message.text)
            await bot.send_message(message.chat.id, 'Выберите ещё или начните парсинг')
    if message.text == 'Парсить':
        arr =[]
        SQL('SELECT', 'categories', message.chat.id, None)   
        arr = items
        if len(items) != 0:
            await bot.send_message(message.chat.id, 'Парсим!')
            SQL('SELECT', 'random', message.chat.id, None)
            for el in items:
                key = el
            key_parse = key
            check_href = 0
            
            while 0 == 0:
                SQL('SELECT', 'random', message.chat.id, None)
                if len(items) != 0:
                    for el in items:
                        key = el
                    if key_parse != key:
                        break
                    r = requests.get('https://www.rbc.ru/short_news')
                    soup = BeautifulSoup(r.content, 'html.parser')
                    try:
                        img = soup.find('div', class_='item__wrap l-col-center').find('img').get('src')
                    except:
                        img = 'https://koronapay.com/transfers/europe/static/rbk_05b1697cef-1e51cefc9b0d1f98b617abdaf35b7417.jpg'
                
                    txt = soup.find('div', class_='item__wrap l-col-center').find('span', class_='item__title rm-cm-item-text')
                    href = soup.find('a', class_='item__link').get('href')
                    tema = soup.find('div', class_='item__bottom').find('a', class_='item__category')
                    if tema != None:
                        if (tema.text.strip()[:-1] in arr) == True and (href != check_href):
                            
                            SQL('SELECT', 'checks', message.chat.id, None)
                            if len(items) != 0:
                                SQL('UPDATE', 'checks', message.chat.id, href)
                            else:
                                SQL('INSERT', 'checks', message.chat.id, href)
                            SQL('SELECT', 'checks', message.chat.id, None)
                            for el in items:
                                check_href = el
                            markup = types.InlineKeyboardMarkup()
                            button = types.InlineKeyboardButton("Перейти к новости", url=href)
                            markup.add(button)

                            await bot.send_photo(message.chat.id, photo = img , caption = f'<b>{txt.text.strip()}</b>' + '\n' + '\n' + f'<em>{tema.text.strip()[:-1]}</em>', reply_markup=markup, parse_mode= "html") 
                    await asyncio.sleep(60)    
            else:
                await bot.send_message(message.chat.id, 'Вы не выбрали категории. Нажмите "Подписки", затем "Выбрать категории"')
asyncio.run(bot.polling(non_stop=True))