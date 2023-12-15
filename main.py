import telebot
import sqlite3
from telebot import types
from config import TOKEN
from pyowm import OWM
from pyowm.utils.config import get_default_config
#Инициализация OWM
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('20d7c2473ee824719d8b793bb6a4388f', config_dict)
mgr = owm.weather_manager()

#Инициализируем бота
bot = telebot.TeleBot(TOKEN)

print('Бот запущен!')

#команда /start описывает бота
@bot.message_handler(commands=['start'])
def start_message(message):
    id = message.from_user.id
    text = 'Вас приветствует бот погода!\n Что бы узнать погоду пропишите /place и черех пробел укажите место которое вас интересует'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['set_place'])
def set_place(message):
    place = message.text.split(' ')[1]
    id = message.from_user.id
    msg = f'Готово!\nМесто по стандарту установлено как: {place}'
    bot.send_message(message.chat.id, msg)



#команда /place показывает погоду в установленом городе
@bot.message_handler(commands=['place'])
def place_message(message):
    place = message.text.split('/place')[1].strip(' ')
    observation = mgr.weather_at_place(place)
    w = observation.weather
    temp = w.temperature('celsius')['temp']
    msg = f'Погода в городе {place} : {temp}'
    bot.send_message(message.chat.id, msg )

bot.infinity_polling()
