# -*- coding: utf-8 -*-
# !/usr/local/bin/python3

import boto3
from contextlib import closing
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import sys
import os

KEY = sys.argv[1]
print('key ' + KEY[:8] + '... successfully used')

logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

client = boto3.client('polly')
tracks_dir = '/home/ec2-user/speechBot/tracks'
chosen_language = 'Maxim'
language_keys = {'Brian': 'англійську', 'Hans': 'німецьку', 'Maxim': 'російську', 'Giorgio': 'італійську', }


def speech(bot, update):
    text = update.message.text
    track_count = len(os.listdir(tracks_dir))

    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        TextType='text',
        VoiceId=chosen_language
    )

    if "AudioStream" in response:
        global output
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(tracks_dir, str(track_count) + " track-boto.mp3")
            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)

    track = open(output, 'rb')
    bot.sendAudio(chat_id=update.message.chat_id, audio=track)


def start_command(bot, update):
    keyboard = [[InlineKeyboardButton('ENG 🇬🇧', callback_data='Brian')],
                [InlineKeyboardButton('GER 🇩🇪', callback_data='Hans')],
                [InlineKeyboardButton('RU 🇷🇺', callback_data='Maxim')],
                [InlineKeyboardButton('IT 🇮🇹', callback_data='Giorgio')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id, reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                    text='<b>Бот конвертує текст в аудіо. Зараз обрано {} мову, можеш вибрати іншу</b>'
                    .format(language_keys[chosen_language]))


def set_language(bot, update):
    global chosen_language
    chosen_language = update.callback_query.data
    bot.editMessageText(
        text='Ти обрав <b>{}</b>. Пиши текст, і бот пришле аудіо цією мовою.'.format(language_keys[chosen_language]),
        chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML)


def main():
    updater = Updater(KEY)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text, speech))
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CallbackQueryHandler(set_language))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
