#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as dt

def location(bot, update):
   """Records the live location of the user"""
   message = None
   if update.edited_message:
      message = update.edited_message
   else:
      message = update.message
   now = dt.datetime.now()
   current_pos = (message.location.latitude, message.location.longitude)
   print(now,current_pos)

def callback_30(bot, job):
   bot.send_message(chat_id='3875655',
                    text='A single message with 30s delay')
