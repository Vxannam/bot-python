import telebot
import requests
import time
from translate import Translator


token = "1310730598:AAF7KY5kRqHhk6BOFiceKrIUh1ktpmO-t_I"
bot = telebot.TeleBot(token)

translator = Translator(from_lang="English", to_lang="Russian")

api_adres= "http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="

note_list = []

@bot.message_handler(commands=['start'])
def start_command(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/start','/weather','/notes')
    user_markup.row('/new_note','/print_note','/del_note')

    bot.send_message(message.from_user.id,
        'Привет, дорогой мой друг!\n' +
        '-Если ты хочешь узнать погоду /weather \n' +
        '-Если ты хочешь узнать другие функции бота /help.', reply_markup=user_markup)

@bot.message_handler(commands=['weather'])
def handle_text(message):
    bot.send_message(message.chat.id, 'Введи название города в формате : moscow')
    @bot.message_handler(content_types=['text'])
    def city_text(message):
        url = api_adres + message.text
        json_data = requests.get(url).json()
        formatted_temp = json_data['main']['temp']
        formatted_desc = json_data['weather'][0]['description']
        bot.send_message(message.chat.id, formatted_temp-273.15)
        result = translator.translate(formatted_desc)
        bot.send_message(message.chat.id, result)




# bot.send_message(390695710, "Все работает, пробуй")

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(2)
            print(e)