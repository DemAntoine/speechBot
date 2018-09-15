# -*- coding: utf-8 -*-
# !/usr/bin/python

import boto3
from contextlib import closing

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import sys
from classes import *
import os

KEY = sys.argv[1]
print('key ' + KEY[:8] + '... successfully used')

logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

client = boto3.client('polly')
tracks_dir = '/home/ec2-user/test'


def testmp3(bot, update):
    full_name = os.path.join(tracks_dir, "polly-boto.mp3")
    track = open(full_name, 'rb')
    bot.sendAudio(chat_id=update.message.chat_id, audio=track)


def speech(bot, update):
    text = update.message.text
    track_count = len(os.listdir(tracks_dir))

    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        TextType='text',
        VoiceId='Maxim'
    )

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = str(track_count) + " track-boto.mp3"

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
    bot.sendMessage(chat_id=update.message.chat_id, text='тест. працює <b>ніби</b>', parse_mode=ParseMode.HTML)


def main():
    updater = Updater(KEY)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(filter_testmp3, testmp3))
    dispatcher.add_handler(MessageHandler(Filters.text, speech))
    dispatcher.add_handler(CommandHandler("start", start_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
