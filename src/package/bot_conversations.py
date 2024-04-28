# bot_conversations.py

#! /usr/bin/python
# -
# *- coding: utf-8 -*-
"""
WEB SCRAPING 
Date: '02 APR 2024'
Update: '02 APR 2024'
Author: Marco De Stavola '
"""

from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .bot_handlers import TypeHandler, LocationHandler,StartHandler, CancelHandler,TextHandler,RestartHandler
from .bot_constants import TYPE, QUERY_CITY,TRIGGER_SCRAPING,RESULTS  # Adjust the import path as needed


def get_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", StartHandler.ask_type)],
        states={
            TYPE: [
                # CommandHandler('Affittare', TypeHandler.receive_type)
                MessageHandler(filters.Regex("^(Affittare|Acquistare|Altro)$"), TypeHandler.receive_type)
                ],
            QUERY_CITY: [MessageHandler(filters.TEXT, LocationHandler.receive_location)],
            # TRIGGER_SCRAPING: [MessageHandler(filters.Regex('^scrape$'), LocationHandler.trigger_scraping)],
            TRIGGER_SCRAPING: [
                # CommandHandler('search', LocationHandler.trigger_scraping)
                CallbackQueryHandler(LocationHandler.trigger_scraping, pattern='^start_scraping$') 
            ],
            RESULTS: [MessageHandler(filters.TEXT, TextHandler.text)]
            # Add other states and handlers here
        },
        fallbacks=[CommandHandler("cancel", CancelHandler.cancel),
                   CommandHandler("restart", RestartHandler.restart) 
                   ],
    )
