from playwright.sync_api import sync_playwright
from telebot import types
import telebot
import time
from flask import Flask,request
import os
from subprocess import Popen, PIPE
import sys

p = Popen([sys.executable, "-m", "playwright", "install"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
bot1_token='5345454658:AAFMgAm4NmwpDwRWcvEiZobBjalTYRJ961Y'
frws='https://results.eenadu.net/ts-inter-2022/ts-inter-1st-year-results-2022-general.aspx'
srws='https://results.eenadu.net/ts-inter-2022/ts-inter-2nd-year-results-2022-general.aspx'
sscws='https://results.eenadu.net/ts-tenth-2022/ts-10th-ssc-results-2022.aspx'

bot=telebot.TeleBot(bot1_token)
server=Flask(__name__)
@bot.message_handler(commands=['start'])
def welcome(message):
    marku=types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=2)
    marku.add('/FirstYear','/SecondYear')
    bot.send_message(message.chat.id, "Welcome to TS Inster Results Bot\nFor 1st year use command- /FirstYear\nFor 1st year use command- /SecondYear\nA bot by -Shashank",reply_markup=marku)
   
@bot.message_handler(commands=['FirstYear'])
def firstyr(message):
    sent_mess=bot.send_message(message.chat.id,"Send Roll No")
    bot.register_next_step_handler(sent_mess,fr)
@bot.message_handler(commands=['SecondYear'])
def secondyr(message):
    sent_mess=bot.send_message(message.chat.id,"Send Roll No")
    bot.register_next_step_handler(sent_mess,sr)

@server.route('/' + bot1_token, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ts-results-bot.herokuapp.com/' + bot1_token)
    return "The App is Running \nYou can Open Telegram now", 200

def fr(message):
    roll_number=message.text
    if (roll_number.lower()=="demo"):
        bot.send_photo(message.chat.id,"AgACAgUAAxkBAAEQwv9ixvCWG6IWGfy8tLlEe0BCXFy-hAACQrIxGyi_OFZt9ePlb7Y91AEAAwIAA3gAAykE")
    else:
        frs(roll_number)
        time.sleep(5)
        res=open("{}.png".format(roll_number),"rb")
        log=open('logs.txt','at')
        log.write(roll_number)
        log.close()
        bot.send_photo(message.chat.id,res)
        res.close()

def sr(message):
    roll_number=message.text
    if (roll_number.lower()=="demo"):
        bot.send_photo(message.chat.id,"AgACAgUAAxkBAAEQwv9ixvCWG6IWGfy8tLlEe0BCXFy-hAACQrIxGyi_OFZt9ePlb7Y91AEAAwIAA3gAAykE")
    else:
        frs(roll_number)
        time.sleep(5)
        res=open("{}.png".format(roll_number),"rb")
        log=open('logs.txt','at')
        log.write(roll_number)
        log.close()
        bot.send_photo(message.chat.id,res)
        res.close()

def frs(x):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(frws,timeout=0)
        page.type('#txtHTNo',x)
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)
        page.screenshot(path="{}.png".format(x),full_page=True)

def srs(x):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(srws,timeout=0)
        page.type('#txtHTNo',x)
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)
        page.screenshot(path="{}.png".format(x),full_page=True)

def ssc(x):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(sscws,timeout=0)
        page.type('#txtHTNo',x)
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)
        page.screenshot(path="{}.png".format(x),full_page=True)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
