import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import Bot , InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import requests

API_KEY = os.environ['API_KEY']
bot = Bot(API_KEY)

def start(update,context):
  user = update.message.from_user
  result = f"Hello and welcome {user['username']} !\n\nSend a keyword to get a wallpaper related to it.\nOr send /random to generate a random one.\n\n Enjoy! :)"
  update.message.reply_text(result)

def about(update,context):
  update.message.reply_text("This is a wallpapers generator bot, made by @itsmeyukki.")
  
def message_handler(update,context):
        user = update.message.from_user
        msg = update.message.text
        board(update, context,msg)
  
def random(update,context):
  update.message.reply_text("Your picture is being loaded..")
  pic = requests.get("https://picsum.photos/850/1280")
  bot.send_photo(chat_id=update.message.chat_id, photo=pic.url)

def board(update,context,msg):    
    user = update.message.from_user
    keyboard = [
      [ InlineKeyboardButton("📱 Mobile 📱", callback_data=f"mobile,{msg}"), InlineKeyboardButton("💻 Laptop/pc 💻", callback_data=f"pc,{msg}")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Pick a text",reply_markup=reply_markup)


def inline(update,context):
    query = update.callback_query
    query.answer()
    queryData = query.data.split(',')
    if(queryData[0] == "mobile"):
        size = "850x1280"
    else:
        size = "1980x1080"
    query.edit_message_text(text="<b>Your pic is being loaded..</b>",parse_mode=ParseMode.HTML)  

    pic = requests.get(f"https://source.unsplash.com/{size}/?{queryData[1]}")
    # If image is not found, it'll be replaced with random one
    if pic.url == "https://images.unsplash.com/source-404?fit=crop&fm=jpg&h=800&q=60&w=1200":
        pic = requests.get(f"https://source.unsplash.com/{size}/random")
    bot.send_photo(query.message.chat_id,pic.url)

updater = Updater(API_KEY)
disp = updater.dispatcher

disp.add_handler(CommandHandler("start",start))
disp.add_handler(CommandHandler("about",about))
disp.add_handler(CommandHandler("random",random))
disp.add_handler(MessageHandler(Filters.text, message_handler))
disp.add_handler(CallbackQueryHandler(inline))

updater.start_polling()
updater.idle()

# @itsmeyukki
