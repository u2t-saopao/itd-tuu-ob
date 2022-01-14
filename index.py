#!/usr/bin/env python
# -- coding: utf-8 --
import time
import socketio
import eventlet
import eventlet.wsgi

from flask import Flask, request, abort, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage
)

sio = socketio.Server()
app = Flask(__name__)

line_bot_api = LineBotApi('2HXDSd8UG3mxBOboLxq15zE3JfUBFqn+2ThJauXxbWVm8ye7zCu5YNxSxOqin2ZDSJVzy65LGKWdGgxUNeppPtIyoLHcTl07xnCDh/kLRhC5b7kadxPEEVrGG48bK5T2XiFTJkzaWiHcZgj9M8KgbAdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('63c875ea8193fd83505c3bb150f3ca33') #Your Channel Secret

users = ['Uef2a83ec08dd0e0e55f8da7f07df192f','Uc59840c0335ea720214d1e41b8846ea2','Uc0471a13945e267150b756c181728dd8']

_state = 'J'

_timeon = "15:03"
_timeoff = "6:00"
_auto = False
_a = False

@app.route('/')
def data():
    global _state,_timeon,_timeoff,_auto,_a
    print time.strftime("%H:%M:%S")
    print _state
    if _auto:
        if time.strftime("%H:%M") == _timeon and _state == 'J' and not(_a):
            
            _state = 'Y'
            _a = True
        elif time.strftime("%H:%M") == _timeoff and _state == 'Y' and _a:
            _state = 'J'
            _a = False
    return jsonify(_state)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global _state,_timeon,_timeoff,_auto
    text = event.message.text #message from user
    profile = line_bot_api.get_profile(event.source.user_id) #get user profile
    print text
    print profile.user_id
    print time.strftime("%H:%M:%S")
    t = text.find(u'เวลา ')
    
    if profile.user_id in users:
        if t > -1 :
            m = text.split(u'เวลา ')
            
            m[1]=m[1].replace('.', ':')
            if u'เปิดไฟ' in m:
                
                _timeon = m[1]
                line_bot_api.reply_message(event.reply_token,TextMessage(text="ไฟเปิดที่เวลา "+str(m[1])+"นะคะ"))
                
                _auto =True
                print _timeon
                
            elif u'ปิดไฟ' in m:
                
                _timeoff = m[1]
                line_bot_api.reply_message(event.reply_token,TextMessage(text="ไฟปิดที่เวลา "+str(m[1])+"นะคะ"))
                
                _auto =True
                print _timeoff
                
            else:
                line_bot_api.reply_message(event.reply_token,TextMessage(text="ขออภัย ฉันไม่เข้าใจคำสั่ง"))
                
        else :
            if text == u'เปิดไฟ':
                
                if _state == 'Y':
                    line_bot_api.reply_message(event.reply_token,TextMessage(text="ไฟเปิดอยู่แล้วค่ะ"))
                else:
                    _state = 'Y'
                    line_bot_api.reply_message(event.reply_token,TextMessage(text="ไฟเปิดแล้วค่ะ"))
             #line_bot_api.reply_message(event.reply_token,TextMessage(text="ฟังชั่นนี้ยังไม่สามารถใช้งานได้"))
                 
                
            elif text == u'ปิดไฟ':
                
                if _state == 'J':
                    line_bot_api.reply_message(event.reply_token,TextMessage(text="ไฟปิดอยุ่แล้วค่ะ"))
                
                else:
                    _state = 'J'
                    line_bot_api.reply_message(event.reply_token,TextMessage(text="ไฟปิดแล้วค่ะ"))
                 #line_bot_api.reply_message(event.reply_token,TextMessage(text="ฟังชั่นนี้ยังไม่สามารถใช้งานได้"))
            
            elif text == u'สถานะ':
                
                if _state == 'J':
                    line_bot_api.reply_message(event.reply_token,TextMessage(text="ไฟปิดอยุ่ค่ะ"))
                    
                elif _state == 'Y':
                    line_bot_api.reply_message(event.reply_token,TextMessage(text="ไฟเปิดอยู่ค่ะ")) 
                    
                if _timeon != None:
                    line_bot_api.push_message(profile.user_id,TextMessage(text="ตั้งเวลาเปิดไฟไว้ที่ "+str(_timeon)+"นะคะ"))
                    #_auto = True
                    
                if _timeoff != None:
                    line_bot_api.push_message(profile.user_id,TextMessage(text="ตั้งเวลาปิดไฟไว้ที่ "+str(_timeoff)+"นะคะ"))
                    #_auto =True
                    
            elif text == u'ยกเลิกการตั้งค่า':
                
                _timeon = None
                _timeoff = None
                _auto = False
                
                line_bot_api.reply_message(event.reply_token,TextMessage(text="ยกเลิกตั้งเวลาเปิดปิดไฟแล้วนะคะ"))
                    
            else:
                line_bot_api.reply_message(event.reply_token,TextMessage(text="ขออภัย ฉันไม่เข้าใจคำสั่ง"))
    else:
        line_bot_api.reply_message(event.reply_token,TextMessage(text="คุณไม่สามารถใช้บริการได้"))
import os
if __name__ == "__main__":
    #app = socketio.Middleware(sio, app)
    #eventlet.wsgi.server(eventlet.listen(('', 8080)), app)
    app.run(host='0.0.0.0',port=os.environ['PORT'])