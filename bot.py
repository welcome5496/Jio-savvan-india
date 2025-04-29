import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot's API key from BotFather
API_KEY = "8157582382:AAGgIhtU_jmzK24bqjCDSfOnl6Y5hPtEEdo"

# Function to start the bot and show the welcome message
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Search Song", callback_data='search')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to the JioSaavn bot! You can search for songs below.', reply_markup=reply_markup)

# Function to handle the song search
def search_song(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Please send the song name you're looking for.")

# Function to handle user message and search the song
def handle_message(update: Update, context):
    song_name = update.message.text
    search_url = f"https://www.jiosaavn.com/api.php?__call=webapi.get&token=&query={song_name}"
    response = requests.get(search_url).json()

    if response['status'] == 'ok' and 'songs' in response:
        songs = response['songs']
        song_list = []
        for song in songs[:5]:  # Show only top 5 songs
            song_list.append(f"{song['name']} by {song['primary_artists']} - [Link]({song['perma_url']})")
        
        update.message.reply_text("\n\n".join(song_list), parse_mode='Markdown')
    else:
        update.message.reply_text("Sorry, no songs found. Please try again.")

# Function to log errors
def error(update: Update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Initialize Updater and Dispatcher
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Command Handlers
    dp.add_handler(CommandHandler("start", start))

    # Callback Handlers
    dp.add_handler(CallbackQueryHandler(search_song, pattern='search'))

    # Message Handlers
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Updated filter syntax

    # Error Handler
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
