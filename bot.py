# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
import info
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
from emoji import emojize



from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


notclick=0

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
vip=[441399484, 55888804]
games={}
skills=[]

games={}

timerss={}

ban=[]
timers=[]
pokeban=[]


client1=os.environ['database']
client=MongoClient(client1)
db=client.pokewars
users=db.users
chats=db.chats


symbollist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я',
           '1','2','3','4','5','6','7','8','9','0']


def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)

@bot.message_handler(commands=['update'])
def spammm(m):
      if m.from_user.id==441399484:
          users.update_many({'money':{'$lt':0}},{'$set':{'money':0}})
#           x=users.find({})
 #          for ids in x:
  #           for idss in ids['pokemons']:
   #                 users.update_one({'id':ids['id']},{'$set':{'pokemons.'+idss+'.agility':1}})
          print('yes')


pokemonlist=['dildak','loshod','penis','zaluper','pikachu','pedro','bulbazaur','mayt','psyduck','zhopa','moxnatka','charmander',
            'diglet','golem','sidot','traxer', 'pizdak','tyxlomon','morzh','penisdetrov','gandonio','spermostrel']
basepokes=['dildak','loshod','penis','zaluper','zhopa']
elita=['pikachu','pedro','bulbazaur','psyduck', 'moxnatka','charmander',
            'diglet','golem','sidot','traxer','tyxlomon','morzh','penisdetrov','gandonio','spermostrel']


def huntt(id, chatid, pokemon):
    x=users.find_one({'id':id})
    earned=0
    users.update_one({'id':id},{'$set':{'pokemons.'+pokemon+'.hunting':0}})
    i=0
    chances=0
    win=0
    pokemon=x['pokemons'][pokemon]
    while i<pokemon['cool']:
        i+=1
        chances+=1
        z=random.randint(1,100)
        if z<=30+(pokemon['atk']*2):
            win+=1
            earned+=1
            z=random.randint(1,100)
            if z<=5+pokemon['agility']:
                earned+=1
            z=random.randint(1,100)
            if z<=pokemon['def']:
                i-=1
    z=random.randint(1,100)
    level='нет'
    if z<=10:
        earned=earned*pokemon['lvl']
        level='да'
    bot.send_message(chatid, 'Покемон '+pokemon['name']+' пользователя '+x['name']+' вернулся с охоты!\nПринесённое золото: '+str(earned)+'\n'+
                    'Количество попыток: '+str(chances)+'\nКоличество побед: '+str(win)+'\nУмножено ли золото на уровень покемона: '+level)
    users.update_one({'id':id},{'$inc':{'money':earned}})
   

@bot.message_handler(commands=['huntall'])
def huntallll(m):
 if m.from_user.id not in ban:
   x=banns(m.from_user.id, m.chat.id, m.from_user.first_name)
   if x==0:
        x=users.find_one({'id':m.from_user.id})
        if x!=None:
            for ids in x['pokemons']:
                  if x['pokemons'][ids]['hunting']==0:
                         users.update_one({'id':m.from_user.id},{'$set':{'pokemons.'+ids+'.hunting':1}})
                         t=threading.Timer(1800,huntt,args=[m.from_user.id, m.chat.id, ids])
                         t.start()
            bot.send_message(m.chat.id, 'Вы отправили всех готовых покемонов на охоту. Вернутся через 30 минут.')


@bot.message_handler(commands=['gold'])
def goldd(m):
     x=users.find_one({'id':m.from_user.id})
     if x!=None:
            bot.send_message(m.chat.id, m.from_user.first_name+', ваше золото: '+str(x['money']))


#@bot.message_handler(commands=['suckdick'])
#def suckdick(m):
# if m.from_user.id not in ban:
#   x=banns(m.from_user.id, m.chat.id, m.from_user.first_name)
#   if x==0:
#     try:
#        users.update_one({'id':m.from_user.id},{'$inc':{'money':-10}}) 
#        bot.send_message(m.chat.id, 'Вы успешно отсосали хуйца и потратили 10 монет.')
#     except:
#        pass


@bot.message_handler(commands=['extra'])
def extra(m):
   if m.from_user.id==441399484:
      gold=random.randint(1,100)
      if gold==1:
            gold='(золотой!!!) '
            pokemon='gold'
      else:
            gold=''
            pokemon=''
      i=0
      for ids in pokemons:
          i+=1   
      pokechance=40/(i*0.06)
      come=[]
      for ids in elita:
               come.append(ids)
      if len(come)>0:
        poke=random.choice(come)
      else:
        poke=random.choice(basepokes)
      kb=types.InlineKeyboardMarkup()
      kb.add(types.InlineKeyboardButton(text='Поймать', callback_data=pokemon+poke))
      m=bot.send_message(m.chat.id, 'Обнаружен *'+gold+'*покемон '+pokemons[poke]['name']+'! Его крутость: '+str(pokemons[poke]['cool'])+'. Жмите кнопку ниже, чтобы попытаться поймать.',reply_markup=kb,parse_mode='markdown')
      bot.pin_chat_message(m.chat.id, m.message_id, disable_notification=True)
                      

