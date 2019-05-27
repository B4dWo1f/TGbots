#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime as dt

def call_delete(bot, job):
   chatID = job.context['chat']['id']
   msgID = job.context['message_id']
   bot.delete_message(chatID,msgID)

def send_picture(bot, chatID, job_queue, pic, msg='',
                 t=60,delete=True,dis_notif=False):
   if pic[:4] == 'http': photo = pic
   else: photo = open(pic, 'rb')  # TODO raise and report if file not found
   M = bot.send_photo(chatID, photo, caption=msg,
                                  timeout=300, disable_notification=dis_notif)
   if delete: job_queue.run_once(call_delete, t, context=M)


def fcst(bot,update,job_queue,args):
   """ echo-like service to check system status """
   chatID = update.message.chat_id
   dates = [dt.datetime.strptime(d,'%d/%m/%Y-%H:%M') for d in args]
   try: dates = [dt.datetime.strptime(d,'%d/%m/%Y-%H:%M') for d in args]
   except ValueError:
      txt = 'Sorry, I didn\'t understand\n'
      txt += 'Usage: /fcst %d/%m/%Y-%H:%M\n'
      txt += 'ex: /fcst 18/05/2019-13:00'
      bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
      return
   for d in dates:
      _,f = locate(d, 'sfcwind')
      txt = 'Surface wind for %s'%(d.strftime('%d/%m/%Y-%H:%M'))
      send_picture(bot, chatID, job_queue, f, msg=txt, t=30,delete=True)

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
   fname  = '/home/n03l/Documents/RASP/PLOTS/w2/%s/'%(fol)
   fname += utcdate.strftime('%Y/%m/%d/%H00')
   fname += '_%s.jpg'%(prop)
   return fol,fname


def sounding(bot,update,job_queue,args):
   """ echo-like service to check system status """
   places = {'arcones': 1, 'bustarviejo': 2, 'cebreros': 3, 'abantos': 4,
             'piedrahita': 5, 'pedro bernardo': 6, 'lillo': 7,
             'fuentemilanos': 8, 'candelario': 10, 'pitolero': 11,
             'pegalajar': 12, 'otivar': 13}
   place, date = args
   index = places[place]
   chatID = update.message.chat_id
   try: date = dt.datetime.strptime(date,'%d/%m/%Y-%H:%M')
   except ValueError:
      txt = 'Sorry, I didn\'t understand\n'
      txt += 'Usage: /sounding {place} %d/%m/%Y-%H:%M\n'
      txt += 'ex: /sounding Arcones 18/05/2019-13:00'
      bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
      return
   f = '/home/n03l/Documents/RASP/SC2/FCST/' + date.strftime('%d_%m_%Y_%H_%M')
   f += '.sounding%s.w2.png'%(index)
   txt = 'Sounding for %s at %s'%(place, date.strftime('%d/%m/%Y-%H:%M'))
   fol,_ = locate(date,'')
   H = date.strftime('%H%M')
   url_picture = f'http://raspuri.mooo.com/RASP/'
   url_picture += f'{fol}/FCST/sounding{index}.curr.{H}lst.w2.png'
   send_picture(bot, chatID, job_queue, url_picture, msg=txt, t=30,delete=True)


#def cape(bot,update,job_queue,args):
#   """ echo-like service to check system status """
#   chatID = update.message.chat_id
#   #salu2 = ['What\'s up?', 'Oh, hi there!', 'How you doin\'?', 'Hello!']
#   #txt = choice(salu2)
#   dates = [dt.datetime.strptime(d,'%d/%m/%Y-%H:%M') for d in args]
#   try: dates = [dt.datetime.strptime(d,'%d/%m/%Y-%H:%M') for d in args]
#   except ValueError:
#      txt = 'Sorry, I didn\'t understand\n'
#      txt += 'Usage: /fcst %d/%m/%Y-%H:%M\n'
#      txt += 'ex: /fcst 18/05/2019-13:00'
#      bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
#      return
#   for d in dates:
#      f = '/home/n03l/Documents/RASP/SC2/FCST/' + d.strftime('%Y/%m/%d/')
#      f += 'new_sfcwind.%s.jpg'%(d.strftime('%H00'))
#      txt = 'Surface wind for %s'%(d.strftime('%d/%m/%Y-%H:%M'))
#      send_picture(bot, chatID, job_queue, f, msg=txt, t=300,delete=True)
