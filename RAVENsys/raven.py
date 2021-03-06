#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from threading import Thread
# Telegram-Bot libraries
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
# My functions
import credentials as CR
import mycallbacks as cb


## Stop Bot ####################################################################
def shutdown():
   upt.stop()
   upt.is_idle = False

@CR.restricted
def stop(bot, update):
   chatID = update.message.chat_id
   txt = 'I\'ll be shutting down\nI hope to see you soon!'
   M = bot.send_message(chatID, text=txt,
                        parse_mode='Markdown')
   Thread(target=shutdown).start()


## Reload Bot ##################################################################
def stop_and_restart():
   """
   Gracefully stop the Updater and replace the current process with a new one
   """
   upt.stop()
   os.execl(sys.executable, sys.executable, *sys.argv)

@CR.restricted
def restart(bot,update):
   txt = 'Bot is restarting...'
   chatID = update.message.chat_id
   bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
   Thread(target=stop_and_restart).start()


if __name__ == '__main__':
   import os
   import sys
   import logging
   logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
   here = os.path.dirname(os.path.realpath(__file__))
   try: token = sys.argv[1]
   except IndexError:
      if os.path.isfile(here+'/RAVENsys.token'):
         token = here+'/RAVENsys.token'
      else:
         print('File not specified')
         exit()
   
   token = CR.get_credentials(token)

   # Define the Bot
   upt = Updater(token=token)
   dpt = upt.dispatcher
   jbq = upt.job_queue
   
   ## Add Handlers
   #sys handlers
   dpt.add_handler(CommandHandler('lock', cb.screen_lock))

   #sentinel handlers
   dpt.add_handler(CommandHandler('screenshot',
                                  cb.screenshot,
                                  pass_job_queue=True))
   dpt.add_handler(CommandHandler('picture', cb.picture, pass_job_queue=True))
   dpt.add_handler(CommandHandler('sound', cb.sound))
   dpt.add_handler(CommandHandler('where', cb.whereRyou))
   dpt.add_handler(CommandHandler('whothere', cb.whoSthere))
   dpt.add_handler(CommandHandler('whoami', cb.whoami))
   dpt.add_handler(CommandHandler('who', cb.who))


   #admin handlers
   dpt.add_handler(CommandHandler('hola', cb.hola, pass_job_queue=True))
   dpt.add_handler(CommandHandler('reload', restart))
   dpt.add_handler(CommandHandler('stop', stop))
   

   upt.start_polling()

###import telegram
###from base64 import b64decode as decode
###from time import sleep
##import os
###here = os.path.dirname(os.path.realpath(__file__))
##from random import choice
##import threading
##
##from threading import Thread
##import sys
##from telegram.ext import Updater
##import onlyfunctions as f
##
##token, chatID = CR.get_credentials()
##updater = Updater(token=token)
##dispatcher = updater.dispatcher
##j = updater.job_queue
##
##def start(bot, update):
##   txt = "I'm a bot, please talk to me!"
##   bot.send_message(chat_id=update.message.chat_id, text=txt)
##
##def shutdown():
##   updater.stop()
##   updater.is_idle = False
##
##@CR.restricted
##def stop(bot, update):
##   txt = 'I\'ll be shutting down\nI hope to see you soon!'
##   bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
##   threading.Thread(target=shutdown).start()
##
##def stop_and_restart():
##   """
##   Gracefully stop the Updater and replace the current process with a new one
##   """
##   updater.stop()
##   os.execl(sys.executable, sys.executable, *sys.argv)
##
##
##@CR.restricted
##def restart(bot,update):
##   txt = 'Bot is restarting...'
##   chatID = update.message.chat_id
##   bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
##   #update.message.reply_text('Bot is restarting...')
##   Thread(target=stop_and_restart).start()
##
##
### Start
##start_handler = CommandHandler('start', start)
##dispatcher.add_handler(start_handler)
##
### Re-Load
##dispatcher.add_handler(CommandHandler('reload', restart))
### Hola
##hola_handler = CommandHandler('hola', f.hola, pass_job_queue=True)
##dispatcher.add_handler(hola_handler)
### Lock
##lock_handler = CommandHandler('lock', f.screen_lock)
##dispatcher.add_handler(lock_handler)
### Screenshot
##screenshot_handler = CommandHandler('screenshot', f.screenshot)
##dispatcher.add_handler(screenshot_handler)
### Picture
##picture_handler = CommandHandler('picture', f.picture, pass_job_queue=True)
##dispatcher.add_handler(picture_handler)
### Sound
##sound_handler = CommandHandler('sound', f.sound)
##dispatcher.add_handler(sound_handler)
### Where Are You
##whry_handler = CommandHandler('where', f.whereRyou)
##dispatcher.add_handler(whry_handler)
### Who is there
##whit_handler = CommandHandler('whothere', f.whoSthere)
##dispatcher.add_handler(whit_handler)
### Who am I
##whoami_handler = CommandHandler('whoami', f.whoami)
##dispatcher.add_handler(whoami_handler)
### Help
##help_handler = CommandHandler('help', f.help_msg)
##dispatcher.add_handler(help_handler)
### Stop
##stop_handler = CommandHandler('stop', stop)
##dispatcher.add_handler(stop_handler)
##### Testing ####################################################################
##import testing as tst
##location_handler = MessageHandler(Filters.location, tst.location, 
##                                                          edited_updates=True)
##dispatcher.add_handler(location_handler)
