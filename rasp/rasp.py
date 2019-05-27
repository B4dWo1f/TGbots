#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import credentials as CR
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from threading import Thread
import datetime as dt
import tool
import sys
import os
here = os.path.dirname(os.path.realpath(__file__))

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s:%(levelname)s - %(message)s',
                    datefmt='%Y/%m/%d-%H:%M:%S',
                    filename=here+'/main.log', filemode='w')

LG = logging.getLogger('main')

Bcast_chatID = '-230660894'   # grupo
Bcast_chatID = '3875655'      # private


def start(bot, update):
   txt = "I'm a bot, please talk to me!"
   bot.send_message(chat_id=update.message.chat_id, text=txt)

def shutdown():
   U.stop()
   U.is_idle = False

@CR.restricted
def stop(bot, update):
   chatID = update.message.chat_id
   txt = 'I\'ll be shutting down\nI hope to see you soon!'
   bot.send_message(chatID, text=txt, parse_mode='Markdown')
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
   Thread(target=stop_and_restart).start()



def broadcast(bot, job):
   """ Broadcast information to a given chat """
   LG.info('Starting automatic 12:00 broadcast')
   now = dt.datetime.now()
   tday = now.date()
   if now.hour == 7: hours = [9,12,17,19]
   elif now.hour == 12: hours = [12,17,19]
   elif now.hour == 18: hours = [17,19]
   elif now.hour == 21: raise
   else: raise
   for h in hours:
      d = dt.datetime.combine(tday, dt.time(h, 0))
      LG.info('Broadcasting forecast for '+d.strftime('%H:%M'))
      f = tool.locate(d, 'sfcwind')
      txt = 'Surface wind at *%s*\n'%(d.strftime('%H:%M'))
      txt += 'For more information go to:\n'
      txt += ' http://raspuri.mooo.com/RASP/index.php'
      tool.send_picture(bot, Bcast_chatID, J, f, msg=txt,
                                            t=3600, delete=True, dis_notif=True)


# Start Bot
token = CR.get_credentials('rasp.token')
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
# Forecast
D.add_handler(CommandHandler('fcst', tool.fcst, pass_args=True, pass_job_queue=True))
# Sounding
D.add_handler(CommandHandler('sounding', tool.sounding, pass_args=True, pass_job_queue=True))


J.run_daily(broadcast, dt.time(7,30))
J.run_daily(broadcast, dt.time(12,45))
J.run_daily(broadcast, dt.time(18,15))


U.start_polling()
