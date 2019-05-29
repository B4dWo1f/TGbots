#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from telegram import ChatAction, ParseMode
import datetime as dt
import re
import os
HOME = os.getenv('HOME')

def call_delete(bot, job):
   chatID = job.context['chat']['id']
   msgID = job.context['message_id']
   bot.delete_message(chatID,msgID)

def send_picture(bot, chatID, job_queue, pic, msg='',
                 t=60,delete=True,dis_notif=False):
   """
    Send a picture and, optionally, remove it locally/remotely (rm/delete)
    pic = photo to send
    msg = caption of the picture
    t = time to wait to delete the remote picture
    delete = remove remote file t seconds after sending
    dis_notif = Disable sound notification
   """
   if pic[:4] == 'http': photo = pic
   else: photo = open(pic, 'rb')  # TODO raise and report if file not found
   bot.send_chat_action(chat_id=chatID, action=ChatAction.UPLOAD_PHOTO)
   M = bot.send_photo(chatID, photo, caption=msg,
                              timeout=300, disable_notification=dis_notif,
                              parse_mode=ParseMode.MARKDOWN)
   if delete: job_queue.run_once(call_delete, t, context=M)


def parse_date(date):
   try:
      pattern = r'([ ^\W\w\d_ ]*) (\S+)'
      match = re.search(pattern, date)
      day,time = match.groups()
      try:
         pattern = r'(\S+):(\S+)'
         match = re.search(pattern, time)
         h,m = (match.groups())
         m = 0
      except AttributeError:
         h = time
         m = 0
      h = int(h)
      m = int(m)
      shifts = {'hoy':0, 'mañana':1, 'pasado':2, 'al otro':3}
      delta = dt.timedelta(days=shifts[day])
      now = dt.datetime.now()
      date = now+delta
      return date.replace(hour=h, minute=m, second=0, microsecond=0)
   except: raise


def locate(date,prop):
   UTCshift = dt.datetime.now()-dt.datetime.utcnow()
   utcdate = date - UTCshift
   now = dt.datetime.utcnow()
   day = dt.timedelta(days=1)
   if   utcdate.date() == now.date(): fol = 'SC2'
   elif utcdate.date() == now.date()+day: fol = 'SC2+1'
   elif utcdate.date() == now.date()+2*day: fol = 'SC4+2'
   elif utcdate.date() == now.date()+3*day: fol = 'SC4+3'
   else: raise
   fname  = HOME+'/Documents/RASP/PLOTS/w2/%s/'%(fol)
   fname += utcdate.strftime('%Y/%m/%d/%H00')
   fname += '_%s.jpg'%(prop)
   return fol,fname


def fcst(bot,update,job_queue,args):
   """ echo-like service to check system status """
   chatID = update.message.chat_id
   d = ' '.join(args)
   #dates = [dt.datetime.strptime(d,'%d/%m/%Y-%H:%M') for d in args]
   try: date = dt.datetime.strptime(d,'%d/%m/%Y-%H:%M')
   except ValueError: date = parse_date(d)
   except:
      txt = 'Sorry, I didn\'t understand\n'
      txt += 'Usage: /fcst %d/%m/%Y-%H:%M\n'
      txt += '       /fcst [hoy/mañana/pasado/al otro] %H\n'
      txt += '       /fcst [hoy/mañana/pasado/al otro] %H:%M\n'
      txt += 'ex: /fcst 18/05/2019-13:00\n'
      txt += '    /fcst mañana 13:00\n'
      txt += '    /fcst al otro 14'
      bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
      return
   _,f = locate(date, 'sfcwind')
   txt = 'Surface wind for %s'%(date.strftime('%d/%m/%Y-%H:%M'))
   send_picture(bot, chatID, job_queue, f, msg=txt, t=30,delete=True)


def sounding(bot,update,job_queue,args):
   """ echo-like service to check system status """
   places = {'arcones': 1, 'bustarviejo': 2, 'cebreros': 3, 'abantos': 4,
             'piedrahita': 5, 'pedro bernardo': 6, 'lillo': 7,
             'fuentemilanos': 8, 'candelario': 10, 'pitolero': 11,
             'pegalajar': 12, 'otivar': 13}
   place = args[0]
   date = ' '.join(args[1:])
   index = places[place]
   chatID = update.message.chat_id
   try: date = dt.datetime.strptime(date,'%d/%m/%Y-%H:%M')
   except ValueError: date = parse_date(date)
   except:
      txt = 'Sorry, I didn\'t understand\n'
      txt += 'Usage: /sounding {place} %d/%m/%Y-%H:%M\n'
      txt += 'ex: /sounding Arcones 18/05/2019-13:00'
      bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
      return
   fmt = '%d_%m_%Y_%H_%M'
   #f = HOME + '/Documents/RASP/SC2/FCST/' + date.strftime('%d_%m_%Y_%H_%M')
   #f += '.sounding%s.w2.png'%(index)
   txt = "Sounding for *%s* at *%s*"%(place.capitalize(), date.strftime(fmt))
   fol,_ = locate(date,'')
   H = date.strftime('%H%M')
   url_picture = f'http://raspuri.mooo.com/RASP/'
   url_picture += f'{fol}/FCST/sounding{index}.curr.{H}lst.w2.png'
   send_picture(bot, chatID, job_queue, url_picture, msg=txt, t=30,delete=True)


## Auxiliary ###################################################################
from random import choice
def hola(bot, update):
   """ echo-like service to check system status """
   chatID = update.message.chat_id
   salu2 = ['What\'s up?', 'Oh, hi there!', 'How you doin\'?', 'Hello!']
   txt = choice(salu2)
   M = bot.send_message(chatID, text=txt, parse_mode='Markdown')