@bot.message_handler(commands=['hunt'])
def hunt(m):
 if m.from_user.id not in ban:
   x=banns(m.from_user.id, m.chat.id, m.from_user.first_name)
   if x==0:
    kb=types.InlineKeyboardMarkup()
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
     for ids in x['pokemons']:
      if x['pokemons'][ids]['hunting']!=1:
        kb.add(types.InlineKeyboardButton(text=pokemons[ids]['name'], callback_data=str(m.from_user.id)+' earn'+ids))
     bot.send_message(m.chat.id, m.from_user.first_name+', какого покемона вы хотите отправить на охоту?', reply_markup=kb)
    else:
           bot.send_message(m.chat.id, 'Ошибка!')
    
    
    
@bot.message_handler(commands=['give'])
def give(m):
  if m.from_user.id==441399484:
    x=m.text.split(' ')
    try:
      users.update_one({'id':m.reply_to_message.from_user.id}, {'$set':{'pokemons.'+x[1]:createpoke(x[1], 0)}})
      bot.send_message(m.chat.id, 'Покемон '+pokemons[x[1]]['name']+' успешно выдан!')
    except:
        pass
      

def banns(id, chatid, name):
    i=0
    for ids in timerss:
        if timerss[ids]['id']==id:
            i=1
    if i==0:
        print('1')
        timerss.update({id:{'id':id,
                          'messages':0}})
        t=threading.Timer(15, unwarn, args=[id])
        t.start()
    else:
        print('2')
        timerss[id]['messages']+=1
        if timerss[id]['messages']>=4:
            if id not in ban:
                      bot.send_message(chatid, 'Пользователь '+name+' много спамил и был заблокирован на 20 секунд.')
            ban.append(id)
            tt=threading.Timer(20, unbannn, args=[id])
            tt.start()
            print(ban)
            return 1
    return 0

def unwarn(id):
    try:
        del timerss[id]
        print('UNWARN!!!!!')
    except:
        pass


def unbannn(id):
      print('unbanlaunch')
      try:
        ban.remove(id)
        print('UNBAN!')
      except:
           pass

