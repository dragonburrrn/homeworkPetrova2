# Вариант 3 - меню, анекдот, картинка

import telebot  # pyTelegramBotAPI	4.3.1
from telebot import types
import requests
import bs4

import wikipedia, re

#русский язык в википедии
wikipedia.set_lang("ru")

bot = telebot.TeleBot('5204365820:AAFvuyokcKcxoDygSTsQ4I60SkiHMPNK8QU')  # Создаем экземпляр бота @Ivanov_Ivan_1MD19_bot

# -----------------------------------------------------------------------
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton ("Главное меню")
    btn2 = types.KeyboardButton ("Помощь")
    markup.add(btn1, btn2)

    bot.send_message(chat_id, text="Привет, {0.first_name} ! Я тестовый бот для курса программирования на языке ПаЙтон".format(message.from_user), reply_markup=markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Главное меню" or ms_text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Развлечения")
        btn2 = types.KeyboardButton("Wikipedia")
        btn3 = types.KeyboardButton("Управление")
        back = types.KeyboardButton("Помощь")
        markup.add(btn1, btn2, btn3,back)
        bot.send_message(chat_id, text="Вы на главном меню", reply_markup=markup)
    elif ms_text == "Развлечения":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Прислать собачку")
        btn2 = types.KeyboardButton("Прислать анекдот")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(chat_id, text="Развлечения", reply_markup=markup)

    elif ms_text == "Собачка" or ms_text == "Прислать собачку":

        contens = requests.get('https://random.dog/woof.json').json()
        urlDogs = contens['url']
        bot.send_photo(chat_id, photo=urlDogs, caption="Собачка")

    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())
    elif ms_text == "Wikipedia":
        bot.send_message(chat_id, 'Отправьте любое слово, и я найду его значение на wikipedia')



    elif ms_text == "Управление":
        bot.send_message(chat_id, text="еще не готово...")
    elif ms_text == "Помощь" or ms_text == "/help":
        bot.send_message(chat_id, text="Автор: Петрова Анастасия")
        key1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://vk.com/dragonburrrn")
        key1.add(btn1)
        img = open('Петрова Анастасия.jpg', 'rb')
        bot.send_photo(message.chat.id, img, reply_markup=key1)
    else:
        bot.send_message(message.chat.id, getwiki(message.text))

# ----------------------------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    req_anek = requests.get("https://nekdo.ru/random/")
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select(".text")
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]
# -----------------------------------------------------------------------

# чистим текст статьи в wikipedia и ограничиваем его тысячей символов
def getwiki(s):

    print('fff')

    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('{[^\{\}]*\)', '', wikitext2)
        return wikitext2
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


bot.polling(none_stop=True, interval=0) # Запускаем бота

print()