# -*- coding: utf-8 -*-
import boto3
from contextlib import closing
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import sys
import os
from config import log
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, NetworkError)

KEY = sys.argv[1]
aws_access_key_id = sys.argv[2]
aws_secret_access_key = sys.argv[3]
print('key... ' + KEY[-6:] + ' successfully used')

client = boto3.client('polly',
                      region_name='us-east-2',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

tracks_dir = os.path.join(os.getcwd(), 'tracks')

default_lang = 'Maxim'
langs_arr = {}
language_keys = {'Brian': 'англійську', 'Hans': 'німецьку', 'Maxim': 'російську', 'Giorgio': 'італійську', }


def speech(update, context):
    text = update.message.text
    track_count = len(os.listdir(tracks_dir))

    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        TextType='text',
        VoiceId=langs_arr.get(update.effective_user.id, 'Maxim')
    )

    if "AudioStream" in response:
        try:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(tracks_dir, str(track_count) + " track-boto.mp3")
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
                    track = open(output, 'rb')
            context.bot.sendAudio(chat_id=update.message.chat_id, audio=track)
        except IOError as error:
            print(error)
            sys.exit(-1)


def start_command(update, context):
    log.info(f'user_id: {update.effective_user.id} name: {update.effective_user.full_name}')
    keyboard = [[InlineKeyboardButton('ENG 🇬🇧', callback_data='Brian')],
                [InlineKeyboardButton('GER 🇩🇪', callback_data='Hans')],
                [InlineKeyboardButton('RU 🇷🇺', callback_data='Maxim')],
                [InlineKeyboardButton('IT 🇮🇹', callback_data='Giorgio')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    current_lang = language_keys.get(langs_arr.get(update.effective_user.id, 'Maxim'))

    context.bot.sendMessage(chat_id=update.message.chat_id, reply_markup=reply_markup, parse_mode=ParseMode.HTML,
                            text=f'Бот конвертує текст в аудіо. '
                            f'Зараз обрано <b>{current_lang}</b> мову, можеш вибрати іншу')


def set_language(update, context):
    log.info(f'user_id: {update.effective_user.id} name: {update.effective_user.full_name}')
    chosen_language = update.callback_query.data
    langs(update, context, chosen_language)
    context.bot.editMessageText(
        text=f'Ти обрав <b>{language_keys[chosen_language]}</b>. Пиши текст, і бот пришле аудіо цією мовою.',
        chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML)


def langs(update, context, chosen_language):
    langs_arr[update.effective_user.id] = chosen_language


def catch_err(update, context, error):
    """handle all telegram errors end send report"""
    log.info(f'user_id: {update.effective_user.id} name: {update.effective_user.username} {type(error)}')
    try:
        raise error
    except Unauthorized:
        context.bot.sendMessage(chat_id=3680016,
                                text=f'ERROR:\n {error}\n type {type(error)}\n user_id {update.effective_user.id}')
    except BadRequest:
        try:
            context.bot.sendMessage(chat_id=3680016, text=f'ERROR:\n {error}\n type {type(error)}')
        except:
            log.info('*' * 100)
    except (TimedOut, NetworkError, TelegramError):
        context.bot.sendMessage(chat_id=3680016,
                                text=f'ERROR:\n {error}\n type {type(error)}\n user_id {update.effective_user.id}')
        context.bot.sendPhoto(chat_id=update.effective_user.id, photo=open(os.path.join('img', 'error.jpg'), 'rb'),
                              caption=f'Щось пішло не так... Спробуйте ще раз.')


def main():
    updater = Updater(KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text, speech))
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CallbackQueryHandler(callback=set_language,
                                                pattern='^Brian$|^Hans$|^Maxim$|^Giorgio$'))
    dispatcher.add_error_handler(catch_err)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
