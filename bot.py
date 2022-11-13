# -*- coding: utf-8 -*-
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
import sqlite3

db = sqlite3.connect('Users.db')
sql = db.cursor()
sql.execute('''CREATE TABLE IF NOT EXISTS categories(
    chat_id INT,
    categories STR
)''')
sql.execute('''CREATE TABLE IF NOT EXISTS keys(
    chat_id INT,
    keys INT
)''')
sql.execute('''CREATE TABLE IF NOT EXISTS checks(
    chat_id INT,
    checks STR
)''')
db.commit()
db.close()


bot = AsyncTeleBot(os.getenv('TOKEN'))
@bot.message_handler(content_types=['text'])
async def get_text_messages(message):

    if message.text == '/start' or message.text == 'Вернуться в главное меню' or message.text == 'Парсить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sub = types.KeyboardButton('Подписки')
        markup.add(sub)
        await bot.send_message(message.chat.id, text= 'Нажмите "Подписки" если хотите выбрать или отредактировать категории новостей',reply_markup=markup)
    if message.text == 'Выбрать категории':
        db = sqlite3.connect('Users.db')
        sql = db.cursor()
        sql.execute("DELETE FROM categories WHERE chat_id = ?",(message.chat.id, ))
        db.commit()
        
        key = random.randrange(1, 1000000)
        items = sql.execute("SELECT keys FROM keys WHERE chat_id = ?", (message.chat.id, )).fetchall()
        if len(items) != 0:
            sql.execute("UPDATE keys SET keys = ? WHERE chat_id = ?", (key, message.chat.id))
            db.commit()
        else:
            sql.execute("INSERT INTO keys VALUES (?,?)", (message.chat.id, key))
            db.commit()
        db.close()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cat1 = types.KeyboardButton('Политика')
        cat2 = types.KeyboardButton('Экономика')
        cat3 = types.KeyboardButton('Спорт')
        cat4 = types.KeyboardButton('Общество')
        cat5 = types.KeyboardButton('Финансы')
        cat6 = types.KeyboardButton('Технологии и медиа')
        back = types.KeyboardButton('Парсить')
        markup.add(cat1, cat2, cat3, cat4, cat5, cat6, back)
        await bot.send_message(message.chat.id, 'Выберите категории или нажмите вернитесь в меню подписок для завершения',reply_markup=markup)
    
    if message.text == 'Активные категории':
        db = sqlite3.connect('Users.db')
        sql = db.cursor()
        items = sql.execute("SELECT categories FROM categories WHERE chat_id = ?", (message.chat.id, )).fetchall()
        if len(items) != 0:
            for el in items:
                await bot.send_message(message.chat.id, el[0])
        else:
            await bot.send_message(message.chat.id, 'Нет')
        db.close()
    if message.text == 'Подписки' or message.text == 'Вернуться в меню подписок':
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sub = types.KeyboardButton('Активные категории')
        reload = types.KeyboardButton('Выбрать категории')
        back = types.KeyboardButton('Вернуться в главное меню')
        markup.add(sub, reload, back)
        await bot.send_message(message.chat.id, 'Выберите пункт',reply_markup=markup)
       
    if message.text == 'Экономика' or message.text == 'Политика' or message.text == 'Спорт' or message.text == 'Общество' or message.text == 'Финансы' or message.text == 'Технологии и медиа':
        arr = []
        db = sqlite3.connect('Users.db')
        sql = db.cursor()
        items = sql.execute("SELECT categories FROM categories WHERE chat_id = ?", (message.chat.id, )).fetchall()
        if len(items) != 0:
            for el in items:
                arr.append(el[0])
            if (message.text in arr):
                await bot.send_message(message.chat.id, 'Уже добавлено!')
            else:
                sql.execute("INSERT INTO categories VALUES (?,?)", (message.chat.id, message.text))
                db.commit()
                await bot.send_message(message.chat.id, 'Выберите ещё или начните парсинг')
        else:
            sql.execute("INSERT INTO categories VALUES (?,?)", (message.chat.id, message.text))
            db.commit()
            await bot.send_message(message.chat.id, 'Выберите ещё или начните парсинг')
        db.close()
    if message.text == 'Парсить':
        arr = []
        db = sqlite3.connect('Users.db')
        sql = db.cursor()
        items = sql.execute("SELECT categories FROM categories WHERE chat_id = ?", (message.chat.id, )).fetchall()
        for el in items:
            arr.append(el[0])
        if len(arr) == 0:
            await bot.send_message(message.chat.id, 'Вы не выбрали категории. Нажмите "Подписки", затем "Выбрать категории"')
            db.close()
        else:
            await bot.send_message(message.chat.id, 'Парсим!')
            
            items = sql.execute("SELECT keys FROM keys WHERE chat_id = ?", (message.chat.id, )).fetchall()
            db.close()
            for el in items:
                key = el[0]
            key_parse = key
            
            check_href = 0

            while 0 == 0:
                db = sqlite3.connect('Users.db')
                sql = db.cursor()
                items = sql.execute("SELECT keys FROM keys WHERE chat_id = ?", (message.chat.id, )).fetchall()
                db.close()

                for el in items:
                    key = el[0]
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
                        db = sqlite3.connect('Users.db')
                        sql = db.cursor()
                        items = sql.execute("SELECT checks FROM checks WHERE chat_id = ?", (message.chat.id, )).fetchall()
                        if len(items) != 0:
                            sql.execute("UPDATE checks SET checks = ? WHERE chat_id = ?", (href, message.chat.id))
                            db.commit()
                        else:
                            sql.execute("INSERT INTO checks VALUES (?,?)", (message.chat.id, href))
                            db.commit()
                        items = sql.execute("SELECT checks FROM checks WHERE chat_id = ?", (message.chat.id, )).fetchall()
                        db.close()
                        for el in items:
                            check_href = el[0]
                        markup = types.InlineKeyboardMarkup()
                        button = types.InlineKeyboardButton("Перейти к новости", url=href)
                        markup.add(button)

                        await bot.send_photo(message.chat.id, photo = img , caption = f'<b>{txt.text.strip()}</b>' + '\n' + '\n' + f'<em>{tema.text.strip()[:-1]}</em>', reply_markup=markup, parse_mode= "html") 

                await asyncio.sleep(60)    

asyncio.run(bot.polling(non_stop=True))