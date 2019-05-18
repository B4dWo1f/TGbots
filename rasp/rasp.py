#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import credentials as CR
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from threading import Thread
import datetime as dt
import sys
import os
here = os.path.dirname(os.path.realpath(__file__))

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
                    datefmt='%Y/%m/%d-%H:%M:%S',
                    filename=here+'/main.log', filemode='w')

LG = logging.getLogger('main')



def start(bot, update):
   txt = "I'm a bot, please talk to me!"
   bot.send_message(chat_id=update.message.chat_id, text=txt)
   txt = "Only for me I'm a bot, please talk to me!"
   bot.send_message(chat_id=3875655, text=txt)

def shutdown():
   U.stop()
   U.is_idle = False

@CR.restricted
def stop(bot, update):
   txt = 'I\'ll be shutting down\nI hope to see you soon!'
   bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
   Thread(target=shutdown).start()

def stop_and_restart():
   """
   Gracefully stop the Updater and replace the current process with a new one
   """
   U.stop()
   os.execl(sys.executable, sys.executable, *sys.argv)


@CR.restricted
def restart(bot,update):
   txt = 'Bot is restarting...'
   chatID = update.message.chat_id
   bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
   #update.message.reply_text('Bot is restarting...')
   Thread(target=stop_and_restart).start()



def call_delete(bot, job):
   chatID = job.context['chat']['id']
   msgID = job.context['message_id']
   bot.delete_message(chatID,msgID)


def callback_minute(bot, job):
   M = bot.send_message(chat_id='3875655',
                        text='One message every minute')
   J.run_once(call_delete, 20, context=M)


def send_picture(bot, chatID, job_queue, pic, msg='', t=3600, delete=True):
   #print('Sending',pic)
   photo = open(pic, 'rb')
   M = bot.send_photo(chatID, photo, 
                      caption=msg,
                      timeout=300,
                      parse_mode='Markdown')
   if delete: job_queue.run_once(call_delete, t, context=M)


def callback_30(bot, job):
   bot.send_message(chat_id=chatID,
                            text='A single message with 30s delay')


def callback_8(bot, job):
   print('Starting automatic broadcast 8')
   to_send = []
   for f in files:
      h = f.split('.')[-2]
      if h in ['0900','1200','1700','1900']:
         to_send.append(f)
         txt = 'Surface wind at *%s:%s*\n'%(h[:2],h[-2:])
         txt += 'For more information go to:\n'
         txt += ' http://raspuri.mooo.com/RASP/index.php'
         send_picture(bot, chatID, J, f, msg=txt, t=3600, delete=True)
         #send_picture(bot, chatID, J, f, msg=txt, t=3*3600, delete=True)

def callback_12(bot, job):
   print('Starting automatic broadcast 12')
   to_send = []
   for f in files:
      h = f.split('.')[-2]
      if h in ['1200','1700','1900']:
         to_send.append(f)
         txt = 'Surface wind at *%s:%s*\n'%(h[:2],h[-2:])
         txt += 'For more information go to:\n'
         txt += ' http://raspuri.mooo.com/RASP/index.php'
         send_picture(bot, chatID, J, f, msg=txt, t=3600, delete=True)

def callback_18(bot, job):
   print('Starting automatic broadcast 18')
   to_send = []
   for f in files:
      h = f.split('.')[-2]
      if h in ['1200','1700','1900']:
         to_send.append(f)
         txt = 'Surface wind at *%s:%s*\n'%(h[:2],h[-2:])
         txt += 'For more information go to:\n'
         txt += ' http://raspuri.mooo.com/RASP/index.php'
         send_picture(bot, chatID, J, f, msg=txt, t=3600, delete=True)


# Start Bot
token, chatID = CR.get_credentials()
U = Updater(token=token)
D = U.dispatcher
J = U.job_queue

## Add Handlers
# Start
D.add_handler(CommandHandler('start', start))

# Re-Load
D.add_handler(CommandHandler('reload', restart))

# Stop
D.add_handler(CommandHandler('stop', stop))

# Hola
import tool
D.add_handler(CommandHandler('fcst', tool.fcst, pass_args=True, pass_job_queue=True))


#J.run_daily(callback_8,  dt.time(7, 30))
J.run_daily(callback_8,  dt.time(16,58))
J.run_daily(callback_12, dt.time(12,45))
J.run_daily(callback_18, dt.time(18,15))


DATA = '/home/n03l/Documents/RASP'
now = dt.datetime.now()
folder = DATA+'/SC2/FCST/'+now.strftime('%Y/%m/%d')
files = os.popen('ls %s/new*.jpg'%(folder)).read().strip().splitlines()


U.start_polling()
