from bs4 import BeautifulSoup
import json, sys

class Scraping():
    def scrape_immobiliare(self,city,folder,timestr):
        file_path = f'../{folder}/{city}_{timestr}_soup.html'
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'lxml')  # You can also use 'html.parser' instead of 'lxml'
            listings  =  soup.find('li', class_='nd-list__item in-reListItem')
            # listings = soup.find('li', {'class': 'nd-list__item in-reListItem'})
            print(len(listings))
            sys.exit(1)
            # List to store each listing's information
            listings_data = []

            # Extract and print information from each listing
            for listing in listings:
                title_link = listing.find('a', class_='in-reListCard__title')
                title = title_link.text if title_link else "No title found"
                link = title_link['href'] if title_link else "No link found"
            
                # Append a dictionary for each listing to the list
                listings_data.append({
                    'Title': title,
                    'Link': link
                })

        
        return soup