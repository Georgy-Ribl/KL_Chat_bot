import telebot
from telebot import types
from config import TOKEN, OWM_API
from pyowm import OWM
from pyowm.utils.config import get_default_config
#Инициализация OWM
#Инициализируем бота
bot = telebot.TeleBot(TOKEN)

#Инициализация OWM
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(OWM_API, config_dict)
mgr = owm.weather_manager()


print('Бот запущен!')
#документация OWM https://buildmedia.readthedocs.org/media/pdf/pyowm/latest/pyowm.pdf

#команда /start описывает бота
@bot.message_handler(commands=['start'])
def start_message(message):
    id = message.from_user.id
    text = 'Здравствуйте! Вас приветствует бот, помогающий определить погоду!\nЧтобы узнать погоду, пожалуйста, пропишите команду /place, через тире искомую информацию на английском языке(можно выбрать температуру, ветер, давление или видимость), а затем через пробел укажите нужное Вам местоположение'
    bot.send_message(message.chat.id, text)

#команда /place показывает нужную погоду в запрашиваемом городе
@bot.message_handler(commands=['place-temperature'])
def place_message(message):
    place = message.text.split('/place-temperature')[1].strip(' ')
    observation = mgr.weather_at_place(place)
    w = observation.weather
    temp = w.temperature('celsius')['temp']
    msg = f'Температура в городе {place} {temp} градусов по Цельсию.\nСпасибо за то, что пользуетесь нашим ботом!'
    bot.send_message(message.chat.id, msg )

@bot.message_handler(commands=['place-wind'])
def place_message(message):
    place = message.text.split('/place-wind')[1].strip(' ')
    observation = mgr.weather_at_place(place)
    w = observation.weather
    wind_dict_in_meters_per_sec = w.wind()['speed']
    msg = f'Скорость ветра в городе {place} {wind_dict_in_meters_per_sec} метров в секунду.\nСпасибо за то, что пользуетесь нашим ботом!'
    bot.send_message(message.chat.id, msg )

@bot.message_handler(commands=['place-pressure'])
def place_message(message):
    place = message.text.split('/place-pressure')[1].strip(' ')
    observation = mgr.weather_at_place(place)
    w = observation.weather
    pressure = w.barometric_pressure(unit='inHg')['press'] #pressure in current location
    msg = f'Давление в городе {place} {pressure} inHg.\nСпасибо за то, что пользуетесь нашим ботом!'
    bot.send_message(message.chat.id, msg )

@bot.message_handler(commands=['place-visibility'])
def place_message(message):
    place = message.text.split('/place-visibility')[1].strip(' ')
    observation = mgr.weather_at_place(place)
    w = observation.weather
    visibility = w.visibility_distance #in metres
    msg = f'Видимость в городе {place} {visibility} метров.\nСпасибо за то, что пользуетесь нашим ботом!'
    bot.send_message(message.chat.id, msg)
bot.infinity_polling()