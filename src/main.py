#! /usr/bin/python
# -
# *- coding: utf-8 -*-
"""
WEB SCRAPING 
Date: '02 APR 2024'
Update: '02 APR 2024'
Author: Marco De Stavola '
"""

# main.py

import logging
from telegram.ext import Application
from package import get_conversation_handler

def main() -> None:
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    logger = logging.getLogger(__name__)

    application = Application.builder().token("6845005306:AAHASISYw1H_hry4h3GO_expZhr13lxXdOI").build()

    conv_handler = get_conversation_handler()
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
