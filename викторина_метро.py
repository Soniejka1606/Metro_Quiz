import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
import gspread

bot = telebot.TeleBot('5907180411:AAGG_L1KNqmIj-3SeuqGBNPYFUe0hL82Dk8')

gc = gspread.service_account(filename="powerful-answer-378008-27deea09709c.json")
sht2 = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1fUu3aU7DhJoZl6X_KAX0GQVGvhqCW9f5iI0GbPPI5OA/edit?userstoinvite=e.butivshchenko@gmail.com&actionButton=1#gid=737320297')
worksheet = sht2.sheet1
list_of_lists = worksheet.get_all_values()

# print(list_of_lists[1][1])  # текст с первой строки
# print(list_of_lists[1][2])  # фото с первой строки
# print('--------')
# print(list_of_lists[2][1])  # текст со второй строки

def main_func(id,num):

    if list_of_lists[num][6] != '':
        mass = list_of_lists[num][6].split(',')
        wict = InlineKeyboardMarkup()

        for i in mass:
            if i == list_of_lists[num][7]:
                wict.add(InlineKeyboardButton(i, callback_data="T" + str(num)))

            else:
                wict.add(InlineKeyboardButton(i, callback_data="F" + str(num)))

        bot.send_message(id, list_of_lists[num][1], reply_markup=wict)
    else:
        keyb = InlineKeyboardMarkup()
        keyb.add(InlineKeyboardButton(list_of_lists[num][12],callback_data="n"+str(num)))
        # keyb.add(InlineKeyboardButton("↓", callback_data="n" + str(num)))
        try:
            photo1 = open(list_of_lists[num][2], 'rb')
            bot.send_photo(id, photo=photo1)
            photo1.close()
        except:
            pass

        try:
            audio1 = open(list_of_lists[num][4], 'rb')
            bot.send_audio(id, audio1)
            audio1.close()
        except:
            pass

        try:
            bot.send_message(id,list_of_lists[num][3])

        except:
            pass

        bot.send_message(id, list_of_lists[num][1],reply_markup=keyb)

# print(list_of_lists[2][3])
dict_stat = {'start': [],'end':[]}

@bot.message_handler(content_types=['text'])
def start(message):
    # print(message)
    if message.text == '/start':
        # bot.send_message(message.chat.id,
        #                        'Привет,' + ' ' + message.from_user.first_name + ',' + ' ' + "Начинаем?")
        main_func(message.chat.id, 1)
        dict_stat['start'].append(message.from_user.id)
    if message.text == '/stat':
        stat_text = f'Количество людей начавших квест - {len(dict_stat["start"])}\nКоличество людей дошедших до конца  - {len(dict_stat["end"])}'
        bot.send_message(message.chat.id,stat_text)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, )
    id = call.message.chat.id
    flag = call.data[0]
    data = call.data[1:]
    if flag == 'n':
        main_func(call.message.chat.id, int(data) + 1)
        if data == list_of_lists[int(48)][1]:
            if call.message.from_user.id not in dict_stat["end"]:
                dict_stat['end'].append(call.message.from_user.id)

    if flag == 'T':
        keyb = InlineKeyboardMarkup()
        keyb.add(InlineKeyboardButton(list_of_lists[int(data)][12], callback_data="n" +data))
        bot.send_message(id, list_of_lists[int(data)][8],reply_markup=keyb)
        try:
            photo1 = open(list_of_lists[int(data)][14], 'rb')
            bot.send_photo(id, photo=photo1)
            photo1.close()
        except:
            pass
        try:
            audio1 = open(list_of_lists[int(data)][15], 'rb')
            bot.send_audio(id, audio1)
            audio1.close()
        except:
            pass

    if flag == 'F':
        try:
            photo1 = open(list_of_lists[int(data)][14], 'rb')
            bot.send_photo(id, photo=photo1)
            photo1.close()
        except:
            pass
        try:
            audio1 = open(list_of_lists[int(data)][15], 'rb')
            bot.send_audio(id, audio1)
            audio1.close()
        except:
            pass
        keyb = InlineKeyboardMarkup()
        keyb.add(InlineKeyboardButton(list_of_lists[int(data)][12], callback_data="n" +data))
        bot.send_message(id, list_of_lists[int(data)][9],reply_markup=keyb)





print("Ready")
bot.infinity_polling()

"""

bot.send_message(IdOfMessage, text)  
сообщение


photo1 = open("file", 'rb')
bot.send_photo(IdOfMessage, photo=photo1)
photo1.close()
фото

audio1 = open("file", 'rb')
bot.send_audio(IdOfMessage, audio1)
audio1.close()
аудио

stic1 = open("file", 'rb')
bot.send_sticker(IdOfMessage, stic1)
stic1.close()
стикер
"""
