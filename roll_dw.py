#!/usr/bin/env python3
from roll_parser import parse
from roller import roll, count
import telepot
from traceback import print_exc
from time import sleep
import os


COMMANDS = ['/р', '/r', '/roll', '/r@roll_dw_bot', '/roll@roll_dw_bot']


def mystr(item):
    if type(item) is tuple and len(item) == 1:
        return '('+str(item[0])+')'
    return str(item)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text' or 'forward_from' in msg:
        return
    for command in reversed(COMMANDS):
        if msg['text'].startswith(command):
            expression = msg['text'][len(command):]
            break
    else:
        return
    #print("Command:", msg['text'])
    print(expression)
    try:
        tokens, reason = parse(expression)
        print(expression, tokens, reason)
        rolled = roll(tokens)
        result = count(rolled)
        print(tokens)
        if reason:
            reason += '\n'
        bot.sendMessage(chat_id, '🎲 %s%s -> %s = <b>%d</b>'
                        % (reason, ' '.join(tokens),
                           ' '.join(map(mystr, rolled)), result),
                        parse_mode='HTML')
    except Exception as e:
        print_exc()
        bot.sendMessage(chat_id, '‼ Какая-то хрень ‼')


if __name__ == '__main__':
    token = os.getenv('TOKEN')
    if token is None:
        with open("token.txt") as token_file:
            for line in token_file:
                key, value = line.split('=')
                if key.strip() == 'TOKEN':
                    token = value.strip()
    print(token)
    bot = telepot.Bot(token)
    bot.message_loop(handle)
    while True:
        sleep(100)
