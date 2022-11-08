# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from telebot import types
import telebot 
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from telebot.async_telebot import AsyncTeleBot

arr = []

bot = AsyncTeleBot(os.getenv('TOKEN'))

@bot.message_handler(content_types=['text'])
async def get_text_messages(message):
    if message.text == '/start' or message.text == 'Вернуться в главное меню' or message.text == 'Парсить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sub = types.KeyboardButton('Подписки')
        markup.add(sub)
        await bot.send_message(message.chat.id, text= 'Нажмите "Подписки" если хотите выбрать или отредактировать категории новостей',reply_markup=markup)
    if message.text == 'Выбрать категории':
        global arr
        arr=[]
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
        i = 0
        if len(arr) == 0:
            await bot.send_message(message.chat.id, 'Нет')
        else:
            while i < len(arr):
                await bot.send_message(message.chat.id, arr[i])
                i += 1
    if message.text == 'Подписки' or message.text == 'Вернуться в меню подписок':
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sub = types.KeyboardButton('Активные категории')
        reload = types.KeyboardButton('Выбрать категории')
        back = types.KeyboardButton('Вернуться в главное меню')
        markup.add(sub, reload, back)
        await bot.send_message(message.chat.id, 'Выберите пункт',reply_markup=markup)
       
    if message.text == 'Экономика' or message.text == 'Политика' or message.text == 'Спорт' or message.text == 'Общество' or message.text == 'Финансы' or message.text == 'Технологии и медиа':
        if message.text not in arr:
            arr.append(message.text)
        await bot.send_message(message.chat.id, 'Выберите ещё или начните парсинг')
    
    if message.text == 'Парсить':
        if len(arr) == 0:
            await bot.send_message(message.chat.id, 'Вы не выбрали категории. Нажмите "Подписки", затем "Выбрать категории"')
        else:
            await bot.send_message(message.chat.id, 'Парсим!')
        check_txt = 0
        check_href = 0
       
        while len(arr) > 0:
            r = requests.get('https://www.rbc.ru/short_news')
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                img = soup.find('div', class_='item__wrap l-col-center').find('img').get('src')
            except:
                img = 'https://koronapay.com/transfers/europe/static/rbk_05b1697cef-1e51cefc9b0d1f98b617abdaf35b7417.jpg'
                
            txt = soup.find('div', class_='item__wrap l-col-center').find('span', class_='item__title rm-cm-item-text')
            href = soup.find('a', class_='item__link').get('href')
            try:
                tema = soup.find('div', class_='item__bottom').find('a', class_='item__category')
            except:
                print('Ошибка')
                
            if (tema.text.strip()[:-1] in arr) == True:
                if txt != check_txt and href != check_href:
                    check_txt = txt
                    check_href = href
                    markup = types.InlineKeyboardMarkup()
                    button = types.InlineKeyboardButton("Перейти к новости", url=href)
                    markup.add(button)

                    await bot.send_photo(message.chat.id, photo = img , caption = f'<b>{txt.text.strip()}</b>' + '\n' + '\n' + f'<em>{tema.text.strip()[:-1]}</em>', reply_markup=markup, parse_mode= "html") 

            await asyncio.sleep(60)    
asyncio.run(bot.infinity_polling())