from telegram.ext import Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler
from telegram.ext import MessageHandler, Filters
from PyDictionary import PyDictionary
import logging
import os
from OxfordDictionariesAPI import get_meaning
from bot_storage import Storage

# dic setup
dictionary = PyDictionary

# print(dictionary.meaning("sultry")) # - test



storages = {}

customDict = Storage(storage_name = "Tg_bot_dictionary") # create my custom dictionary
Ideas = Storage(storage_name = "Ideas")

# names for function list_storage
storages["dict"] = customDict
storages["ideas"] = Ideas


last_meaning = "" #variable to store last request to get meaning function


# proxy setting ##################
proxy = 'http://217.61.106.183:80'

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

# from subprocess import call
# print(call(["wget",  "-q", "-O", "-", "checkip.dyndns.org"]))

###################################


# create log in case of errors
logger = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


updater = Updater(token='617888050:AAEqmIsJmBrv00PtE82uj1iuxg2iJWa0Rt0')
dispatcher = updater.dispatcher




# message handling ############

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

#################################

def get_meaning_API(word):
    try:
        return get_meaning(word)
    except:
        return "Lol dude, some weird error"


def get_meaning_pyDict(word):
    meaning = ''

    try:
        get_meaning = dictionary.meaning(str(word))
        for key, value in get_meaning.items():
            meaning += str(key) + ':' + '\n'
            for i in value:
                meaning += '-' + (i) + '\n'
        return meaning
    except:
        return "Lol dude, some weird error"


def identity_check(bot, update):
    if update.message.chat_id != 137916237:
        bot.send_message(chat_id=update.message.chat_id, text="Huh, I don't like you")
        return True
    else:
        return False


# tg command functions

def start(bot, update):

    if identity_check(bot, update):
        print("Somebody tried to use the bot")
        return

    bot.send_message(chat_id=update.message.chat_id, text="Look up description to correctly use this!")
    return PROCESSER


def caps(bot, update, args):

    # print(update.message.chat_id)

    if identity_check(bot, update):
        print("Somebody tried to use the bot")
        return

    text_caps = ' '.join(args).upper()

    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def meaning(bot, update, args):
    if identity_check(bot, update):
        print("Somebody tried to use the bot")
        return

    global last_meaning

    meaning = get_meaning_API(str(args[0]))

    last_meaning = meaning

    keyboard = [[InlineKeyboardButton("Add word", callback_data=("1!!!" + str(args[0])) )]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(meaning, reply_markup=reply_markup)

    # bot.send_message(chat_id=update.message.chat_id, text=meaning)





def add_word(bot, update, args):

    if identity_check(bot, update):
        print("Somebody tried to use the bot")
        return

    item = str(args[0])
    meaning = get_meaning_API(item)
    customDict.add_item(item, meaning)

    bot.send_message(chat_id=update.message.chat_id, text="{} is added to the dictionary".format(item))


def add_idea(bot, update, args):

    if identity_check(bot, update):
        print("Somebody tried to use the bot")
        return

    name = ' '.join(str(args[0]).split("_"))
    body = args[1:]
    Ideas.add_item(name, body)

    bot.send_message(chat_id=update.message.chat_id, text="{} is added to the dictionary".format(name))


# def list_storage(bot, update, args):
#
#     if identity_check(bot, update):
#         print("Somebody tried to use the bot")
#         return
#
#     if args[0] in storages.keys():
#         out = storages[args[0]].list_items()
#     else:
#         out = "Wrong key, dude"
#
#     bot.send_message(chat_id=update.message.chat_id, text=out)

def list_storage(bot, update):

    if identity_check(bot, update):
        print("Somebody tried to use the bot")
        return

    keyboard = [[InlineKeyboardButton(i, callback_data=("2!!!" + i))] for i in storages.keys()]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Which one?", reply_markup=reply_markup)



def button(bot, update):
    query = update.callback_query

    num, data = query.data.split("!!!")[0], query.data.split("!!!")[1]

    if int(num) == 2:
        out = storages[data].list_items()
        bot.edit_message_text(text=out,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return
    if int(num) == 1:
        word = data
        meaning = last_meaning

        # print(word + meaning)

        bot.edit_message_text(text="Word {} is added to the dictionary".format(word),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        customDict.add_item(word, meaning)
        return


# Conversation_functions############################

def processor(bot, update):
    user = update.message.from_user
    data = update.message.text

    special_char = {WORD: ":",
                    IDEA: "-"}

    for i, value in special_char.items():
        if value in data:
            return i

#     still needs to be done a lot

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

# ~Conversation_functions##############################



# def list_storage_button(bot, update):
#     query = update.callback_query
#
#     out = storages[query.data].list_items()
#     bot.edit_message_text(text=out,
#                           chat_id=query.message.chat_id,
#                           message_id=query.message.message_id)

# tg CommandHandler setup
caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

meaning_handler = CommandHandler('meaning', meaning, pass_args=True)
dispatcher.add_handler(meaning_handler)

add_word_handler = CommandHandler('add_word', add_word, pass_args=True)
dispatcher.add_handler(add_word_handler)

add_idea_handler = CommandHandler('add_idea', add_idea, pass_args=True)
dispatcher.add_handler(add_idea_handler)

list_storage_handler = CommandHandler('list_storage', list_storage)
dispatcher.add_handler(list_storage_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(button))
# updater.dispatcher.add_handler(CallbackQueryHandler(list_storage_button))


PROCESSOR, WORD, IDEA = range(3)


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PROCESSOR: [MessageHandler(Filters.text, processor)],

            WORD: [MessageHandler(Filters.text, photo),
                    CommandHandler('skip', skip_photo)],

            IDEA: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

updater.add_handler(conv_handler)


# log all errors
updater.add_error_handler(error)



updater.start_polling()
