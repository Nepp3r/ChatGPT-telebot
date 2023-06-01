#! ../telebot-venv/bin/python3

import telebot
import openai

bot_token = open("bot-token", "r").readline()
bot_token = bot_token[:-1] #It is very important, nl symbol crashes bot because of bad token
bot = telebot.TeleBot(bot_token)
openai.api_key = open("gpt-api", "r").readline()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}, I\'m a bot, that allows you to use ChatGPT inside telegram chats! For more information: /help \n\n P.S. I\'m a bit slow due to some technical details')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,'You can ask me a question in this format: \n\"gpt question\"\nQuestion is actually the question that you\'d like to ask and only gpt required at any part of your message', parse_mode="html")

@bot.message_handler()
def info(message):
    if "gpt" in message.text.split():
        print(message.text)
        request = message.text.replace("gpt", "")        
        answer = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": request}])
        bot.send_message(message.chat.id, answer.choices[0].message.content, parse_mode="html")

bot.polling(none_stop=True)
