#!/usr/bin/env python3
import os
from flask import Flask, request
import telepot

import roll_dw

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

app = Flask(__name__)
TOKEN = os.environ['PP_BOT_TOKEN']
SECRET = '/bot' + TOKEN
URL = 'https://shrouded-meadow-82782.herokuapp.com'

UPDATE_QUEUE = Queue()
BOT = telepot.Bot(TOKEN)

def on_chat_message(msg):
    roll_dw.handle(msg)

roll_dw.bot = BOT
print("starting message loop")
BOT.message_loop({'chat': on_chat_message}, source=UPDATE_QUEUE)  # take updates from queue
print("message loop started")

@app.route(SECRET, methods=['GET', 'POST'])
def pass_update():
    UPDATE_QUEUE.put(request.data)  # pass update to bot
    return 'OK'

BOT.setWebhook(URL + SECRET)
print("webhook set to", URL+SECRET)
