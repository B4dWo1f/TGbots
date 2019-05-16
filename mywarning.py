#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#import telegram
#from base64 import b64decode as decode
#from time import sleep
import os
#here = os.path.dirname(os.path.realpath(__file__))
from random import choice
import threading
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from telegram.ext import Updater
import onlyfunctions as f
from telegram.ext import CommandHandler, Filters


token, chatID = f.get_credentials()
updater = Updater(token=token)
dispatcher = updater.dispatcher


def start(bot, update):
   txt = "I'm a bot, please talk to me!"
   bot.send_message(chat_id=update.message.chat_id, text=txt)

def shutdown():
   updater.stop()
   updater.is_idle = False

def stop(bot, update):
   txt = 'I\'ll be shutting down\nI hope to see you soon!'
   bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
   threading.Thread(target=shutdown).start()

def stop_and_restart():
   """
   Gracefully stop the Updater and replace the current process with a new one
   """
   updater.stop()
   os.execl(sys.executable, sys.executable, *sys.argv)

from threading import Thread
import sys

def restart(bot,update):
   txt = 'Bot is restarting...'
   chatID = update.message.chat_id
   bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
   #update.message.reply_text('Bot is restarting...')
   Thread(target=stop_and_restart).start()

usernames = open('username.whitelist','r').read().strip().splitlines()

# Start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
# Re-Load
dispatcher.add_handler(CommandHandler('reload', restart, filters=Filters.user(username='@n0w3l')))
# Hola
hola_handler = CommandHandler('hola', f.hola,
                              filters=Filters.user(username=usernames))
dispatcher.add_handler(hola_handler)
# Lock
lock_handler = CommandHandler('lock', f.screen_lock)
dispatcher.add_handler(lock_handler)
# Screenshot
screenshot_handler = CommandHandler('screenshot', f.screenshot)
dispatcher.add_handler(screenshot_handler)
# Picture
picture_handler = CommandHandler('picture', f.picture)
dispatcher.add_handler(picture_handler)
# Sound
sound_handler = CommandHandler('sound', f.sound)
dispatcher.add_handler(sound_handler)
# Where Are You
whry_handler = CommandHandler('where', f.whereRyou)
dispatcher.add_handler(whry_handler)
# Who is there
whit_handler = CommandHandler('whothere', f.whoSthere)
dispatcher.add_handler(whit_handler)
# Help
help_handler = CommandHandler('help', f.help_msg)
dispatcher.add_handler(help_handler)
# Stop
stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)



updater.start_polling()
print(usernames)
