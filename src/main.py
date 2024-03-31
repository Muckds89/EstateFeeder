#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

TYPE = 1
QUERY_CITY = 2
QUERY_NEIGHBOURHOOD = 3
MACROZONE = 4
MIN_PRICE = 5
MAX_PRICE = 6
MIN_SURFACE = 7
MAX_SURFACE = 8
END = 9

RESULTS = 100

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TYPE, LOCATION = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their research type."""
    reply_keyboard = [['Affittare', 'Acquistare','Altro']]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Do you want Affittare or Acquistare?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return TYPE

async def type(update, context) -> int:
    """Stores the selected type and asks for a location."""
    user = update.message.from_user
    logger.info("Type of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please let me know which location, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location."""
    user = update.message.from_user
    logger.info("Location of %s: %s", user.first_name, update.message.text)

    return ConversationHandler.END

async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me the location of the research."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TYPE: [MessageHandler(filters.Regex("^(Affittare|Acquistare|Altro)$"),type)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location), CommandHandler("skip", skip_location)], 
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()