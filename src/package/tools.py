#! /usr/bin/python
# -
# *- coding: utf-8 -*-
"""
WEB SCRAPING 
Date: '24 MAR 2024'
Update: '24 MAR 2024'
Author: Marco De Stavola '
"""
import json

class Scraper():
    def __init__(self,response):
        self.response = response

    def handle_rest_response(self):
        """
        Handles different REST responses.

        :param response: The response object from a REST API call.
        :return: Parsed data or error message.
        """
        try:
            # Check if the response was successful
            if 200 <= self.response.status_code < 300:
                # Attempt to parse JSON data from the self.response
                return self.response.json()
            else:
                # For non-success codes, return an error message
                return f"Error {self.response.status_code}: {self.response.reason}"
        except json.JSONDecodeError:
            # Handle cases where self.response is not in JSON format
            return "Invalid JSON in self.response"
        except Exception as e:
            # General error handling
            return f"An error occurred: {str(e)}"

class HandleText():

    def __init__(self,context):
        self.context = context

    def create_data_model(self):
        self.context.user_data["min_price"] = None
        self.context.user_data["max_price"] = None
        self.context.user_data["min_surface"] = None
        self.context.user_data["max_surface"] = None
        self.context.user_data["searches"] = []
        self.context.user_data['notifications'] = False

    # function to handle the /start command
    async def start(self,update):
        first_name = update.message.chat.first_name

        if len(self.context.user_data) > 0:
            update.message.reply_text(f"Ciao {first_name}, bentornato!\n\nPer visualizzare i tuoi dati salvati digita /getpreferences.\n\nPer iniziare una nuova ricerca digita /startsearch.\n\nPer modificare le tue preferenze digita /editpreferences.")
        else:
            update.message.reply_text(f"Ciao {first_name}, piacere di conoscerti!")
            self.context.user_data['chat_id'] = update.message.chat.id
            create_data_model()
            start_search(update)

    # function to handle normal text 
    def text(self, update):
        conversation_state = self.context.user_data['conversational_state']

        if conversation_state == TYPE:
            if update.message.text != "Affittare" and update.message.text != "Acquistare":
                update.message.reply_text("gg retard, clicca su uno dei bottoni sottostanti, grazie.")
            else:
                return get_search_type(update, self.context)
        
        if conversation_state == QUERY_CITY:
            return get_query_result_city(update, self.context)

        if conversation_state == QUERY_NEIGHBOURHOOD:
            return get_query_result_neighbourhood(update, self.context)

        #allow skipping of params of search
        if update.message.text.lower() == "skip":
            conversation_state += 1

            update.message.text = None

        if conversation_state == MIN_PRICE:
            if update.message.text and not is_number(update.message.text):
                update.message.reply_text("Inserisci un numero intero, senza virgole e punti.")
            else:
                return get_min_price(update, self.context)

        if conversation_state == MAX_PRICE:
            if update.message.text and not is_number(update.message.text):
                update.message.reply_text("Inserisci un numero intero, senza virgole e punti.")
            else:
                return get_max_price(update, self.context)

        if conversation_state == MIN_SURFACE:
            if update.message.text and not is_number(update.message.text):
                update.message.reply_text("Inserisci un numero intero, senza virgole e punti.")
            else:
                return get_min_surface(update, self.context)

        if conversation_state == MAX_SURFACE:
            if update.message.text and not is_number(update.message.text):
                update.message.reply_text("Inserisci un numero intero, senza virgole e punti.")
            else:
                return get_max_surface(update, self.context)
        
        if conversation_state == END:
            update.message.reply_text("Se vuoi iniziare una ricerca con le preferenze salvate, digita /startsearch.")

        if conversation_state == RESULTS:
            return get_more_data(update, self.context)
