#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import threading
from base64 import b64decode as decode
from random import choice
import tools
import geoip
import check
from functools import wraps
import credentials as CR
import os
here = os.path.dirname(os.path.realpath(__file__))


## Action functions
def send_picture(bot,chatID,job_queue,pic,msg='This is your picture',rm=True,delete=True):
   photo = open(pic, 'rb')
   M = bot.send_photo(chatID, photo, caption=msg,timeout=50)
   if rm: os.system('rm %s'%(pic))
   if delete: job_queue.run_once(call_delete, 60, context=M)

def send_sound(bot,chatID,audio,msg='This is your picture',rm=True):
   mp3 = open(audio, 'rb')
   bot.send_audio(chatID, mp3, caption=msg,timeout=50)
   if rm: os.system('rm %s'%(audio))


## Callback functions
def hola(bot,update, job_queue):
   """ echo-like service to check system status """
   chatID = update.message.chat_id
   salu2 = ['What\'s up?', 'Oh, hi there!', 'How you doin\'?', 'Hello!']
   txt = choice(salu2)
   M = bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')
   job_queue.run_once(call_delete, 60, context=M)

def call_delete(bot, job):
   chatID = job.context['chat']['id']
   msgID = job.context['message_id']
   bot.delete_message(chatID,msgID)


def screen_lock(bot,update):
   """ Lock the computer """
   chatID = update.message.chat_id
   com = 'gnome-screensaver-command --lock'
   os.system(com)
   bot.send_message(chat_id=chatID, text='Screen locked',parse_mode='Markdown')

@CR.restricted
def screenshot(bot,update):
   """
   Take a screenshot and send it
   """
   chatID = update.message.chat_id
   pic = '/tmp/screenshot.png'
   com = 'scrot -z %s'%(pic)
   os.system(com)
   txt = 'Please be patient, this usually takes a few seconds'
   bot.send_message(chatID, text=txt,parse_mode='Markdown')
   send_picture(bot,chatID,pic,msg='Here it is the screenshot')

@CR.restricted
def picture(bot,update,job_queue):
   """
   Take a picture from the webcam and send it
   ffmpeg args:
   -y: automatic overwrite
   -v 0: quiet, verbose = 0
   """
   chatID = update.message.chat_id
   devices = os.popen('ls /dev/video*').read().strip().splitlines()
   txt = 'Taking a picture from %s devices'%(len(devices))
   bot.send_message(chatID, text=txt,parse_mode='Markdown')
   for dev in devices:
      pic = '/tmp/out.jpg'
      com = 'ffmpeg -y -v 0 -f video4linux2 -s 640x480 -i %s -ss 0:0:5'%(dev)
      com += ' -frames 1 %s'%(pic)
      os.system(com)
      send_picture(bot,chatID,job_queue,pic,msg='Picture from %s'%(dev),delete=True)

@CR.restricted
def sound(bot,update):
   """
   Work in progress
   TODO: send mp3 file
   """
   chatID = update.message.chat_id
   f = '/tmp/recording.mp3'
   com = 'sox -t alsa default %s silence 1 0.1 1%% 1 1.0 5%%'%(f)
   os.system(com)
   send_sound(bot,chatID,f)
   bot.send_message(chatID, text='Recorded sound',parse_mode='Markdown')

def whereRyou(bot,update):
   """ Return the IP where the bot is running """
   chatID = update.message.chat_id
   ip = tools.get_public_IP()
   txt = ''
   for l in str(geoip.analyze_IP(ip)).splitlines():
      txt += l.strip() + '\n'
   bot.send_message(chatID, text=txt[:-1],parse_mode='Markdown')

def whoSthere(bot,update):
   """ Return all the devices connected to the bot's network """
   chatID = update.message.chat_id
   txt = 'Hold on, it might take a second'
   bot.send_message(chatID, text=txt,parse_mode='Markdown')
   txt = ''
   for d in check.check_network():
      l = ''
      for ld in str(d).strip().splitlines():
         l += ld.strip() + '\n'
      l = l.strip().replace('*',' ').replace('_',' ')
      l = l.replace('(','(*').replace(')','*)')
      txt += l + '\n--\n'
   bot.send_message(chatID, text=txt[:-2],parse_mode='Markdown')

def whoami(bot,update):
   """ echo-like service to check system status """
   chatID = update.message.chat_id
   ch = update.message['chat']
   txt = 'username: %s %s\n'%(ch['first_name'],ch['last_name'])
   txt += 'username: %s \n'%(ch['username'])
   txt += 'id: %s'%(ch['id'])
   bot.send_message(chat_id=chatID, text=txt, parse_mode='Markdown')

def help_msg(bot,update):
   """ Display this help message """
   chatID = update.message.chat_id
   txt = 'These are the available commands:\n'
   txt += '- *hola*: Echo service to check on service status\n'
   txt += '- *lock*: Lock the computer\n'
   txt += '- *picture*: Take a picture from the webcam and send it\n'
   txt += '- *screenshot*: Take a screenshot and send it\n'
   txt += '- *sound*: Record sound from the microphone and send it\n'
   txt += '- *where*: Return the IP where the bot is running\n'
   txt += '- *whothere*: Show the devices connected to the bot\'s network\n'
   txt += '- *help*: Display this help message\n'
   txt += '- *stop*: Stop the bot'
   bot.send_message(chatID, text=txt,parse_mode='Markdown')
