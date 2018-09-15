# -*- coding: utf-8 -*-
# !/usr/bin/python

import boto3
from contextlib import closing
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import sys
from classes import *
import os

KEY = sys.argv[1]
print('key ' + KEY[:8] + '... successfully used')

logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

client = boto3.client('polly')
tracks_dir = '/home/ec2-user/speechBot/tracks'


# def testmp3(bot, update):
#     full_name = os.path.join(tracks_dir, "polly-boto.mp3")
#     track = open(full_name, 'rb')
#     bot.sendAudio(chat_id=update.message.chat_id, audio=track)


chosen_language = 'Maxim'


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
        with closing(response["AudioStream"]) as stream:
            output = tracks_dir + '/' + str(track_count) + " track-boto.mp3"

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    full_name = os.path.join(tracks_dir, str(track_count) + " track-boto.mp3")
    track = open(full_name, 'rb')

    bot.sendAudio(chat_id=update.message.chat_id, audio=track)


def start_command(bot, update):
    keyboard = [[InlineKeyboardButton('ENG 🇬🇧', callback_data='Brian')],
                [InlineKeyboardButton('GER 🇩🇪', callback_data='Hans')],
                [InlineKeyboardButton('RU 🇷🇺', callback_data='Maxim')],
                [InlineKeyboardButton('IT 🇮🇹', callback_data='Giorgio')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id, reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                    text='<b>Бот конвертує текст в аудіо. Зараз мова Російська, можеш вибрати іншу</b>')


def set_language(bot, update):
    global chosen_language
    chosen_language = update.callback_query.data
    if chosen_language == 'Brian':
        bot.editMessageText(
            text='Ти обрав <b>англійську</b>. Пиши боту текст, і він пришле аудіо англійською.',
            chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id,
            parse_mode=ParseMode.HTML)
    elif chosen_language == 'Hans':
        bot.editMessageText(
            text='Ти обрав <b>німецьку</b>. Пиши боту текст, і він пришле аудіо німецькою.',
            chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id,
            parse_mode=ParseMode.HTML)
    elif chosen_language == 'Maxim':
        bot.editMessageText(
            text='Ти обрав <b>російську</b>. Пиши боту текст, і він пришле аудіо російською.',
            chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id,
            parse_mode=ParseMode.HTML)
    elif chosen_language == 'Giorgio':
        bot.editMessageText(
            text='Ти обрав <b>італійську</b>. Пиши боту текст, і він пришле аудіо італійською.',
            chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id,
            parse_mode=ParseMode.HTML)


def main():
    updater = Updater(KEY)
    dispatcher = updater.dispatcher

    #dispatcher.add_handler(MessageHandler(filter_testmp3, testmp3))
    dispatcher.add_handler(MessageHandler(Filters.text, speech))
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CallbackQueryHandler(set_language))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
