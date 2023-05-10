import telebot
from datetime import datetime
import sqlite3

def writedata(userid, name, lastname, message):
    conn=sqlite3.connect('botik.db')
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (telegramid integer, name text, lastname text, datatime timestamp)")
    cursor.execute("SELECT * FROM users WHERE telegramid=%s" % (userid))
    result=cursor.fetchall()
    if len(result)==0:
        cursor.execute("INSERT INTO users VALUES (%s,'%s','%s','%s','%s')" % (userid,name,lastname,datetime.today(),'0'))
        conn.commit()

def avtomat (bot, userid, message,login):
    conn=sqlite3.connect('botik.db')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegramid=%s" % (userid))
    vasya=cursor.fetchall()
    status=vasya[0][4]
    if (message=="/help" and status==0):
        cursor.execute("UPDATE users SET status=1 WHERE telegramid=%s" % (userid))
        conn.commit()
        return "Расскажите в чем ваши проблемы. Мы постараемся вам помочь"
    elif (status==1):
        cursor.execute("UPDATE users SET status=0 WHERE telegramid=%s" % (userid))
        conn.commit()
        bot.send_message(956255361, "Вам от пользователя @"+str(login)+" пришло сообщение: "+message)
        return "Нам плевать на ваши жалкие проблемы. Мы ответим если захотим."
    else:
        return "Привет человег!"

token='6110380167:AAFIPKjH9W4c-lTyJGAE-J16W3qy_jKZtWw'

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def dima(message):
    writedata(message.chat.id, message.chat.first_name, message.chat.last_name, message.text)
    bot.send_message(message.chat.id, 'Привет! Рад познакомиться.\n\nЕсли тебе потребуется помощь, введи команду /help')

@bot.message_handler(commands=['time'])
def bot1(message):
    d=datetime.now()
    bot.send_message(message.chat.id, 'Точное время '+str(d.strftime("%d.%m.%Y %H:%M:%S")))

@bot.message_handler(commands=['myid'])
def bot2(message):
    bot.send_message(message.chat.id, 'Ваш ID '+str(message.chat.id))

@bot.message_handler(content_types=['photo'])
def bot3(message):
    bot.send_message(message.chat.id, 'Очень красивая фотка. Но это не точно:)')

@bot.message_handler(content_types=['text'])
def bot4(message):
    print(message)
    mes=avtomat (bot, message.chat.id, message.text, message.chat.username)
    bot.send_message(message.chat.id, mes)

bot.polling()