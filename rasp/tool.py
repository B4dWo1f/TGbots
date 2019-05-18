#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as dt

def call_delete(bot, job):
   chatID = job.context['chat']['id']
   msgID = job.context['message_id']
   bot.delete_message(chatID,msgID)

def send_picture(bot, chatID, job_queue, pic, msg='', t=60,delete=True):
   photo = open(pic, 'rb')
   M = bot.send_photo(chatID, photo, caption=msg,timeout=300)
   if delete: job_queue.run_once(call_delete, t, context=M)


def fcst(bot,update,job_queue,args):
   """ echo-like service to check system status """
   chatID = update.message.chat_id
   #salu2 = ['What\'s up?', 'Oh, hi there!', 'How you doin\'?', 'Hello!']
   #txt = choice(salu2)
   dates = [dt.datetime.strptime(d,'%d/%m/%Y-%H:%M') for d in args]
   try: dates = [dt.datetime.strptime(d,'%d/%m/%Y-%H:%M') for d in args]
   except ValueError:
      txt = 'Sorry, I didn\'t understand\n'
      txt += 'Usage: /fcst %d/%m/%Y-%H:%M\n'
      txt += 'ex: /fcst 18/05/2019-13:00'
      bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
      return
   for d in dates:
      f = '/home/n03l/Documents/RASP/SC2/FCST/' + d.strftime('%Y/%m/%d/')
      f += 'new_sfcwind.%s.jpg'%(d.strftime('%H00'))
      txt = 'Surface wind for %s'%(d.strftime('%d/%m/%Y-%H:%M'))
      send_picture(bot, chatID, job_queue, f, msg=txt, t=300,delete=True)

   #M = bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
#   job_queue.run_once(call_delete, 60, context=M)

