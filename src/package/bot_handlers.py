import logging,os, sys
from selenium import webdriver
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters,ConversationHandler
from .bot_constants import TYPE, QUERY_CITY, TRIGGER_SCRAPING,END, RESULTS  # Adjust the import path as needed
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import aiohttp
import asyncio



# Get current date and time as a formatted string
folder_name = datetime.now().strftime("%Y-%m-%d")

# Set up logging
logger = logging.getLogger(__name__)
DEFAULT_STATE = 'START'  


class StartHandler:
    @staticmethod
    async def ask_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # Logic for the start command
        reply_keyboard = [['Affittare', 'Acquistare']]
        await update.message.reply_text(
            "Hi! My name is Professor Bot. I will hold a conversation with you. "
            "Send /cancel to stop talking to me.\n\n"
            "Do you want Affittare or Acquistare?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="What's your choice?"
            ),
        )
        return TYPE  # Make sure TYPE is defined in your main script or in a constants file

class TypeHandler:
    @staticmethod
    async def receive_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # Logic for handling the user's type selection
        user = update.message.from_user
        logger.info("Type of %s: %s", user.first_name, update.message.text)
        context.user_data['type'] = update.message.text
        await update.message.reply_text(
            "Great! Please tell me the location you're interested in.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return QUERY_CITY  # Make sure QUERY_CITY is defined in your main script or in a constants file

class LocationHandler:
    @staticmethod
    async def receive_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # Logic for handling the user's location input
        user = update.message.from_user
        logger.info("Location of %s: %s", user.first_name, update.message.text)
        context.user_data['location'] = update.message.text
        await update.message.reply_text(
            "Location noted! Initiating the research"
            
        )
        return TRIGGER_SCRAPING  # Define NEXT_STEP as needed
    
    async def trigger_scraping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # Call the scraping function
        user = update.message.from_user
        logger.info("User %s triggered scraping.", user.first_name)
        chat_id = update.message.chat_id
        
        city = context.user_data['location']  # Make sure 'city' is set in user data
        folder = './RESULTS'  # Set the folder path
        if not os.path.exists(folder):
            os.mkdir(folder)

        try:
            result = await HandleLocationSearch.scrape_immobiliare(city, folder)
            await context.bot.send_message(chat_id=chat_id, text=result)
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"An error occurred: {str(e)}")

        return ConversationHandler.END  # Or move to another state if you have more steps

class HandleLocationSearch:
    @staticmethod

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.status

    async def retrieve_status_code(url):
        async with aiohttp.ClientSession() as session:
            status_code = await HandleLocationSearch.fetch(session, url)
            print(status_code)

    async def scrape_immobiliare(city,folder):
            # Replace this URL with the specific results page URL for your city
            # Set up the Selenium WebDriver. You might need to download a driver for this to work.
            # driver = webdriver.Chrome()
            url = f'https://www.immobiliare.it/vendita-case/{city}/'
            # Open the URL in Selenium
            # driver.get(url)

            # Wait for JavaScript to load (you might need to adjust the sleep time)
            # import time
            # time.sleep(5)
            
            logger.info("Serching in : %s",  url)

            print(folder)
            if not os.path.exists(folder):
                os.mkdir(folder)
            
            # Make an HTTP request to the URL using aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    # Check if the request was successful
                    if response.status != 200:
                        logger.info("Failed to retrieve data")
                        return
                    html_content = await response.text()
                    print(type(html_content))  # This should print <class 'str'>

                    soup = BeautifulSoup(html_content, 'html.parser')
                    print(soup.prettify())
                    # Find elements that contain the data you're interested in
                    # This is a placeholder example, you'll need to adjust selectors
                    # based on the actual structure of the webpage
                    # listings = soup.find_all('div', class_='in-reListCard')
                    listings  =  soup.find('li', class_='nd-list__item in-reListItem')
                    # listings = soup.find('li', {'class': 'nd-list__item in-reListItem'})
                    print(len(listings))
                    # print(listings)
                    # sys.exit(1)
                    # List to store each listing's information
                    listings_data = []

                    # Extract and print information from each listing
                    for listing in listings:
                        title_link = list_item.find('a', class_='in-reListCard__title')
                        title = title_link.text if title_link else "No title found"
                        link = title_link['href'] if title_link else "No link found"
                    
                        # Append a dictionary for each listing to the list
                        listings_data.append({
                            'Title': title,
                            'Link': link
                        })

                    # Write the list of dictionaries to a JSON file
                    with open(f'{folder}/{city}_listings.json', 'w', encoding='utf-8') as file:
                        json.dump(listings_data, file, ensure_ascii=False, indent=4)

                    # Don't forget to close the driver
                    # driver.quit()

                    return f"Data scraped and saved to {city}_listings.json"
                
        # Example usage
        # scrape_immobiliare('milano')

class CancelHandler:
    @staticmethod
    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # Logic to handle conversation cancellation
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        await update.message.reply_text(
            "Bye! Hope to talk to you again soon.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

class TextHandler:
    @staticmethod

    # function to handle normal text 
    async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        conversation_state = context.user_data.get('conversational_state', DEFAULT_STATE)


        if conversation_state == TYPE:
            if update.message.text != "Affittare" and update.message.text != "Acquistare":
                update.message.reply_text("gg retard, clicca su uno dei bottoni sottostanti, grazie.")
            else:
                return HandleLocationSearch().get_search_type(update, context)
        
        if conversation_state == QUERY_CITY:
            return HandleLocationSearch().get_query_result_city(update, context)

        if conversation_state == END:
            update.message.reply_text("Se vuoi iniziare una ricerca con le preferenze salvate, digita /startsearch.")

        if conversation_state == RESULTS:
            update.message.reply_text('Results')
            # return get_more_data(update, context)

