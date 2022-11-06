# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from telebot import types
import telebot 


import time
import os
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
arr = []
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start' or message.text == 'Вернуться в главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        parser = types.KeyboardButton('Парсить')
        sub = types.KeyboardButton('Подписки')
        markup.add(parser, sub)
        bot.send_message(message.chat.id, text= 'Нажмите "Подписки" если хотите выбрать или отредактировать категории новостей'+'\n'+ 'Нажмите "Парсить" для запуска парсера',reply_markup=markup)
    if message.text == 'Выбрать категории':
        global arr
        arr = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cat1 = types.KeyboardButton('Политика')
        cat2 = types.KeyboardButton('Экономика')
        cat3 = types.KeyboardButton('Спорт')
        cat4 = types.KeyboardButton('Общество')
        cat5 = types.KeyboardButton('Финансы')
        back = types.KeyboardButton('Вернуться в меню подписок')
        markup.add(cat1, cat2, cat3, cat4, cat5, back)
        bot.send_message(message.chat.id, 'Выберите категории или нажмите вернитесь в меню подписок для завершения',reply_markup=markup)
    
    if message.text == 'Активные категории':
        i = 0
        if len(arr) == 0:
            bot.send_message(message.chat.id, 'Нет')
        else:
            while i < len(arr):
                bot.send_message(message.chat.id, arr[i])
                i += 1
    if message.text == 'Подписки' or message.text == 'Вернуться в меню подписок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sub = types.KeyboardButton('Активные категории')
        reload = types.KeyboardButton('Выбрать категории')
        back = types.KeyboardButton('Вернуться в главное меню')
        markup.add(sub, reload, back)
        bot.send_message(message.chat.id, 'Выберите пункт',reply_markup=markup)
    if message.text == 'Экономика' or message.text == 'Политика' or message.text == 'Спорт' or message.text == 'Общество' or message.text == 'Финансы':
        if message.text not in arr:
            arr.append(message.text)
        bot.send_message(message.chat.id, 'Выберите ещё или вернитесь в меню подписок')
    
    if message.text == 'Парсить':
        if len(arr) == 0:
            bot.send_message(message.chat.id, 'Вы не выбрали категории. Нажмите "Подписки", затем "Выбрать категории"')
        else:
            bot.send_message(message.chat.id, 'Парсим!')
        check = 0
       
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
                if txt != check:
                    check = txt
                    markup = types.InlineKeyboardMarkup()
                    button = types.InlineKeyboardButton("Перейти к новости", url=href)
                    markup.add(button)

                    bot.send_photo(message.chat.id, photo = img , caption = f'<b>{txt.text.strip()}</b>' + '\n' + '\n' + f'<em>{tema.text.strip()[:-1]}</em>', reply_markup=markup, parse_mode= "html") 

            time.sleep(60)
           
bot.polling(none_stop=True)

