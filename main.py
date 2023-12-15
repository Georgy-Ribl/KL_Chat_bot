import telebot
from config import TOKEN
from pyowm import OWM
from pyowm.utils.config import get_default_config
import json
#Инициализация OWM
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('20d7c2473ee824719d8b793bb6a4388f', config_dict)
mgr = owm.weather_manager()

#Инициализируем бота
bot = telebot.TeleBot(TOKEN)

print('Бот запущен!')


def read_json_file():
    with open('table.json', 'r') as file:
        data = json.load(file)
    return data
def write_json_file(data):
    with open('table.json', 'w') as file:
        json.dump(data, file, indent=2)

def add_user_preference(user_id, place):
    data = read_json_file()

    if user_id not in data:
        data[user_id] = {}

    data[user_id]["set_place"] = place

    write_json_file(data)

def get_user_data(user_id):
    data = read_json_file()
    return data.get(user_id, {})

#команда /start описывает бота
@bot.message_handler(commands=['start'])
def start_message(message):
    text = 'Вас приветствует бот погода!\n Что бы узнать погоду пропишите /place и черех пробел укажите место которое вас интересует'

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['set_place'])
def set_place(message):
    place = message.text
    place = place.split(' ')[1]
    add_user_preference(message.chat.id, place)
    msg = f'Готово!\nМесто по стандарту установлено как: {place}'
    updated_data = read_json_file()
    print(json.dumps(updated_data, indent=2, ensure_ascii=False))
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
