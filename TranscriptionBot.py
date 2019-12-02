import logging
import os
import subprocess
import GoogleSpeechToText as Trans

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

lang = 'en-IN'

def voice(update, context):
    """Send a audio command /start is issued."""
    voice = update.message.voice
    chat_id = str(update.message.chat_id)
    message_id = str(update.message.message_id)
    ##chat_id = str(update.message.
    voiceFile = voice.get_file()
    voice_file_ogg = "voice-" + message_id + chat_id + ".ogg"
    interim_ogg_file = "temp-" + voice_file_ogg
    voice_file_wav = "voice-" + message_id + chat_id + ".wav"
    voiceFile.download(voice_file_ogg)
    subprocess.run(
        ["ffmpeg.exe", "-i", voice_file_ogg, "-c:a", "libvorbis", "-ab", "32k", "-ar", "16000", interim_ogg_file])
    subprocess.run(["ffmpeg.exe", "-i", interim_ogg_file, voice_file_wav])
    transcribed_text = Trans.transcribe(voice_file_wav, lang)
    update.message.reply_text(transcribed_text)
    os.remove(voice_file_wav)
    os.remove(voice_file_ogg)
    os.remove(interim_ogg_file)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Dubakoor is your speech to text converter for 120 languages. Record a '
                              'voice message and try how Dubakoor gives you results'
                              'Selections : /language - To select the language ')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def language(update, context):
    keyboard = [[InlineKeyboardButton("English", callback_data='en-US'),
                 InlineKeyboardButton("Tamil", callback_data='ta-IN')],

                [InlineKeyboardButton("Hindi", callback_data='hi-IN'),
                InlineKeyboardButton("French", callback_data='fr-FR')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose the Language :', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))
    global lang
    lang = query.data


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    updater = Updater(telegram_bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("Language",language))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))


    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.voice, voice))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