pokemons={'dildak':{'cool':10,
                   'name':'Дилдак',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'loshod':{'cool':25,
                   'name':'Лошод',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'penis':{'cool':37,
                   'name':'Пенис',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'zaluper':{'cool':13,
                   'name':'Залупер',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'pikachu':{'cool':100,
                   'name':'Пикачу',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'ruinmon':{'cool':-1,
                   'name':'Руинмон',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'pedro':{'cool':68,
                   'name':'Педро',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'bulbazaur':{'cool':112,
                   'name':'Бульбазавр',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'mayt':{'cool':41,
                   'name':'Мяут',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'psyduck':{'cool':131,
                   'name':'Псайдак',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'zhopa':{'cool':16,
                   'name':'Жопа',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'catchermon':{'cool':200,
                   'name':'Кэтчермон',
                   'lvl':1,
                   'atk':1,
                   'def':1},
          'moxnatka':{'cool':75,
                   'name':'Мохнатка'},
          'charmander':{'cool':82,
                   'name':'Чармандер'},
          'diglet':{'cool':49,
                   'name':'Диглет'},
          'golem':{'cool':125,
                   'name':'Голем'},
          'sidot':{'cool':56,
                   'name':'Сидот'},
          'traxer':{'cool':110,
                   'name':'Трахер'},
          'pizdak':{'cool':19,
                   'name':'Вонючий Пиздак'},
          'tyxlomon':{'cool':250,
                   'name':'Тухломон'},
          'morzh':{'cool':176,
                   'name':'Морж'},
          'penisdetrov':{'cool':425,
                   'name':'Пенис Детров'},
          'gandonio':{'cool':99,
                   'name':'Гандонио'},
          'spermostrel':{'cool':213,
                   'name':'Спермострел'}

          
}


@bot.message_handler(commands=['summon'])
def summon(m):
     y=users.find_one({'id':m.from_user.id})
     if y['money']>=100:
        x=random.randint(1,100)
        users.update_one({'id':y['id']},{'$inc':{'money':-100}})
        if x<=10:
           bot.send_message(m.chat.id, 'Вы потратили 100 монет. Вам удалось призвать покемона!!!')
           poke(m.chat.id)
        else:
           bot.send_message(m.chat.id, 'Вы потратили 100 монет. Вам не удалось призвать покемона.')
     else:
        bot.send_message(m.chat.id, 'Недостаточно золота!')
         


def poke(id):
      gold=random.randint(1,100)
      if gold==1:
            gold='(золотой!!!) '
            pokemon='gold'
      else:
            gold=''
            pokemon=''
      i=0
      for ids in pokemons:
          i+=1   
      pokechance=40/(i*0.06)
      come=[]
      for ids in elita:
            chance=pokechance/(pokemons[ids]['cool']*0.03)
            x=random.randint(1,100)
            if x<=chance:
                come.append(ids)
      if len(come)>0:
        poke=random.choice(come)
      else:
        poke=random.choice(elita)
      kb=types.InlineKeyboardMarkup()
      kb.add(types.InlineKeyboardButton(text='Поймать', callback_data=pokemon+poke))
      m=bot.send_message(id, 'Обнаружен *'+gold+'*покемон '+pokemons[poke]['name']+'! Его крутость: '+str(pokemons[poke]['cool'])+'. Жмите кнопку ниже, чтобы попытаться поймать.',reply_markup=kb,parse_mode='markdown')
      t=threading.Timer(random.randint(300,600),runpoke,args=[m.message_id,m.chat.id])
      t.start()
      timers.append('1')
      bot.pin_chat_message(m.chat.id, m.message_id, disable_notification=False)



def dailypoke(id):
      x=random.randint(600,3000)
      t=threading.Timer(x, dailypoke, args=[id])
      t.start()
      gold=random.randint(1,100)
      if gold==1:
            gold='(золотой!!!) '
            pokemon='gold'
      else:
            gold=''
            pokemon=''
      i=0
      for ids in pokemons:
          i+=1   
      pokechance=40/(i*0.06)
      come=[]
      for ids in pokemonlist:
            chance=pokechance/(pokemons[ids]['cool']*0.03)
            x=random.randint(1,100)
            if x<=chance:
                come.append(ids)
      if len(come)>0:
        poke=random.choice(come)
      else:
        poke=random.choice(basepokes)
      kb=types.InlineKeyboardMarkup()
      kb.add(types.InlineKeyboardButton(text='Поймать', callback_data=pokemon+poke))
      m=bot.send_message(id, 'Обнаружен *'+gold+'*покемон '+pokemons[poke]['name']+'! Его крутость: '+str(pokemons[poke]['cool'])+'. Жмите кнопку ниже, чтобы попытаться поймать.',reply_markup=kb,parse_mode='markdown')
      t=threading.Timer(random.randint(300,600),runpoke,args=[m.message_id,m.chat.id])
      t.start()
      timers.append('1')
      bot.pin_chat_message(m.chat.id, m.message_id, disable_notification=False)

def runpoke(mid,cid):
    if '1' in timers:
         medit('Покемон сбежал!', cid, mid)
         timers.remove('1')
    
            
                        
@bot.message_handler(commands=['cooltop'])
def cooltop(m):
    x=users.find({})


                        
@bot.message_handler(commands=['pokes'])
def pokesfgtd(m):
   if m.from_user.id not in ban:
     x=banns(m.from_user.id, m.chat.id, m.from_user.first_name)
     if x==0:
      x=users.find_one({'id':m.from_user.id})
      if x!=None:
        text=''
        for ids in x['pokemons']:
            if x['pokemons'][ids]['golden']==1:
                  text+='*Золотой* '
            text+=x['pokemons'][ids]['name']+' - крутость: '+str(x['pokemons'][ids]['cool'])+'\n'
        bot.send_message(m.chat.id, 'Ваши покемоны:\n\n'+text,parse_mode='markdown')
      else:
            bot.send_message(m.chat.id, 'Сначала напишите в чат что-нибудь (не команду!).')
      
    
def rebootclick():
    global notclick
    notclick=0
           
           
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
 global notclick
 if notclick==0:
  if 'earn' not in call.data:
   notclick=1
   t=threading.Timer(3,rebootclick)
   t.start()
   if call.from_user.id not in pokeban:
    x=users.find_one({'id':call.from_user.id})
    if x!=None:
        text=call.data
        golden=0
        if call.data[0]=='g' and call.data[1]=='o' and call.data[2]=='l' and call.data[3]=='d':
            text=call.data[4:]
            golden=1
        chancetocatch=(100*(x['chancetocatch']+1))/(pokemons[text]['cool']*0.03)
        z=random.randint(1,100)
        if z<=chancetocatch:
         i=0
         for ids in x['pokemons']:
            if x['pokemons'][ids]['code']==text:
                i=1
         if i!=1:
            givepoke(call.data, call.message.chat.id, call.message.message_id, call.from_user.first_name, call.from_user.id)
            try:
                      timers.remove('1')
            except:
                      pass
         else:
            if golden==1 and x['pokemons'][text]['golden']==0:
                  users.update_one({'id':call.from_user.id}, {'$set':{'pokemons.'+text+'.golden':1}})
                  medit('Покемона *Золотой* '+pokemons[text]['name']+' поймал '+call.from_user.first_name+'! Данный покемон у него уже был, '+
                        'но обычный. Теперь он стал золотым!',call.message.chat.id, call.message.message_id, parse_mode='markdown')
                  timers.remove('1')
            else:
                  bot.answer_callback_query(call.id, 'У вас уже есть этот покемон!')
        else:
           pokeban.append(call.from_user.id)
           t=threading.Timer(60,unban,args=[call.from_user.id])
           t.start()
           bot.send_message(call.message.chat.id, 'Пользователю '+call.from_user.first_name+' не удалось поймать покемона!')
    else:
        bot.answer_callback_query(call.id, 'Сначала напишите в чат что-нибудь (не команду!).')
   else:
    bot.answer_callback_query(call.id, 'Подождите минуту для ловли следующего покемона!')
  else:
    text=call.data.split(' ')
    if int(text[0])==call.from_user.id:
      x=users.find_one({'id':call.from_user.id})
      text=text[1]
      text=text[4:]
      if x['pokemons'][text]['hunting']==0:
        users.update_one({'id':call.from_user.id},{'$set':{'pokemons.'+text+'.hunting':1}})
        medit('Вы отправили покемона '+pokemons[text]['name']+' на охоту. Он вернётся через пол часа.', call.message.chat.id, call.message.message_id)
        t=threading.Timer(1800,huntt,args=[call.from_user.id, call.message.chat.id, text])
        t.start()
      else:
           medit('Покемон уже на охоте!', call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, 'Это не ваше меню!')
             
def unban(id):
    try:
        pokeban.remove(id)
    except:
        pass


def givepoke(pokemon,id, mid, name, userid):
    golden=0
    if pokemon[0]=='g' and pokemon[1]=='o' and pokemon[2]=='l' and pokemon[3]=='d':
      z=len(pokemon)
      pokemon=pokemon[(z-(z-4)):]
      golden=1
    text=''
    if golden==1:
        text='*Золотой* '
    try:
            medit('Покемона '+text+pokemons[pokemon]['name']+' поймал '+name+'!',id, mid, parse_mode='markdown')
            users.update_one({'id':userid},{'$set':{'pokemons.'+pokemon:createpoke(pokemon,golden)}})
    except:
            pass  
 
@bot.message_handler(content_types=['text'])
def textt(m):
    if users.find_one({'id':m.from_user.id})==None:
      users.insert_one(createuser(m.from_user.id))
    x=chats.find_one({'id':m.chat.id})
    if x==None:
        chats.insert_one(createchat(m.chat.id))
    if users.find_one({'id':m.from_user.id})!=None:
           users.update_one({'id':m.from_user.id}, {'$set':{'name':m.from_user.first_name}})

   
def createpoke(pokemon, gold):
      return{'name':pokemons[pokemon]['name'],
             'code':pokemon,
             'cool':pokemons[pokemon]['cool'],
             'golden':gold,
             'lvl':1,
             'atk':1,
             'def':1,
             'agility':1,
             'hunting':0
            }

def createchat(id):
    return{'id':id
          }

def createuser(id):
      return{'id':id,
             'name':None,
             'pokemons':{},
             'chancetocatch':0,
             'money':0
            }
  
if True:
 try:
   print('7777')
   x=users.find({})
   for ids in x:
     for idss in ids['pokemons']:
        users.update_one({'id':ids['id']},{'$set':{'pokemons.'+idss+'.hunting':0}})
   t=threading.Timer(300,dailypoke,args=[-1001256539790])
   t.start()
   bot.polling(none_stop=True,timeout=600)
 except:
        print('!!! READTIME OUT !!!')           
        bot.stop_polling()
        time.sleep(1)
        check = True
        while check==True:
          try:
            bot.polling(none_stop=True,timeout=1)
            print('checkkk')
            check = False
          except (requests.exceptions.ConnectionError):
            time.sleep(1)
   
#if __name__ == '__main__':
 # bot.polling(none_stop=True)

#while True:
#    try:
  #      bot.polling()
 #   except:
  #      pass
#    time.sleep(0.1)
       
